import click
from sqlalchemy import select

from epic_events.controllers.permissions_controller import has_permission
from epic_events.models import Client
from epic_events.views.client_view import display_missing_data, display_unknown_client, display_client_data, \
    display_clients_list
from epic_events.views.generic_view import display_exception


@click.group()
def client():
    pass


@client.command()
@has_permission(["management", "commercial", "support"])
def list_clients(session):
    try:
        clients = session.scalars(select(Client).order_by(Client.name)).all()
        return display_clients_list(clients)
    except Exception as e:
        return display_exception(e)


@client.command()
@click.option("-id", "--client_id", required=True, type=int)
@has_permission(["management", "commercial", "support"])
def get_client(session, client_id):
    if not client_id:
        return display_missing_data()
    selected_client = session.scalar(select(Client).where(Client.id == client_id))
    if not selected_client:
        return display_unknown_client()
    return display_client_data(selected_client)


@client.command()
def create_client():
    pass


@client.command()
def update_client():
    pass


@client.command()
def delete_client():
    pass
