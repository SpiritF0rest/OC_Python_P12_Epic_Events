import click

from .user_controller import user
from .client_controller import client
from .contract_controller import contract
from .event_controller import event
from .role_controller import role
from .auth_controller import auth


@click.group()
def cli():
    pass


cli.add_command(user)
cli.add_command(client)
cli.add_command(contract)
cli.add_command(event)
cli.add_command(role)
cli.add_command(auth)
