from functools import wraps

from click import ClickException
from sqlalchemy import select

from epic_events.database import current_session
from epic_events.models import User, Role


def has_permission(role):
    @current_session
    def decorator(session, function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            auth_id = kwargs.get("auth_id")
            if auth_id is None:
                raise ClickException("Are you properly authenticated ?")
            user_email = kwargs.get("requester")
            if user_email is None:
                raise ClickException("Missing requester.")
            user = session.scalar(select(User).where(User.email == user_email))
            if not user:
                raise ClickException("Please, verify your email.")
            selected_role = session.scalar(select(Role).where(Role.name == role))
            if user.role != selected_role.id or user.id != auth_id["id"]:
                raise ClickException("Sorry, you're not authorized.")
            return function(session, *args, **kwargs)
        return wrapper
    return decorator
