import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from models import Session, Message  # important for create table

# connect db
load_dotenv()

assert os.environ.get(
    "SQLALCHEMY_DATABASE_URL"
), "SQLALCHEMY_DATABASE_URL not found in .env file"

SQLALCHEMY_DATABASE_URL = os.environ.get("SQLALCHEMY_DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# create table if not exist
Base.metadata.create_all(engine)

# make session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
