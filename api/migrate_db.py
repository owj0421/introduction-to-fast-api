from sqlalchemy import create_engine

from api.models.task import Base

DB_URL = "mysql+pymysql://root@db:3306/demo?charset=utf8"

db_engine = create_engine(DB_URL, echo=True)

def reset_db():
    Base.metadata.drop_all(db_engine)
    Base.metadata.create_all(db_engine)
    
if __name__ == "__main__":
    reset_db()