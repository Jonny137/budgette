from uuid import UUID
from typing import Any, List
from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from dependencies import get_db
from schemas.expense import (
    ExpenseCreate, ExpenseEdit, Expense, FilterExpense, ExpenseBalance
)
from services.expense import (
    create_expense, modify_expense, remove_expense, filter_expenses,
    get_monthly_balance
)

expense_router = APIRouter()


@expense_router.post('/', response_model=Expense)
def create_new_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Create new expense.

    :param expense: Expense data
    :param db: Current database session
    :returns: Newly created expense
    """
    new_expense = create_expense(db=db, expense=expense)
    return new_expense


@expense_router.put('/{expense_id}', response_model=Expense)
def modify_existing_expense(
    expense_id: UUID,
    new_expense: ExpenseEdit,
    db: Session = Depends(get_db)
) -> Any:
    """
    Modify existing expense.

    :param new_expense: New expense data
    :param expense_id: ID of the expense which will be modified
    :param db: Current database session
    :returns: Newly updated expense
    """
    modified_expense = modify_expense(
        db=db, new_expense=new_expense, expense_id=expense_id
    )
    return modified_expense


@expense_router.delete('/{expense_id}', response_model=Expense)
def remove_existing_expense(
    expense_id: UUID,
    db: Session = Depends(get_db)
) -> Any:
    """
    Remove expense.

    :param expense_id: Expense ID
    :param db: Current database session
    :returns: Removed expense
    """
    removed_expense = remove_expense(db=db, expense_id=expense_id)
    return removed_expense


@expense_router.get('/filter', response_model=List[FilterExpense])
def get_expenses_by_timeframe(
        db: Session = Depends(get_db),
        end_time=datetime.now().isoformat(),
        start_time=datetime.today().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        ).isoformat()
) -> Any:
    """
    Filter expenses by provided timeframe. Defaults to current month.

    :param db: Current database session
    :param start_time: Start time for the filtering
    :param end_time: End time for the filtering
    :returns: List of expenses in provided timeframe
    """
    filtered_expenses = filter_expenses(
        db=db, start_time=start_time, end_time=end_time
    )
    return filtered_expenses


@expense_router.get('/monthly_balance', response_model=ExpenseBalance)
def user_monthly_balance(
    name_1: str, name_2: str, db: Session = Depends(get_db),
) -> Any:
    """
    Get two persons monthly balance and calculate who paid less for the given
    month.

    :param db: Current database session
    :param name_1: First person name
    :param name_2: Second person name
    :returns: Each person balance
    """
    user_balance = get_monthly_balance(db=db, name_1=name_1, name_2=name_2)
    return user_balance
