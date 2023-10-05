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

load_dotenv()
JWT_KEY = getenv("JWT_KEY")
TOKEN_FILE_PATH = "token.json"


@current_session
def login_user_controller(session, email, password):
    user = session.scalar(select(User).where(User.email == email))
    if not (user and user.check_password(password)):
        return "Please, be sure to use the correct email and password."
    if get_token():
        return "You are already connected."
    token = encode({"id": user.id}, JWT_KEY, algorithm="HS256")
    with open(TOKEN_FILE_PATH, "w") as f:
        dump({"token": token}, f)
    return "Connection successful."


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
    def wrapper(*args, **kwargs):
        token = get_token()
        if not token:
            raise click.ClickException("Please log in first.")
        try:
            auth_id = verify_token(token)
            return function(auth_id, *args, ** kwargs)
        except InvalidTokenError:
            raise click.ClickException("Invalid token")
    return wrapper
