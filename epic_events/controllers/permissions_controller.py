from functools import wraps

from sqlalchemy import select

from epic_events.controllers.auth_controller import check_auth
from epic_events.models import Role
from epic_events.views.permissions_view import display_not_authorized


def has_permission(roles):
    def decorator(function):
        @wraps(function)
        @check_auth
        def wrapper(session, current_user, *args, **kwargs):
            selected_roles = [session.scalar(select(Role.id).where(Role.name == role)) for role in roles]
            if current_user.role not in selected_roles:
                return display_not_authorized()
            return function(session, *args, **kwargs)
        return wrapper
    return decorator
