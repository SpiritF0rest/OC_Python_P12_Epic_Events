from click.testing import CliRunner
from sqlalchemy import select

from epic_events.controllers.user_controller import create_user
from epic_events.models import User


class TestUserController:
    runner = CliRunner()

    def test_create_user_with_missing_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        result = self.runner.invoke(create_user, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 2
        assert "Missing option" in result.output

    def test_create_user_with_existing_user(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        email = "manager_toto@test.com"
        options = ["-n", "toto", "-e", email, "-r", "management", "--password", "1234"]
        result = self.runner.invoke(create_user, options, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 1
        assert f"User ({email}) already exists." in result.output
