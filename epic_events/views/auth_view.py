import click

from epic_events.controllers.auth_controller import login_user_controller


@click.group()
def cli_auth():
    pass


@cli_auth.command()
@click.option("-e", "--email", required=True, type=str)
@click.password_option()
def login_user(email, password):
    print(login_user_controller(email, password))


@cli_auth.command()
def logout_user():
    pass
