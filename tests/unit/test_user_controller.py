from click.testing import CliRunner
from sqlalchemy import select

from epic_events.controllers.user_controller import create_user, get_user
from epic_events.models import User


class TestCreateUserController:
    runner = CliRunner()

    def test_create_user_with_missing_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        result = self.runner.invoke(create_user, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 2
        assert "Missing option" in result.output

    def test_create_user_with_existing_user(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        email = "manager_alex@test.com"
        options = ["-n", "alex", "-e", email, "-r", "management", "--password", "1234"]
        result = self.runner.invoke(create_user, options, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 1
        assert f"User ({email}) already exists." in result.output

    def test_create_user_with_unknown_role(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        role = "unknown"
        options = ["-n", "jack", "-e", "jack@test.com", "-r", role, "--password", "1234"]
        result = self.runner.invoke(create_user, options, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 1
        assert f"{role} is not a correct role." in result.output

    def test_create_user_with_correct_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        email = "jack@test.com"
        options = ["-n", "jack", "-e", email, "-r", "commercial", "--password", "1234"]
        result = self.runner.invoke(create_user, options, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 0
        assert f"User {email} is successfully created" in result.output


class TestGetUserController:
    runner = CliRunner()

    def test_get_user_with_missing_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        result = self.runner.invoke(get_user, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 2
        assert "Missing option" in result.output

    def test_get_user_with_unknown_id(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", 777]
        result = self.runner.invoke(get_user, options, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this user does not exist." in result.output

    def test_get_user_with_non_digit_id(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", "ab"]
        result = self.runner.invoke(get_user, options, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 2
        assert "Invalid value" in result.output

    def test_get_user_with_correct_id(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", 2]
        result = self.runner.invoke(get_user, options, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 0
        assert "User(id=2" in result.output
