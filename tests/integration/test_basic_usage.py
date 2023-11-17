from click.testing import CliRunner
from sqlalchemy import select

from epic_events.controllers.auth_controller import login, logout
from epic_events.controllers.client_controller import create_client, delete_client
from epic_events.controllers.contract_controller import create_contract, update_contract
from epic_events.controllers.event_controller import create_event, update_event_support_contact, update_event
from epic_events.controllers.user_controller import create_user
from epic_events.models import User, Client, Contract, Event


class TestBasicUsage:
    runner = CliRunner()

    def test_basic_usage_from_connection_to_disconnection_with_crud_process(self, mocked_session):
        # the manager creates a new commercial and a new support
        manager = mocked_session.scalar(select(User).where(User.id == 1))
        commercial_email = "new_commercial@test.com"
        commercial_name = "Gaël"
        commercial_password = "1234"
        options = ["-n", commercial_name, "-e", commercial_email, "-r", "1", "--password", commercial_password]
        result = self.runner.invoke(create_user, options, obj={"session": mocked_session,
                                                               "current_user": manager})
        assert result.exit_code == 0
        assert f"User {commercial_email} is successfully created" in result.output
        new_commercial = mocked_session.scalar(select(User).where(User.email == commercial_email))
        assert new_commercial is not None

        support_email = "new_support@test.com"
        support_name = "Daniel"
        support_password = "1234"
        options = ["-n", support_name, "-e", support_email, "-r", "2", "--password", support_password]
        result = self.runner.invoke(create_user, options, obj={"session": mocked_session,
                                                               "current_user": manager})
        assert result.exit_code == 0
        assert f"User {support_email} is successfully created" in result.output
        new_support = mocked_session.scalar(select(User).where(User.email == support_email))
        assert new_support is not None

        # the new commercial creates a new client
        client_email = "sophia@test.com"
        client_name = "sophia"
        options = ["-e", client_email, "-n", client_name, "-ph", 123456789, "-c", "chess tournament"]
        result = self.runner.invoke(create_client, options,
                                    obj={"session": mocked_session, "current_user": new_commercial})
        assert result.exit_code == 0
        assert f"Client {client_email} is successfully created." in result.output
        new_client = mocked_session.scalar(select(Client).where(Client.email == client_email))
        assert new_client is not None
        assert new_client.name == client_name

        # the manager creates a contract for the new client
        options = ["-client", new_client.id, "-a", 100]
        result = self.runner.invoke(create_contract, options, obj={"session": mocked_session,
                                                                   "current_user": manager})
        assert result.exit_code == 0
        assert "Contract 3 is successfully created." in result.output
        new_contract = mocked_session.scalar(select(Contract).where(Contract.client_id == new_client.id))
        assert new_contract is not None

        # the new commercial updates the contract
        left_to_pay = 90
        status = "SIGNED"
        assert new_contract.status == "UNSIGNED"
        options = ["-id", new_contract.id, "-ltp", left_to_pay, "-s", status]
        result = self.runner.invoke(update_contract, options, obj={"session": mocked_session,
                                                                   "current_user": new_commercial})
        assert result.exit_code == 0
        assert [arg in result.output for arg in [str(new_contract.id), str(left_to_pay), status]]
        assert new_contract.status == status
        assert new_contract.left_to_pay == left_to_pay

        # the new commercial create an event
        options = ["-c", new_contract.id]
        result = self.runner.invoke(create_event, options, obj={"session": mocked_session,
                                                                "current_user": new_commercial})
        assert result.exit_code == 0
        assert "Event 2 is successfully created." in result.output
        new_event = mocked_session.scalar(select(Event).where(Event.contract_id == new_contract.id))
        assert new_event is not None

        # the manager assigns a support to the event
        options = ["-id", new_event.id, "-s", new_support.id]
        result = self.runner.invoke(update_event_support_contact, options, obj={"session": mocked_session,
                                                                                "current_user": manager})
        assert result.exit_code == 0
        assert f"{new_support.name} is now responsible for the event {new_event.id}" in result.output

        # the new support update the event
        attendees = 50
        options = ["-id", new_event.id, "-a", attendees]
        result = self.runner.invoke(update_event, options, obj={"session": mocked_session,
                                                                "current_user": new_support})
        assert result.exit_code == 0
        assert [arg in result.output for arg in [str(new_event.id), str(attendees)]]
        assert new_event.attendees == attendees

        # unfortunately the client is closing their business, so the new commercial deletes him.
        options = ["-id", new_client.id]
        result = self.runner.invoke(delete_client, options, input="y",
                                    obj={"session": mocked_session, "current_user": new_commercial})
        assert result.exit_code == 0
        assert "This client is successfully deleted." in result.output
        old_client = mocked_session.scalar(select(Client).where(Client.id == new_client.id))
        old_contract = mocked_session.scalar(select(Contract).where(Contract.id == new_contract.id))
        old_event = mocked_session.scalar(select(Event).where(Event.id == new_event.id))
        assert old_client is None
        assert old_contract is None
        assert old_event is None
