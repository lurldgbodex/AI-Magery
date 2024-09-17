from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from databases import Database
from dotenv import load_dotenv
import os

if os.getenv("CI") is None:
    load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

database = Database(DATABASE_URL)
