from click import ClickException

from sqlalchemy import select

from epic_events.controllers.permissions_controller import has_permission
from epic_events.models import Role


@has_permission(["management"])
def list_roles_controller(session, requester, auth_id):
    if not requester:
        raise ClickException("Missing requester.")
    try:
        roles = session.scalars(select(Role)).all()
        return roles
    except Exception as e:
        raise ClickException(f"Error: {e}") from e
