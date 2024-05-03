import os
from sqlmodel import create_engine, SQLModel


sqlite_database = '../database.sqlite'

base_dir = os.path.dirname(os.path.realpath(__file__))

database_url = f"sqlite:///{os.path.join(base_dir,sqlite_database)}"

engine = create_engine(
    database_url,echo=True
)


SQLModel.metadata.create_all(engine)