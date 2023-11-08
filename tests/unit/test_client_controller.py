from click.testing import CliRunner
from sqlalchemy import select

from epic_events.controllers.client_controller import list_clients, get_client
from epic_events.models import User


class TestListClientController:
    runner = CliRunner()

    def test_list_client(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        result = self.runner.invoke(list_clients, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 0
        assert 1 == result.output.count("Client")


class TestGetClientController:
    runner = CliRunner()

    def test_get_client_without_id(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        result = self.runner.invoke(get_client, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 2
        assert "Missing option" in result.output

    def test_get_client_with_unknown_id(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", "777"]
        result = self.runner.invoke(get_client, options, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this client does not exist." in result.output

    def test_get_client_with_existing_id(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", "1"]
        result = self.runner.invoke(get_client, options, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 0
        assert "Client(id=1" in result.output
