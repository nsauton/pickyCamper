from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

URL_DATABASE = os.getenv("DATABASE_URL", 'postgresql://postgres:elephant@db:5432/pickyCamper')

engine = create_engine(URL_DATABASE)

SessionLocale = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()