from uuid import UUID
from typing import Any, List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from dependencies import get_db
from schemas.expense_type import (
    ExpenseTypeResp, ExpenseTypeCreate, ExpenseType, ExpenseTypeEdit
)
from services.expense_type import (
    create_expense_type, expense_type_by_id, get_all_expense_types,
    edit_expense_type, remove_expense_type
)

exp_type_router = APIRouter()


@exp_type_router.post('/', response_model=ExpenseTypeResp)
def create_new_expense_type(
    expense_type: ExpenseTypeCreate,
    db: Session = Depends(get_db),
) -> Any:
    """
    Create new expense type.

    :param expense_type: Expense type schema with name and category fields
    :param db: Current database session
    :returns: Newly created expense type
    """
    new_expense_type = create_expense_type(db=db, expense_type=expense_type)
    return new_expense_type


@exp_type_router.get('/all', response_model=List[ExpenseType])
def fetch_all_expense_types(db: Session = Depends(get_db)) -> Any:
    """
    Fetch all expense types.

    :param db: Current database session
    :returns: Newly created expense type
    """
    expense_types = get_all_expense_types(db=db)
    return expense_types


@exp_type_router.get('/{expense_type_id}', response_model=ExpenseType)
def fetch_expense_type_by_id(
    expense_type_id: UUID,
    db: Session = Depends(get_db)
) -> Any:
    """
    Fetch expense type by ID.

    :param expense_type_id: Expense type UUID
    :param db: Current database session
    :returns: Newly created expense type
    """
    expense_type = expense_type_by_id(db=db, expense_type_id=expense_type_id)
    return expense_type


@exp_type_router.put('/{expense_type_id}', response_model=ExpenseTypeResp)
def edit_existing_expense_type(
        expense_type_id: UUID,
        new_expense_type: ExpenseTypeEdit,
        db: Session = Depends(get_db)
) -> Any:
    """
    Edit expense type data.

    :param db: Current database session
    :param expense_type_id: Expense type ID which will be updated
    :param new_expense_type: Expense type params for the updating
    :returns: Updated expense type
    """
    edited_expense_type = edit_expense_type(
        db=db, new_expense_type=new_expense_type,
        expense_type_id=expense_type_id
    )
    return edited_expense_type


@exp_type_router.delete('/{expense_type_id}', response_model=ExpenseTypeResp)
def remove_existing_expense_type(
    expense_type_id: UUID,
    db: Session = Depends(get_db)
) -> Any:
    """
    Remove expense type.

    :param expense_type_id: Expense type UUID
    :param db: Current database session
    :returns: Removed expense type
    """
    expense_type = remove_expense_type(db=db, expense_type_id=expense_type_id)
    return expense_type
