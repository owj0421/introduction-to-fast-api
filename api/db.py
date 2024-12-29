# from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# DB_URL = "mysql+pymysql://root@db:3306/demo?charset=utf8"
ASYNC_DB_URL = "mysql+aiomysql://root@db:3306/demo?charset=utf8"

# db_engine = create_engine(DB_URL)
# db_session = sessionmaker(
#     autocommit=False, 
#     autoflush=False, 
#     bind=db_engine
# )
db_engine = create_async_engine(ASYNC_DB_URL)
db_session = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=db_engine,
    class_=AsyncSession,
)

Base = declarative_base()

# def get_db():
#     session = db_session()
#     yield session
async def get_db():
    async with db_session() as session:
        yield session