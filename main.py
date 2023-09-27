import click

from views.user_view import cli_user
from views.client_view import cli_client
from views.contract_view import cli_contract
from views.event_view import cli_event
from views.role_view import cli_role


cli = click.CommandCollection(sources=[cli_user, cli_client, cli_contract, cli_event, cli_role])


if __name__ == "__main__":
    cli()
