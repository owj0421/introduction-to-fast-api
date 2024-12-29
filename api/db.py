from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL = "mysql+pymysql://root@db:3306/demo?charset=utf8"

db_engine = create_engine(DB_URL)
db_session = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=db_engine
)

Base = declarative_base()

def get_db():
    session = db_session()
    try:
        yield session
    finally:
        session.close()