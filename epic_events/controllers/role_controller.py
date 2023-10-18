import click
from sqlalchemy import select

from epic_events.controllers.auth_controller import check_auth
from epic_events.controllers.permissions_controller import has_permission
from epic_events.models import Role
from epic_events.views.generic_view import display_exception
from epic_events.views.role_view import display_roles_list


@click.group()
@click.pass_context
@check_auth
def role(ctx):
    ctx.ensure_object(dict)


@role.command()
@click.pass_context
@has_permission(["management"])
def list_roles(session):
    try:
        roles = session.scalars(select(Role)).all()
        return display_roles_list(roles)
    except Exception as e:
        return display_exception(e)


@role.command()
def create_role():
    pass
