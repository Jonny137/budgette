import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, String, DateTime, Float

from db.base_class import Base, UtcNow


class Expense(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True,
                nullable=False, default=uuid.uuid4)
    name = Column(String, index=True)
    person = Column(String, index=True)
    amount = Column(Float, index=True)
    made_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=UtcNow())
    modified_at = Column(DateTime(timezone=True), onupdate=UtcNow())
    expense_type_id = Column(UUID(as_uuid=True), ForeignKey('expensetype.id'))
