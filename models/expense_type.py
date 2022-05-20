import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from db.base_class import Base


class ExpenseType(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True,
                nullable=False, default=uuid.uuid4)
    name = Column(String, index=True, unique=True)
    category = Column(String, nullable=True)

    expenses = relationship('Expense', backref='expensetype')
