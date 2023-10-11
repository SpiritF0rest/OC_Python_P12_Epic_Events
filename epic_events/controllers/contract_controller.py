from click import ClickException

from sqlalchemy import select

from epic_events.controllers.permissions_controller import has_permission
from epic_events.models import Contract


@has_permission(["management", "commercial", "support"])
def list_contracts_controller(session, requester, auth_id):
    if not requester:
        raise ClickException("Missing requester.")
    try:
        contracts = session.scalars(select(Contract)).all()
        return contracts
    except Exception as e:
        raise ClickException(f"Error: {e}") from e
