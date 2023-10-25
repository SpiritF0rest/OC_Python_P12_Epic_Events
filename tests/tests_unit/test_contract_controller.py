from click.testing import CliRunner
from sqlalchemy import select

from epic_events.controllers.contract_controller import list_contracts
from epic_events.models import User


class TestListContractController:
    runner = CliRunner()

    def test_list_contract(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        result = self.runner.invoke(list_contracts, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 0
        assert 2 == result.output.count("Contract")
