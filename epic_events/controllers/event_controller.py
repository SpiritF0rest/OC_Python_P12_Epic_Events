import click
from sqlalchemy import select

from epic_events.controllers.permissions_controller import has_permission
from epic_events.models import Event
from epic_events.views.event_view import display_events_list
from epic_events.views.generic_view import display_exception


@click.group()
def event():
    pass


@event.command()
@has_permission(["management", "commercial", "support"])
def list_events(session):
    try:
        events = session.scalars(select(Event)).all()
        return display_events_list(events)
    except Exception as e:
        return display_exception(e)


@event.command()
def create_event():
    pass


@event.command()
def update_event():
    pass


@event.command()
def get_event():
    pass


@event.command()
def delete_event():
    pass
