from click.testing import CliRunner
from sqlalchemy import select

from epic_events.controllers.client_controller import create_client, update_client_contact
from epic_events.controllers.user_controller import create_user
from epic_events.models import User, Client


class TestChangeClientContact:
    runner = CliRunner()

    def test_change_client_contact(self, mocked_session):
        # the manager creates two commercials
        manager = mocked_session.scalar(select(User).where(User.id == 1))
        first_commercial_email = "first_commercial@test.com"
        first_commercial_name = "Gaël"
        first_commercial_password = "1234"
        first_options = ["-n", first_commercial_name, "-e", first_commercial_email, "-r", "1",
                         "--password", first_commercial_password]
        result = self.runner.invoke(create_user, first_options, obj={"session": mocked_session,
                                                                     "current_user": manager})
        assert result.exit_code == 0
        assert f"User {first_commercial_email} is successfully created" in result.output
        first_commercial = mocked_session.scalar(select(User).where(User.email == first_commercial_email))
        assert first_commercial is not None

        second_commercial_email = "second_commercial@test.com"
        second_commercial_name = "Emilie"
        second_commercial_password = "1234"
        second_options = ["-n", second_commercial_name, "-e", second_commercial_email, "-r", "1",
                          "--password", second_commercial_password]
        result = self.runner.invoke(create_user, second_options, obj={"session": mocked_session,
                                                                      "current_user": manager})
        assert result.exit_code == 0
        assert f"User {second_commercial_email} is successfully created" in result.output
        second_commercial = mocked_session.scalar(select(User).where(User.email == second_commercial_email))
        assert second_commercial is not None

        # the first commercial creates a new client, he is therefore by default his contact
        client_email = "sophia@test.com"
        client_name = "sophia"
        options = ["-e", client_email, "-n", client_name, "-ph", 123456789, "-c", "chess tournament"]
        result = self.runner.invoke(create_client, options,
                                    obj={"session": mocked_session, "current_user": first_commercial})
        assert result.exit_code == 0
        assert f"Client {client_email} is successfully created." in result.output
        new_client = mocked_session.scalar(select(Client).where(Client.email == client_email))
        assert new_client is not None
        assert new_client.name == client_name
        assert new_client.commercial_contact_id == first_commercial.id

        # the first commercial can no longer be the contact, the manager therefore changes the client contact
        options = ["-id", new_client.id, "-c", second_commercial.id]
        result = self.runner.invoke(update_client_contact, options,
                                    obj={"session": mocked_session, "current_user": manager})
        assert result.exit_code == 0
        assert f"{second_commercial.name} is now responsible for the client {new_client.id}" in result.output
        assert new_client.commercial_contact_id == second_commercial.id
