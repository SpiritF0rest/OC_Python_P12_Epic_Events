from unittest.mock import patch

from click.testing import CliRunner
from sqlalchemy import select

from epic_events.controllers.cli import cli
from epic_events.models import User, Client


class TestChangeClientContact:
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
    def test_change_client_contact(self, mock_current_session, mocked_session):
        mock_current_session.return_value = mocked_session

        with self.runner.isolated_filesystem():
            # The manager connects to the application
            manager_email = "manager_alex@test.com"
            manager_password = "1234"
            self.login_user(manager_email, manager_password)

            # He creates two commercials
            first_commercial_email = "first_commercial@test.com"
            first_commercial_name = "Gaël"
            first_commercial_password = "1234"
            first_options = ["user", "create", "-n", first_commercial_name, "-e", first_commercial_email, "-r", "1",
                             "--password", first_commercial_password]
            result = self.runner.invoke(cli, first_options)
            assert result.exit_code == 0
            assert f"User {first_commercial_email} is successfully created" in result.output
            first_commercial = mocked_session.scalar(select(User).where(User.email == first_commercial_email))
            assert first_commercial is not None

            second_commercial_email = "second_commercial@test.com"
            second_commercial_name = "Emilie"
            second_commercial_password = "1234"
            second_options = ["user", "create", "-n", second_commercial_name, "-e", second_commercial_email, "-r", "1",
                              "--password", second_commercial_password]
            result = self.runner.invoke(cli, second_options)
            assert result.exit_code == 0
            assert f"User {second_commercial_email} is successfully created" in result.output
            second_commercial = mocked_session.scalar(select(User).where(User.email == second_commercial_email))
            assert second_commercial is not None

            # He logs out of the application
            self.logout_user()

            # The first commercial connects to the application
            self.login_user(first_commercial_email, first_commercial_password)

            # He creates a new client, he is therefore by default his contact
            client_email = "sophia@test.com"
            client_name = "sophia"
            client_company = "chess tournament"
            options = ["client", "create", "-e", client_email, "-n", client_name,
                       "-ph", 123456789, "-c", client_company]
            result = self.runner.invoke(cli, options)
            assert result.exit_code == 0
            assert f"Client {client_email} is successfully created." in result.output
            new_client = mocked_session.scalar(select(Client).where(Client.email == client_email))
            assert new_client is not None
            assert new_client.name == client_name
            assert new_client.commercial_contact_id == first_commercial.id

            # He logs out of the application
            self.logout_user()

            # The manager connects to the application
            self.login_user(manager_email, manager_password)

            # The first commercial can no longer be the contact, the manager therefore changes the client contact
            options = ["client", "contact", "-id", new_client.id, "-c", second_commercial.id]
            result = self.runner.invoke(cli, options)
            assert result.exit_code == 0
            assert f"{second_commercial.name} is now responsible for the client {new_client.id}" in result.output
            assert new_client.commercial_contact_id == second_commercial.id

            # He logs out of the application
            self.logout_user()

            # The first commercial connects to the application
            self.login_user(first_commercial_email, first_commercial_password)

            # He tries to update his former client
            new_company_name = "super chess tournament"
            options = ["client", "update", "-id", new_client.id, "-com", new_company_name]
            result = self.runner.invoke(cli, options)
            assert result.exit_code == 1
            assert "Sorry, you're not authorized." in result.output
            assert new_client.company == client_company

            # He logs out of the application
            self.logout_user()

            # The second commercial connects to the application
            self.login_user(second_commercial_email, second_commercial_password)

            # He updates his new client
            options = ["client", "update", "-id", new_client.id, "-com", new_company_name]
            result = self.runner.invoke(cli, options)
            assert result.exit_code == 0
            assert f"Client {client_email} is successfully updated." in result.output
            assert new_client.company == new_company_name

            # He logs out of the application
            self.logout_user()
