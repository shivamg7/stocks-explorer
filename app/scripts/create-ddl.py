from sqlalchemy import create_engine
import os
from app.backend.core.models import Base

PGHOST = os.getenv("PGHOST")
PGUSER = os.getenv("PGUSER")
PGPORT = os.getenv("PGPORT")
PGPASSWORD = os.getenv("PGPASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")

engine = create_engine(f"postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{DATABASE_NAME}")

connection = engine.connect()
trans = connection.begin()
try:
    connection.execute("drop table if exists public.stocks;")
    Base.metadata.create_all(connection)
    trans.commit()
except Exception as e:
    trans.rollback()
    raise e
