from datetime import datetime, timezone, timedelta
from functools import wraps
from json import dump, load
from json.decoder import JSONDecodeError
from os import getenv

import click
import sentry_sdk
from dotenv import load_dotenv
from jwt import encode, decode, InvalidTokenError, ExpiredSignatureError
from sqlalchemy import select

from epic_events.models import User
from epic_events.views.auth_view import (display_successful_connection, display_auth_already_connected,
                                         display_invalid_token, display_auth_data_entry_error,
                                         display_not_connected_error, display_expired_token)

load_dotenv()
JWT_KEY = getenv("JWT_KEY")
TOKEN_FILE_PATH = "config.json"


def delete_token():
    with open(TOKEN_FILE_PATH, "r") as f:
        data = load(f)
        del data["token"]
    with open(TOKEN_FILE_PATH, "w") as f:
        dump(data, f)


@click.group()
@click.pass_context
def auth(ctx):
    ctx.ensure_object(dict)


def verify_token(token):
    return decode(token, JWT_KEY, algorithms=["HS256"])


def get_token():
    try:
        with open(TOKEN_FILE_PATH, 'r') as f:
            data = load(f)
            return data.get('token', None)
    except JSONDecodeError as e:
        # Send a message via sentry to notify the json error
        with sentry_sdk.push_scope() as scope:
            scope.set_tag("json-error", "decode error")
            sentry_sdk.capture_exception(e)
        return None
    except FileNotFoundError:
        return None
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return None


def check_auth(function):
    @wraps(function)
    def wrapper(ctx, *args, **kwargs):
        session = ctx.obj["session"]
        token = get_token()
        if not token:
            return display_not_connected_error()
        try:
            auth_id = verify_token(token)
            current_user = session.scalar(select(User).where(User.id == auth_id["id"]))
            ctx.obj["current_user"] = current_user
            return function(ctx, *args, ** kwargs)
        except ExpiredSignatureError:
            delete_token()
            return display_expired_token()
        except InvalidTokenError as e:
            # Send a message via sentry to notify the token error
            with sentry_sdk.push_scope() as scope:
                scope.set_tag("token-error", "invalid")
                sentry_sdk.capture_exception(e)
            return display_invalid_token()
    return wrapper


@auth.command()
@click.option("-e", "--email", required=True, type=str)
@click.password_option()
@click.pass_context
def login(ctx, email, password):
    session = ctx.obj["session"]
    user = session.scalar(select(User).where(User.email == email))

    if not (user and user.check_password(password)):
        return display_auth_data_entry_error()
    if get_token():
        return display_auth_already_connected()

    token = encode({"id": user.id, "exp": datetime.now(tz=timezone.utc) + timedelta(hours=12)},
                   JWT_KEY, algorithm="HS256")
    with open(TOKEN_FILE_PATH, "w") as f:
        dump({"token": token}, f)
    return display_successful_connection(login=True)


@auth.command()
@click.confirmation_option(prompt="Are you sure you want to logout?")
def logout():
    delete_token()
    return display_successful_connection(login=False)
