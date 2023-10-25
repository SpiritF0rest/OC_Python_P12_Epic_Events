from click.testing import CliRunner
from sqlalchemy import select

from epic_events.controllers.event_controller import list_events
from epic_events.models import User


class TestListEventController:
    runner = CliRunner()

    def test_list_events(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        result = self.runner.invoke(list_events, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 0
        assert 1 == result.output.count("Event")
