from .orm import Base
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func


class TableWithDate(Base):
    __abstract__ = True

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
