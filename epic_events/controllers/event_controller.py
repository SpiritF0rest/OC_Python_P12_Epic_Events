from click import ClickException

from sqlalchemy import select

from epic_events.controllers.permissions_controller import has_permission
from epic_events.models import Event


@has_permission(["management", "commercial", "support"])
def list_events_controller(session, requester, auth_id):
    if not requester:
        raise ClickException("Missing requester.")
    try:
        events = session.scalars(select(Event)).all()
        return events
    except Exception as e:
        raise ClickException(f"Error: {e}") from e
