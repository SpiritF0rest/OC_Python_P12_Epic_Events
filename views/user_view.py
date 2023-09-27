import click

from controllers.user_controller import create_user_controller


@click.group()
def cli_user():
    pass


@cli_user.command()
@click.option("-req", "--requester", required=True, type=str)
@click.option("-n", "--name", required=True, type=str)
@click.option("-e", "--email", required=True, type=str)
@click.option("-p", "--password", required=True, type=str)
@click.option("-r", "--role", required=True, type=str)
def create_user(requester, name, email, password, role):
    create_user_controller(requester, name, email, password, role)


@cli_user.command()
def update_user():
    pass


@cli_user.command()
def get_user():
    pass


@cli_user.command()
def delete_user():
    pass
