import uuid

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, String, DateTime

from db.base_class import Base, UtcNow


class Expense(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True,
                nullable=False, default=uuid.uuid4)
    name = Column(String, index=True)
    person = Column(String, index=True)
    amount = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=UtcNow())
    modified_at = Column(DateTime(timezone=True), onupdate=UtcNow())
    expense_type_id = Column(UUID(as_uuid=True), ForeignKey('expensetype.id'))


class ExpenseType(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True,
                nullable=False, default=uuid.uuid4)
    name = Column(String, index=True, unique=True)
    category = Column(String, nullable=True)

    expenses = relationship('Expense', backref='expensetype')
