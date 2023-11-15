from click.testing import CliRunner
from sqlalchemy import select

from epic_events.controllers.user_controller import create_user
from epic_events.models import User


class TestCreateUserController:
    runner = CliRunner()

    def test_create_user_with_unauthorized_user(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 2))
        email = "jack@test.com"
        options = ["-n", "jack", "-e", email, "-r", "1", "--password", "1234"]
        result = self.runner.invoke(create_user, options, obj={"session": mocked_session,
                                                               "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, you're not authorized." in result.output
