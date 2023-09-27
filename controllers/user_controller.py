from sqlalchemy import select
from sqlalchemy.orm import Session

from database import engine
from models import Role, User


def create_user_controller(requester, name, email, password, role):
    with Session(engine) as session:
        if not requester and name and email and password and role:
            return "Missing data in the command"
        management = session.scalar(select(Role).where(Role.name == "management"))
        try:
            user = session.scalar(select(User).where(User.email == requester))
            if management.id != user.role:
                return "Sorry, you're not authorized to create user."
            if session.scalar(select(User).where(User.email == email)):
                return f"User ({email}) already exist"
            new_user_role = session.scalar(select(Role).where(Role.name == role))
            new_user = User(name=name,
                            email=email,
                            role=new_user_role.id)
            new_user.set_password(password)

            session.add(new_user)
            session.commit()
        except AttributeError:
            print("Sorry, the email entered is not correct")
        except Exception as e:
            print(type(e), e)
