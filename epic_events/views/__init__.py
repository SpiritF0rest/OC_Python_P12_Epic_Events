import click

from .user_view import cli_user
from .client_view import cli_client
from .contract_view import cli_contract
from .event_view import cli_event
from .role_view import cli_role
from .auth_view import cli_auth


@click.group()
def cli():
    pass


cli.add_command(cli_user)
cli.add_command(cli_client)
cli.add_command(cli_contract)
cli.add_command(cli_event)
cli.add_command(cli_role)
cli.add_command(cli_auth)
