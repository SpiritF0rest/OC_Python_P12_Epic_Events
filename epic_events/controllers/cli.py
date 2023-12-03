import click
import sentry_sdk
from sqlalchemy.exc import OperationalError

from .auth_controller import auth
from .client_controller import client
from .contract_controller import contract
from .event_controller import event
from .role_controller import role
from .user_controller import user
from ..database import current_session
from ..views.generic_view import display_exception, display_operational_error


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    try:
        ctx.obj["session"] = current_session()
    except OperationalError:
        return display_operational_error()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return display_exception(e)


cli.add_command(user)
cli.add_command(client)
cli.add_command(contract)
cli.add_command(event)
cli.add_command(role)
cli.add_command(auth)
