import click
from sqlalchemy import select

from epic_events.controllers.auth_controller import check_auth
from epic_events.controllers.permissions_controller import has_permission
from epic_events.models import Event
from epic_events.views.event_view import display_events_list
from epic_events.views.generic_view import display_exception


@click.group()
@click.pass_context
@check_auth
def event(ctx):
    ctx.ensure_object(dict)


@event.command(name="list")
@click.pass_context
@has_permission(["management", "commercial", "support"])
def list_events(session):
    try:
        events = session.scalars(select(Event)).all()
        return display_events_list(events)
    except Exception as e:
        return display_exception(e)


@event.command(name="create")
def create_event():
    pass


@event.command(name="update")
def update_event():
    pass


@event.command(name="get")
def get_event():
    pass


@event.command(name="delete")
def delete_event():
    pass
