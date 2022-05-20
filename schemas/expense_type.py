from uuid import UUID
from typing import Optional
from pydantic import BaseModel


class ExpenseTypeBase(BaseModel):
    name: str
    category: str

    class Config:
        orm_mode = True


class ExpenseTypeCreate(ExpenseTypeBase):
    pass


class ExpenseTypeEdit(ExpenseTypeBase):
    pass


class ExpenseTypeResp(ExpenseTypeBase):
    id: UUID


class ExpenseType(ExpenseTypeBase):
    id: UUID
    category: str
    expenses: 'Optional[list[RelatedExpense]]'


from .expense import RelatedExpense # noqa
ExpenseTypeResp.update_forward_refs()
ExpenseType.update_forward_refs()
