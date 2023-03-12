from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import BYTEA

from app.database import Base


class Record(Base):
    __tablename__ = "records"

    key = Column(String, primary_key=True, index=True, unique=True)
    value = Column(BYTEA)

    def __repr__(self):
        return f"Record(key={self.key}, value={self.value})"
