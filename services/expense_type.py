import logging
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from error_handling.exceptions import BudgetteException

from models.expense_type import ExpenseType
from schemas.expense_type import ExpenseTypeCreate, ExpenseTypeEdit

logger = logging.getLogger(__name__)


def create_expense_type(db: Session, expense_type: ExpenseTypeCreate):
    try:
        new_expense_type = ExpenseType(**expense_type.dict())
        db.add(new_expense_type)
        db.commit()
        db.refresh(new_expense_type)
    except IntegrityError:
        db.rollback()
        raise BudgetteException(status_code=400, message='Duplicate entry.')

    return new_expense_type


def expense_type_by_id(db: Session, expense_type_id: UUID):
    expense_type = db.query(ExpenseType).filter(
        ExpenseType.id == expense_type_id
    ).first()
    if not expense_type:
        raise BudgetteException(
            status_code=404, message='Non existent expense type.'
        )

    return expense_type


def expense_type_by_name(db: Session, name: str):
    expense_type = db.query(ExpenseType).filter(
        ExpenseType.name == name
    ).first()
    if not expense_type:
        raise BudgetteException(
            status_code=404, message='Non existent expense type.'
        )

    return expense_type


def get_all_expense_types(db: Session):
    return db.query(ExpenseType).all()


def edit_expense_type(
        db: Session, new_expense_type: ExpenseTypeEdit, expense_type_id: UUID
):
    expense_type = expense_type_by_id(db, expense_type_id)
    expense_type.name = new_expense_type.name
    expense_type.category = new_expense_type.category
    db.commit()

    return expense_type


def remove_expense_type(db: Session, expense_type_id: UUID):
    expense_type = expense_type_by_id(db, expense_type_id)
    removed_expense_type = expense_type
    db.delete(expense_type)
    db.commit()

    return removed_expense_type
