import click

from epic_events.controllers.auth_controller import check_auth
from epic_events.controllers.contract_controller import list_contracts_controller


@click.group()
def cli_contract():
    pass


@cli_contract.command()
def create_contract():
    pass


@cli_contract.command()
def update_contract():
    pass


@cli_contract.command()
@click.option("-req", "--requester", required=True, type=str)
@check_auth
def list_contracts(auth_id, requester):
    print(list_contracts_controller(auth_id=auth_id, requester=requester))


@cli_contract.command()
def get_contract():
    pass


@cli_contract.command()
def delete_contract():
    pass
