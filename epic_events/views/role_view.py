import click

from epic_events.controllers.auth_controller import check_auth
from epic_events.controllers.role_controller import list_roles_controller


@click.group()
def cli_role():
    pass


@cli_role.command()
def create_role():
    pass


@cli_role.command()
@click.option("-req", "--requester", required=True, type=str)
@check_auth
def list_roles(auth_id, requester):
    print(list_roles_controller(auth_id=auth_id, requester=requester))
