from click import ClickException
from sqlalchemy import select

from epic_events.controllers.permissions_controller import has_permission
from epic_events.models import Role, User


@has_permission(["management"])
def create_user_controller(session, requester, name, email, password, role, auth_id):
    if not requester and name and email and password and role:
        raise ClickException("Missing data in the command")
    if session.scalar(select(User).where(User.email == email)):
        raise ClickException(f"User ({email}) already exist")
    new_user_role = session.scalar(select(Role).where(Role.name == role))
    if not new_user_role:
        raise ClickException(f"{role} is not a correct role.")
    try:
        new_user = User(name=name,
                        email=email,
                        role=new_user_role.id)
        new_user.set_password(password)
        session.add(new_user)
        session.commit()
        return f"User {email} is successfully created"
    except Exception as e:
        raise ClickException(f"Error: {e}") from e

