import click

from controllers.auth_controller import check_auth
from controllers.user_controller import create_user_controller


@click.group()
@check_auth
def cli_user():
    pass


@cli_user.command()
@click.option("-req", "--requester", required=True, type=str)
@click.option("-n", "--name", required=True, type=str)
@click.option("-e", "--email", required=True, type=str)
@click.password_option()
@click.option("-r", "--role", required=True, type=str)
def create_user(auth_id, requester, name, email, password, role):
    print(create_user_controller(auth_id, requester, name, email, password, role))


@cli_user.command()
def update_user():
    pass


@cli_user.command()
def get_user():
    pass


@cli_user.command()
def delete_user():
    pass
