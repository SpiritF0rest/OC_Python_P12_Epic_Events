from click import ClickException

from sqlalchemy import select

from epic_events.controllers.permissions_controller import has_permission
from epic_events.models import Client


@has_permission(["management", "commercial", "support"])
def list_clients_controller(session, requester, auth_id):
    if not requester:
        raise ClickException("Missing requester")
    try:
        clients = session.scalars(select(Client).order_by(Client.name)).all()
        return clients
    except Exception as e:
        raise ClickException(f"Error: {e}") from e


@has_permission(["management", "commercial", "support"])
def get_client_controller(session, requester, email, auth_id):
    if not requester and email:
        raise ClickException("Missing data in the command")
    client = session.scalar(select(Client).where(Client.email == email))
    if not client:
        raise ClickException("Sorry, this client does not exist.")
    return client
