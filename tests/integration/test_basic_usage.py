from unittest.mock import patch

from click.testing import CliRunner
from sqlalchemy import select

from epic_events.controllers.cli import cli
from epic_events.models import User, Client, Contract, Event


class TestBasicUsage:
    runner = CliRunner()

    def login_user(self, email, password):
        options = ["auth", "login", "-e", email, "--password", password]
        result = self.runner.invoke(cli, options)
        assert result.exit_code == 0
        assert "Connection successful." in result.output

    def logout_user(self):
        options = ["auth", "logout"]
        result = self.runner.invoke(cli, options, input="y")
        assert result.exit_code == 0
        assert "You are disconnected, see you later." in result.output

    @patch("epic_events.controllers.cli.current_session")
    def test_basic_usage_from_connection_to_disconnection_with_crud_process(self, mock_current_session,
                                                                            mocked_session):
        mock_current_session.return_value = mocked_session

        with self.runner.isolated_filesystem():
            # The manager connects to the application
            manager_email = "manager_alex@test.com"
            manager_password = "1234"
            self.login_user(manager_email, manager_password)

            # He creates a new commercial and a new support
            commercial_email = "new_commercial@test.com"
            commercial_name = "Gaël"
            commercial_password = "1234"
            options = ["user", "create", "-n", commercial_name, "-e", commercial_email, "-r", "1",
                       "--password", commercial_password]
            result = self.runner.invoke(cli, options)
            assert result.exit_code == 0
            assert f"User {commercial_email} is successfully created" in result.output
            new_commercial = mocked_session.scalar(select(User).where(User.email == commercial_email))
            assert new_commercial is not None

            support_email = "new_support@test.com"
            support_name = "Daniel"
            support_password = "1234"
            options = ["user", "create", "-n", support_name, "-e", support_email, "-r", "2",
                       "--password", support_password]
            result = self.runner.invoke(cli, options)
            assert result.exit_code == 0
            assert f"User {support_email} is successfully created" in result.output
            new_support = mocked_session.scalar(select(User).where(User.email == support_email))
            assert new_support is not None

            # He logs out of the application
            self.logout_user()

            # The new commercial connects to the app
            self.login_user(commercial_email, commercial_password)

            # He creates a new client
            client_email = "sophia@test.com"
            client_name = "sophia"
            options = ["client", "create", "-e", client_email, "-n", client_name,
                       "-ph", 123456789, "-c", "chess tournament"]
            result = self.runner.invoke(cli, options)
            assert result.exit_code == 0
            assert f"Client {client_email} is successfully created." in result.output
            new_client = mocked_session.scalar(select(Client).where(Client.email == client_email))
            assert new_client is not None
            assert new_client.name == client_name
            assert new_client.commercial_contact_id == new_commercial.id

            # He logs out of the application
            self.logout_user()

            # The manager connects to the application
            self.login_user(manager_email, manager_password)

            # He creates a contract for the new client
            options = ["contract", "create", "-client", new_client.id, "-a", 100]
            result = self.runner.invoke(cli, options)
            assert result.exit_code == 0
            assert "Contract 3 is successfully created." in result.output
            new_contract = mocked_session.scalar(select(Contract).where(Contract.client_id == new_client.id))
            assert new_contract is not None

            # He logs out of the application
            self.logout_user()

            # The new commercial connects to the app
            self.login_user(commercial_email, commercial_password)

            # He updates the contract
            left_to_pay = 90
            status = "SIGNED"
            assert new_contract.status == "UNSIGNED"
            options = ["contract", "update", "-id", new_contract.id, "-ltp", left_to_pay, "-s", status]
            result = self.runner.invoke(cli, options)
            assert result.exit_code == 0
            assert [arg in result.output for arg in [str(new_contract.id), str(left_to_pay), status]]
            assert new_contract.status == status
            assert new_contract.left_to_pay == left_to_pay

            # He creates an event
            options = ["event", "create", "-c", new_contract.id]
            result = self.runner.invoke(cli, options)
            assert result.exit_code == 0
            assert "Event 2 is successfully created." in result.output
            new_event = mocked_session.scalar(select(Event).where(Event.contract_id == new_contract.id))
            assert new_event is not None

            # He logs out of the application
            self.logout_user()

            # The manager connects to the application
            self.login_user(manager_email, manager_password)

            # He assigns a support to the event
            options = ["event", "contact", "-id", new_event.id, "-s", new_support.id]
            result = self.runner.invoke(cli, options)
            assert result.exit_code == 0
            assert f"{new_support.name} is now responsible for the event {new_event.id}" in result.output

            # He logs out of the application
            self.logout_user()

            # The new support connects to the application
            self.login_user(support_email, support_password)

            # He updates the event
            attendees = 50
            options = ["event", "update", "-id", new_event.id, "-a", attendees]
            result = self.runner.invoke(cli, options)
            assert result.exit_code == 0
            assert [arg in result.output for arg in [str(new_event.id), str(attendees)]]
            assert new_event.attendees == attendees

            # He logs out of the application
            self.logout_user()

            # The new commercial connects to the app
            self.login_user(commercial_email, commercial_password)

            # Unfortunately the client is closing their business, so the new commercial deletes him.
            options = ["client", "delete", "-id", new_client.id]
            result = self.runner.invoke(cli, options, input="y")
            assert result.exit_code == 0
            assert "This client is successfully deleted." in result.output
            deleted_client = mocked_session.scalar(select(Client).where(Client.id == new_client.id))
            old_contract = mocked_session.scalar(select(Contract).where(Contract.id == new_contract.id))
            old_event = mocked_session.scalar(select(Event).where(Event.id == new_event.id))
            assert deleted_client is None
            assert old_contract is None
            assert old_event is None

            # He logs out of the application
            self.logout_user()
