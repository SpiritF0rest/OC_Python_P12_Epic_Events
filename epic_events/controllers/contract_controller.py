import click
from sqlalchemy import select

from epic_events.controllers.auth_controller import check_auth
from epic_events.controllers.permissions_controller import has_permission
from epic_events.models import Contract
from epic_events.views.generic_view import display_exception


@click.group()
@click.pass_context
@check_auth
def contract(ctx):
    ctx.ensure_object(dict)


@contract.command()
@click.pass_context
@has_permission(["management", "commercial", "support"])
def list_contracts(session):
    try:
        contracts = session.scalars(select(Contract)).all()
        return contracts
    except Exception as e:
        return display_exception(e)


@contract.command()
def create_contract():
    pass


@contract.command()
def update_contract():
    pass


@contract.command()
def get_contract():
    pass


@contract.command()
def delete_contract():
    pass
