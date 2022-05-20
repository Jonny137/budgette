import uuid
import pytest
from datetime import datetime

from error_handling.exceptions import BudgetteException
from schemas.expense import ExpenseCreate, ExpenseEdit
from services.expense import (
    create_expense, expense_by_id, modify_expense, remove_expense
)


TEST_UUID = '3d50ec9e-72ac-4fff-ad42-ba39a2e9ab91'
TEST_NAME = 'SOME_TEST_NAME'


@pytest.mark.parametrize(
    'test_input,expected', [
        (
            (
                {
                    'name': 'expense1',
                    'person': 'person1',
                    'amount': '100',
                    'expense_type_name': 'type_1',
                    'made_at': '2022-05-12T09:23:54'
                }
            ),
            (
                    'expense1',
                    'person1',
                    100,
                    datetime.fromisoformat('2022-05-12T09:23:54')
            )
        )
    ]
)
def test_create_expense(db, test_input, expected, init_expense_types):
    exp_type_1, _ = init_expense_types
    expense_data = test_input
    expense = create_expense(
        db,
        ExpenseCreate(
            name=expense_data['name'],
            person=expense_data['person'],
            amount=expense_data['amount'],
            expense_type_name=expense_data['expense_type_name'],
            made_at=expense_data['made_at']
        )
    )
    assert expense.name == expected[0]
    assert expense.person == expected[1]
    assert expense.amount == expected[2]
    assert expense.expense_type_id == exp_type_1.id
    assert expense.made_at.replace(tzinfo=None) == expected[3]


@pytest.mark.parametrize(
    'test_input,expected', [
        (
            (
                {
                    'name': 'expense1',
                    'person': 'person1',
                    'amount': '100',
                    'expense_type_name': 'type_1',
                    'made_at': '2022-05-12T09:23:54'
                }
            ),
            (
                    'expense1',
                    'person1',
                    100,
                    datetime.fromisoformat('2022-05-12T09:23:54')
            )
        )
    ]
)
def test_get_expense_by_id_existing(
        db, test_input, expected, init_expense_types
):
    exp_type_1, _ = init_expense_types
    expense_data = test_input
    expense = create_expense(
        db,
        ExpenseCreate(
            name=expense_data['name'],
            person=expense_data['person'],
            amount=expense_data['amount'],
            expense_type_name=expense_data['expense_type_name'],
            made_at=expense_data['made_at']
        )
    )

    found_expense = expense_by_id(db, expense.id)

    assert found_expense.name == expected[0]
    assert found_expense.person == expected[1]
    assert found_expense.amount == expected[2]
    assert found_expense.expense_type_id == exp_type_1.id
    assert found_expense.made_at.replace(tzinfo=None) == expected[3]


def test_get_expense_by_id_wrong_uuid(db):
    with pytest.raises(BudgetteException):
        expense_by_id(db, uuid.uuid4())


@pytest.mark.parametrize(
    'test_input,expected', [
        (
            (
                {
                    'name': 'new_test_name',
                    'person': 'test_person'
                }
            ),
            ('new_test_name', 'test_person')
        )
    ]
)
def test_modify_expense(db, test_input, expected, init_expenses):
    exp1, _ = init_expenses
    exp_data = test_input

    new_exp = modify_expense(
        db,
        ExpenseEdit(
            name=exp_data['name'],
            person=exp_data['person']
        ),
        expense_id=exp1.id
    )
    assert new_exp.name == expected[0]
    assert new_exp.person == expected[1]


@pytest.mark.parametrize(
    'test_input', [
        (
            {
                'name': 'type_1',
                'person': 'person1'
            }
        )
    ]
)
def test_create_expense_type_non_existent_id(db, test_input):
    exp_data = test_input

    with pytest.raises(BudgetteException):
        modify_expense(
            db,
            ExpenseEdit(
                name=exp_data['name'],
                person=exp_data['person']
            ),
            expense_id=uuid.uuid4()
        )


def test_remove_expense(db, init_expenses):
    exp1, _ = init_expenses
    removed_exp = remove_expense(db, exp1.id)

    assert removed_exp.name == exp1.name
    assert removed_exp.person == exp1.person


def test_remove_expense_non_existent_id(db, init_expenses):
    with pytest.raises(BudgetteException):
        remove_expense(db, uuid.uuid4())
