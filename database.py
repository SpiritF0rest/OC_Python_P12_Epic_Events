from sqlalchemy import create_engine, URL, select
from dotenv import load_dotenv
from os import getenv

from sqlalchemy.orm import Session

from models import Role, User
from models.base import Base

load_dotenv()

DB_NAME = getenv("DB_NAME")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_USER = getenv("DB_USER")
FIRST_USER_PASSWORD = getenv("FIRST_USER_PASSWORD")

url_object = URL.create(
    drivername=f"postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

# f"postgresql+{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(url_object)

Base.metadata.create_all(engine)


def current_session(function):
    def wrapper(*args, **kwargs):
        with Session(engine) as session:
            return function(session, *args, **kwargs)
    return wrapper


@current_session
def insert_initial_data(session):
    commercial = Role(name="commercial")
    support = Role(name="support")
    management = Role(name="management")

    session.add_all([commercial, support, management])
    session.commit()

    role = session.scalar(select(Role).where(Role.name == "management"))
    first_user = User(name="first manager", email="first_manager@epicevents.com", role=role.id)
    first_user.set_password(FIRST_USER_PASSWORD)

    session.add(first_user)
    session.commit()


if __name__ == "__main__":
    insert_initial_data()
