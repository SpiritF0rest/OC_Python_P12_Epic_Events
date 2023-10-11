import click

from epic_events.controllers.auth_controller import check_auth
from epic_events.controllers.user_controller import create_user_controller


@click.group()
def cli_user():
    pass


@cli_user.command()
@click.option("-req", "--requester", required=True, type=str)
@click.option("-n", "--name", required=True, type=str)
@click.option("-e", "--email", required=True, type=str)
@click.password_option()
@click.option("-r", "--role", required=True, type=str)
@check_auth
def create_user(auth_id, requester, name, email, password, role):
    print(create_user_controller(name=name, email=email, password=password,
                                 role=role, requester=requester, auth_id=auth_id))


@cli_user.command()
def update_user():
    pass


@cli_user.command()
def get_user():
    pass


@cli_user.command()
def delete_user():
    pass
