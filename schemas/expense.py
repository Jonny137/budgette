from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict


class ExpenseBase(BaseModel):
    class Config:
        orm_mode = True


class ExpenseCreate(ExpenseBase):
    name: str
    person: str
    amount: str
    expense_type_name: str
    made_at: datetime
    pass


class ExpenseEdit(ExpenseBase):
    name: Optional[str]
    person: Optional[str]
    amount: Optional[str]
    made_at: Optional[datetime]
    expense_type_name: Optional[str]


class Expense(ExpenseBase):
    id: UUID
    name: str
    person: str
    amount: str
    made_at: datetime
    created_at: datetime
    modified_at: Optional[datetime]
    expense_type_id: UUID


class RelatedExpense(ExpenseBase):
    id: UUID
    name: str
    person: str
    amount: str
    created_at: datetime
    modified_at: Optional[datetime]


class FilterExpense(ExpenseBase):
    id: UUID
    name: str
    person: str
    amount: str
    made_at: datetime
    created_at: datetime
    modified_at: Optional[datetime]
    expensetype: 'Optional[ExpenseTypeResp]'


class ExpenseBalance(BaseModel):
    persons: Dict[str, str]
    user_diff: Dict[str, str]


from .expense_type import ExpenseTypeResp # noqa
RelatedExpense.update_forward_refs()
FilterExpense.update_forward_refs()
