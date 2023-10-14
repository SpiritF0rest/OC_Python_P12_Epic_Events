from functools import wraps
from json import dump, load
from json.decoder import JSONDecodeError
from os import getenv

import click
from dotenv import load_dotenv
from jwt import encode, decode, InvalidTokenError
from sqlalchemy import select

from epic_events.database import current_session
from epic_events.models import User
from epic_events.views.auth_view import display_successful_connection, \
    display_auth_already_connected, display_invalid_token, display_auth_data_entry_error, display_not_connected_error

load_dotenv()
JWT_KEY = getenv("JWT_KEY")
TOKEN_FILE_PATH = "config.json"


@click.group()
def auth():
    pass


def verify_token(token):
    return decode(token, JWT_KEY, algorithms=["HS256"])


def get_token():
    try:
        with open(TOKEN_FILE_PATH, 'r') as f:
            data = load(f)
            return data.get('token', None)
    except JSONDecodeError:
        return None
    except FileNotFoundError:
        return None


def check_auth(function):
    @wraps(function)
    @current_session
    def wrapper(session, *args, **kwargs):
        token = get_token()
        if not token:
            return display_not_connected_error()
        try:
            auth_id = verify_token(token)
            current_user = session.scalar(select(User).where(User.id == auth_id["id"]))
            return function(session=session, current_user=current_user, *args, ** kwargs)
        except InvalidTokenError:
            return display_invalid_token()
    return wrapper


@auth.command()
@click.option("-e", "--email", required=True, type=str)
@click.password_option()
@current_session
def login(session, email, password):
    user = session.scalar(select(User).where(User.email == email))
    if not (user and user.check_password(password)):
        return display_auth_data_entry_error()
    if get_token():
        return display_auth_already_connected()
    token = encode({"id": user.id}, JWT_KEY, algorithm="HS256")
    with open(TOKEN_FILE_PATH, "w") as f:
        dump({"token": token}, f)
    return display_successful_connection()


@auth.command()
def logout():
    pass
