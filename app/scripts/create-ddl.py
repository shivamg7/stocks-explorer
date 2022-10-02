from app.backend.core.models import Base, Stocks
from app.backend.core.database import SessionLocal

session = SessionLocal()
try:
    session.execute(f"drop table if exists {Stocks.__tablename__} cascade;")
    Base.metadata.create_all(session.connection())
    session.commit()
except Exception as e:
    session.rollback()
    raise e
