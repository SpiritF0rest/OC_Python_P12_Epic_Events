from click.testing import CliRunner
from sqlalchemy import select

from epic_events.controllers.user_controller import create_user, get_user, list_users, delete_user, update_user
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
        options = ["-n", "alex", "-e", email, "-r", "3", "--password", "1234"]
        result = self.runner.invoke(create_user, options, obj={"session": mocked_session,
                                                               "current_user": current_user})
        assert result.exit_code == 1
        assert f"User ({email}) already exists." in result.output

    def test_create_user_with_unknown_role(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        role = "777"
        options = ["-n", "jack", "-e", "jack@test.com", "-r", role, "--password", "1234"]
        result = self.runner.invoke(create_user, options, obj={"session": mocked_session,
                                                               "current_user": current_user})
        assert result.exit_code == 1
        assert f"{role} is not a correct role." in result.output

    def test_create_user_with_correct_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        email = "jack@test.com"
        options = ["-n", "jack", "-e", email, "-r", "1", "--password", "1234"]
        result = self.runner.invoke(create_user, options, obj={"session": mocked_session,
                                                               "current_user": current_user})
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


class TestUpdateUserController:
    runner = CliRunner()

    def test_update_user_with_correct_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        email = "commercial_jack@test.com"
        options = ["-id", 2, "-n", "jack", "-e", email, "-r", 1]
        result = self.runner.invoke(update_user, options, obj={"session": mocked_session,
                                                               "current_user": current_user})
        assert result.exit_code == 0
        assert f"User {email} is successfully updated" in result.output

    def test_update_user_without_optional_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", 2]
        result = self.runner.invoke(update_user, options, obj={"session": mocked_session,
                                                               "current_user": current_user})
        assert result.exit_code == 1
        assert "Can't update without data in the command." in result.output

    def test_update_user_with_unknown_role(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        role_id = 777
        options = ["-id", 2, "-n", "jack", "-r", role_id]
        result = self.runner.invoke(update_user, options, obj={"session": mocked_session,
                                                               "current_user": current_user})
        assert result.exit_code == 1
        assert f"{role_id} is not a correct role." in result.output


class TestDeleteUserController:
    runner = CliRunner()

    def test_delete_user_with_unknown_user_id(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", 777]
        result = self.runner.invoke(delete_user, options, input="y", obj={"session": mocked_session,
                                                                          "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this user does not exist." in result.output

    def test_delete_user_with_correct_user_id(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", 3]
        result = self.runner.invoke(delete_user, options, input="y", obj={"session": mocked_session,
                                                                          "current_user": current_user})
        assert result.exit_code == 0
        assert "This user is successfully deleted" in result.output

    def test_delete_user_with_confirmation_to_no(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", 3]
        result = self.runner.invoke(delete_user, options, input="N", obj={"session": mocked_session,
                                                                          "current_user": current_user})
        assert result.exit_code == 1
        assert "Aborted" in result.output


class TestListUserController:
    runner = CliRunner()

    def test_list_user_with_unknown_role(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        role_id = 777
        options = ["-r", role_id]
        result = self.runner.invoke(list_users, options, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 1
        assert f"{role_id} is not a correct role." in result.output

    def test_list_user_without_filter(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        result = self.runner.invoke(list_users, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 0
        assert 5 == result.output.count("Id")

    def test_list_user_with_filter(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        role_id = 3
        options = ["-r", role_id]
        result = self.runner.invoke(list_users, options, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 0
        assert 1 == result.output.count("Id")
