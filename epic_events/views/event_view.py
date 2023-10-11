import click

from epic_events.controllers.auth_controller import check_auth
from epic_events.controllers.event_controller import list_events_controller


@click.group()
def cli_event():
    pass


@cli_event.command()
def create_event():
    pass


@cli_event.command()
def update_event():
    pass


@cli_event.command()
@click.option("-req", "--requester", required=True, type=str)
@check_auth
def list_events(auth_id, requester):
    print(list_events_controller(auth_id=auth_id, requester=requester))


@cli_event.command()
def get_event():
    pass


@cli_event.command()
def delete_event():
    pass
