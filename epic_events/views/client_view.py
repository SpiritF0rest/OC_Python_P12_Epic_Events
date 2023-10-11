import click

from epic_events.controllers.auth_controller import check_auth
from epic_events.controllers.client_controller import list_clients_controller, get_client_controller


@click.group()
def cli_client():
    pass


@cli_client.command()
def create_client():
    pass


@cli_client.command()
def update_client():
    pass


@cli_client.command()
@click.option("-req", "--requester", required=True, type=str)
@check_auth
def list_clients(auth_id, requester):
    print(list_clients_controller(auth_id=auth_id, requester=requester))


@cli_client.command()
@click.option("-req", "--requester", required=True, type=str)
@click.option("-n", "--name", required=True, type=str)
@check_auth
def get_client(auth_id, requester, name):
    print(get_client_controller(auth_id=auth_id, requester=requester, name=name))


@cli_client.command()
def delete_client():
    pass
