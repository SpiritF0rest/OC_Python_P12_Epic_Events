from sqlalchemy import select

from database import current_session
from models import Role, User


@current_session
def create_user_controller(session, auth_id, requester, name, email, password, role):
    if not requester and name and email and password and role:
        return "Missing data in the command"
    management = session.scalar(select(Role).where(Role.name == "management"))
    try:
        user = session.scalar(select(User).where(User.email == requester))
        if not user:
            return "Please, verify your email."
        if management.id != user.role or user.id != auth_id["id"]:
            return "Sorry, you're not authorized to create user."
        if session.scalar(select(User).where(User.email == email)):
            return f"User ({email}) already exist"
        new_user_role = session.scalar(select(Role).where(Role.name == role))
        if not new_user_role:
            return f"{role} is not a correct role."
        new_user = User(name=name,
                        email=email,
                        role=new_user_role.id)
        new_user.set_password(password)
        session.add(new_user)
        session.commit()
        return f"User {email} is successfully created"
    except Exception as e:
        return f"{type(e)}, {e}"
