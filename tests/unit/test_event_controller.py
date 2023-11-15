from datetime import datetime

from click import ClickException
from click.testing import CliRunner
from sqlalchemy import select

from epic_events.controllers.event_controller import list_events, delete_event, get_event, update_event, \
    update_event_support_contact, create_event, check_date
from epic_events.models import User


class TestListEventController:
    runner = CliRunner()

    def test_list_events(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        result = self.runner.invoke(list_events, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 0
        assert 1 == result.output.count("Id")

    def test_list_events_with_filter(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-noc"]
        result = self.runner.invoke(list_events, options, obj={"session": mocked_session,
                                                               "current_user": current_user})
        assert result.exit_code == 0
        assert 0 == result.output.count("Id")


class TestCreateEventController:
    runner = CliRunner()

    def test_create_event_with_unknown_contract(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 3))
        options = ["-c", 777]
        result = self.runner.invoke(create_event, options, obj={"session": mocked_session,
                                                                "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this contract does not exist." in result.output

    def test_create_event_with_unauthorized_user(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 4))
        options = ["-c", 1]
        result = self.runner.invoke(create_event, options, obj={"session": mocked_session,
                                                                "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, you're not authorized." in result.output

    def test_create_event_with_unsigned_contract(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 3))
        contract_id = 2
        options = ["-c", 2]
        result = self.runner.invoke(create_event, options, obj={"session": mocked_session,
                                                                "current_user": current_user})
        assert result.exit_code == 1
        assert f"Sorry, the contract (id:{contract_id}) is not signed, we can't create an event." in result.output

    def test_create_event_with_correct_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 3))
        options = ["-c", 1]
        result = self.runner.invoke(create_event, options, obj={"session": mocked_session,
                                                                "current_user": current_user})
        assert result.exit_code == 0
        assert "Event 2 is successfully created." in result.output


class TestUpdateEventSupportContactController:
    runner = CliRunner()

    def test_update_event_support_contact_with_unknown_event(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", 777, "-s", 2]
        result = self.runner.invoke(update_event_support_contact, options, obj={"session": mocked_session,
                                                                                "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this event does not exist." in result.output

    def test_update_event_support_contact_with_unknown_user(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", 1, "-s", 777]
        result = self.runner.invoke(update_event_support_contact, options, obj={"session": mocked_session,
                                                                                "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this user does not exist." in result.output

    def test_update_event_support_contact_with_correct_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        event_id = 1
        options = ["-id", event_id, "-s", 5]
        result = self.runner.invoke(update_event_support_contact, options, obj={"session": mocked_session,
                                                                                "current_user": current_user})
        assert result.exit_code == 0
        assert f"jeremy is now responsible for the event {event_id}" in result.output


class TestUpdateEventController:
    runner = CliRunner()

    def test_update_event_without_optional_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 2))
        options = ["-id", 1]
        result = self.runner.invoke(update_event, options, obj={"session": mocked_session,
                                                                "current_user": current_user})
        assert result.exit_code == 1
        assert "Can't update without data in the command." in result.output

    def test_update_event_with_unknown_event(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 2))
        options = ["-id", 777, "-a", 50]
        result = self.runner.invoke(update_event, options, obj={"session": mocked_session,
                                                                "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this event does not exist." in result.output

    def test_update_event_with_unauthorized_user(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 5))
        options = ["-id", 1, "-a", 50]
        result = self.runner.invoke(update_event, options, obj={"session": mocked_session,
                                                                "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, you're not authorized." in result.output

    def test_update_event_with_correct_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 2))
        event_id = 1
        attendees = 50
        options = ["-id", event_id, "-a", attendees]
        result = self.runner.invoke(update_event, options, obj={"session": mocked_session,
                                                                "current_user": current_user})
        assert result.exit_code == 0
        assert [arg in result.output for arg in [str(event_id), str(attendees)]]


class TestGetEventController:
    runner = CliRunner()

    def test_get_event_with_unknown_event(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 2))
        options = ["-id", 777]
        result = self.runner.invoke(get_event, options, obj={"session": mocked_session,
                                                             "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this event does not exist." in result.output

    def test_get_event_with_correct_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 2))
        event_id = 1
        options = ["-id", event_id]
        result = self.runner.invoke(get_event, options, obj={"session": mocked_session,
                                                             "current_user": current_user})
        assert result.exit_code == 0
        assert f"Id: {event_id}" in result.output


class TestDeleteEventController:
    runner = CliRunner()

    def test_delete_event_with_unknown_event(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 2))
        options = ["-id", 777]
        result = self.runner.invoke(delete_event, options, input="y", obj={"session": mocked_session,
                                                                           "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this event does not exist." in result.output

    def test_delete_event_with_unauthorized_user(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 5))
        options = ["-id", 1]
        result = self.runner.invoke(delete_event, options, input="y", obj={"session": mocked_session,
                                                                           "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, you're not authorized." in result.output

    def test_delete_event_with_correct_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 2))
        options = ["-id", 1]
        result = self.runner.invoke(delete_event, options, input="y", obj={"session": mocked_session,
                                                                           "current_user": current_user})
        assert result.exit_code == 0
        assert "This event is successfully deleted." in result.output


class TestCheckDate:

    def test_check_date_with_correct_date(self):
        start_date = datetime.strptime("01-07-2023 13:00", "%d-%m-%Y %H:%M")
        end_date = datetime.strptime("01-07-2023 15:00", "%d-%m-%Y %H:%M")
        result = check_date(start_date, end_date)
        assert result is None

    def test_check_date_with_end_date_before_start_date(self):
        start_date = datetime.strptime("01-07-2023 15:00", "%d-%m-%Y %H:%M")
        end_date = datetime.strptime("01-07-2023 13:00", "%d-%m-%Y %H:%M")
        try:
            check_date(start_date, end_date)
        except ClickException as e:
            assert f"End date {end_date} can't be before start date {start_date}." in e.message
