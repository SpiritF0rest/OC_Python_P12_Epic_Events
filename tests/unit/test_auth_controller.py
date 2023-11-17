from click.testing import CliRunner

from epic_events.controllers.auth_controller import login, logout


class TestAuthController:
    runner = CliRunner()

    def test_login(self, mocked_session):
        with self.runner.isolated_filesystem():
            options = ["-e", "manager_alex@test.com", "--password", "1234"]
            result = self.runner.invoke(login, options, obj={"session": mocked_session})
            assert result.exit_code == 0
            assert "Connection successful." in result.output

    def test_login_with_connected_user(self, mocked_session):
        with self.runner.isolated_filesystem():
            options = ["-e", "manager_alex@test.com", "--password", "1234"]
            result = self.runner.invoke(login, options, obj={"session": mocked_session})
            assert result.exit_code == 0
            assert "Connection successful." in result.output

            options = ["-e", "manager_alex@test.com", "--password", "1234"]
            result = self.runner.invoke(login, options, obj={"session": mocked_session})
            assert result.exit_code == 1
            assert "You are already connected." in result.output

    def test_login_with_wrong_password(self, mocked_session):
        with self.runner.isolated_filesystem():
            options = ["-e", "manager_alex@test.com", "--password", "4567"]
            result = self.runner.invoke(login, options, obj={"session": mocked_session})
            assert result.exit_code == 1
            assert "Please, be sure to use the correct email and password." in result.output

    def test_login_with_wrong_email(self, mocked_session):
        with self.runner.isolated_filesystem():
            options = ["-e", "unknown@test.com", "--password", "1234"]
            result = self.runner.invoke(login, options, obj={"session": mocked_session})
            assert result.exit_code == 1
            assert "Please, be sure to use the correct email and password." in result.output

    def test_logout(self, mocked_session):
        with self.runner.isolated_filesystem():
            options = ["-e", "manager_alex@test.com", "--password", "1234"]
            result = self.runner.invoke(login, options, obj={"session": mocked_session})
            assert result.exit_code == 0
            assert "Connection successful." in result.output
            result = self.runner.invoke(logout, input="y", obj={"session": mocked_session})
            assert result.exit_code == 0
            assert "You are disconnected, see you later." in result.output
