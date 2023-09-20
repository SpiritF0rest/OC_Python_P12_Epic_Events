from sqlalchemy import create_engine, URL
from dotenv import load_dotenv
from os import getenv

from models.base import Base

load_dotenv()

DB_NAME = getenv("DB_NAME")
DB_DRIVER = getenv("DB_DRIVER")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_USER = getenv("DB_USER")

url_object = URL.create(
    drivername=f"postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

# f"postgresql+{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(url_object, echo=True)

Base.metadata.create_all(engine)
