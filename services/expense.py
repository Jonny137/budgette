import logging
from uuid import UUID
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from error_handling.exceptions import BudgetteException

from models.expense import Expense
from schemas.expense import ExpenseCreate, ExpenseEdit
from services.expense_type import expense_type_by_name

logger = logging.getLogger(__name__)


def create_expense(db: Session, expense: ExpenseCreate):
    try:
        new_expense = Expense(
            name=expense.name, person=expense.person,
            amount=expense.amount, made_at=expense.made_at
        )
        existing_expense_type = expense_type_by_name(
            db, expense.expense_type_name
        )
        new_expense.expense_type_id = existing_expense_type.id
        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)
    except IntegrityError:
        db.rollback()
        raise BudgetteException(status_code=400, message='Duplicate entry.')

    return new_expense


def expense_by_id(db: Session, expense_id: UUID):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise BudgetteException(
            status_code=404, message='Non existent expense.'
        )

    return expense


def modify_expense(
        db: Session, new_expense: ExpenseEdit, expense_id: UUID
):
    expense = expense_by_id(db, expense_id)

    if new_expense.expense_type_name:
        existing_expense_type = expense_type_by_name(
            db, new_expense.expense_type_name
        )
        expense.expense_type_id = existing_expense_type.id

    for key, value in new_expense.dict().items():
        setattr(expense, key, value)

    db.commit()

    return expense


def remove_expense(db: Session, expense_id: UUID):
    expense_type = expense_by_id(db, expense_id)
    removed_expense_type = expense_type
    db.delete(expense_type)
    db.commit()

    return removed_expense_type


def filter_expenses(db: Session, start_time: str, end_time: str):
    expenses = db.query(Expense).filter(
        Expense.made_at.between(start_time, end_time)
    ).all()

    return expenses


def get_monthly_balance(db: Session, name_1: str, name_2: str):
    end_time = datetime.now().isoformat(),
    start_time = datetime.today().replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    ).isoformat()

    expenses = filter_expenses(db, start_time, str(end_time))

    user_balance = {
        'persons': {
            name_1: 0,
            name_2: 0
        }
    }
    for expense in expenses:
        if expense.person in [name_1, name_2]:
            user_balance['persons'][expense.person] += expense.amount

    person_one = user_balance['persons'][name_1]
    person_two = user_balance['persons'][name_2]
    name = name_1 if person_one > person_two else name_2
    difference = abs(person_one - person_two)

    user_balance['user_diff'] = {
        'name': name,
        'difference': difference
    }

    return user_balance
