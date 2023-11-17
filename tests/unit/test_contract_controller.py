from click import ClickException
from click.testing import CliRunner
from sqlalchemy import select

from epic_events.controllers.contract_controller import (list_contracts, delete_contract, get_contract,
                                                         update_contract, create_contract, check_amount)
from epic_events.models import User, Contract


class TestListContractController:
    runner = CliRunner()

    def test_list_contract(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        result = self.runner.invoke(list_contracts, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 0
        assert 2 == result.output.count("Id")

    def test_list_contract_with_filter(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-s", "SIGNED"]
        result = self.runner.invoke(list_contracts, options, obj={"session": mocked_session,
                                                                  "current_user": current_user})
        assert result.exit_code == 0
        assert 1 == result.output.count("Id")


class TestCreateContractController:
    runner = CliRunner()

    def test_create_contract_with_unknown_client(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-client", 777, "-a", 100]
        result = self.runner.invoke(create_contract, options, obj={"session": mocked_session,
                                                                   "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this client does not exist." in result.output

    def test_create_contract_with_correct_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-client", 1, "-a", 100]
        result = self.runner.invoke(create_contract, options, obj={"session": mocked_session,
                                                                   "current_user": current_user})
        assert result.exit_code == 0
        assert "Contract 3 is successfully created." in result.output


class TestUpdateContractController:
    runner = CliRunner()

    def test_update_contract_without_optional_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", 1]
        result = self.runner.invoke(update_contract, options, obj={"session": mocked_session,
                                                                   "current_user": current_user})
        assert result.exit_code == 1
        assert "Can't update without data in the command." in result.output

    def test_update_contract_with_unknown_contract(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", 777, "-s", "SIGNED"]
        result = self.runner.invoke(update_contract, options, obj={"session": mocked_session,
                                                                   "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this contract does not exist." in result.output

    def test_update_contract_with_unauthorized_user(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 4))
        options = ["-id", 1, "-s", "SIGNED"]
        result = self.runner.invoke(update_contract, options, obj={"session": mocked_session,
                                                                   "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, you're not authorized." in result.output

    def test_update_contract_with_correct_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 3))
        contract_id = 2
        amount = 90
        left_to_pay = 10
        status = "SIGNED"
        updated_contract = mocked_session.scalar(select(Contract).where(Contract.id == contract_id))
        assert updated_contract.total_amount == 100
        assert updated_contract.status == "UNSIGNED"
        options = ["-id", contract_id, "-a", amount, "-ltp", left_to_pay, "-s", status]
        result = self.runner.invoke(update_contract, options, obj={"session": mocked_session,
                                                                   "current_user": current_user})
        assert result.exit_code == 0
        assert [arg in result.output for arg in [str(contract_id), str(amount), str(left_to_pay), status]]
        assert updated_contract.status == status
        assert updated_contract.total_amount == amount


class TestGetContractController:
    runner = CliRunner()

    def test_get_contract_with_unknown_contract(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", 777]
        result = self.runner.invoke(get_contract, options, obj={"session": mocked_session,
                                                                "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this contract does not exist." in result.output

    def test_get_contract_with_correct_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        contract_id = 1
        options = ["-id", contract_id]
        result = self.runner.invoke(get_contract, options, obj={"session": mocked_session,
                                                                "current_user": current_user})
        assert result.exit_code == 0
        assert f"Id: {contract_id}" in result.output


class TestDeleteContractController:
    runner = CliRunner()

    def test_delete_contract_with_unknown_contract(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", 777]
        result = self.runner.invoke(delete_contract, options, input="y", obj={"session": mocked_session,
                                                                              "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this contract does not exist." in result.output

    def test_delete_contract_with_correct_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", 1]
        result = self.runner.invoke(delete_contract, options, input="y", obj={"session": mocked_session,
                                                                              "current_user": current_user})
        assert result.exit_code == 0
        assert "This contract is successfully deleted." in result.output


class TestCheckAmount:

    def test_check_amount_with_correct_argument(self):
        amount = 100
        left_to_pay = 50
        result = check_amount(amount, left_to_pay)
        assert result is True

    def test_check_amount_with_left_to_pay_bigger_than_amount(self):
        amount = 100
        left_to_pay = 200
        error = ("Total amount and left to pay must be positive integer and left to pay can't be bigger "
                 "than total amount.")
        try:
            check_amount(amount, left_to_pay)
        except ClickException as e:
            assert error in e.message
