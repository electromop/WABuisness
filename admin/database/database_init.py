from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from database.db_reader import db_config

engine = create_engine(
    url=db_config.database_url,
    echo=True
)

session_factory = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
