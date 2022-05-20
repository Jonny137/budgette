import uuid
import pytest

from error_handling.exceptions import BudgetteException
from schemas.expense_type import ExpenseTypeCreate, ExpenseTypeEdit
from services.expense_type import (
    create_expense_type, expense_type_by_id, expense_type_by_name,
    get_all_expense_types, edit_expense_type, remove_expense_type
)


TEST_NAME = 'SOME_TEST_NAME'


@pytest.mark.parametrize(
    'test_input,expected', [
        (
            (
                {
                    'name': 'test_name',
                    'category': 'test_category'
                }
            ),
            ('test_name', 'test_category')
        )
    ]
)
def test_create_expense_type(db, test_input, expected):
    exp_type_data = test_input
    new_exp_type = create_expense_type(
        db,
        ExpenseTypeCreate(
            name=exp_type_data['name'],
            category=exp_type_data['category']
        )
    )
    assert new_exp_type.name == expected[0]
    assert new_exp_type.category == expected[1]


@pytest.mark.parametrize(
    'test_input', [
        (
            {
                'name': 'type_1',
                'category': 'test_category'
            }
        )
    ]
)
def test_create_expense_type_existing(db, test_input, init_expense_types):
    exp_type_data = test_input

    with pytest.raises(BudgetteException):
        create_expense_type(
            db, ExpenseTypeCreate(
                name=exp_type_data['name'], category=exp_type_data['category']
            )
        )


@pytest.mark.parametrize(
    'expected', [
        (
            (
                {
                    'name': 'type_1',
                    'category': 'cat_1'
                }
            )
        )
    ]
)
def test_get_expense_type_by_id(db, expected, init_expense_types):
    exp1, _ = init_expense_types

    expense_type = expense_type_by_id(db, exp1.id)

    assert expense_type.id == exp1.id
    assert expense_type.name == expected['name']
    assert expense_type.category == expected['category']


def test_get_expense_type_by_id_wrong_uuid(db, init_expense_types):
    with pytest.raises(BudgetteException):
        expense_type_by_id(db, uuid.uuid4())


@pytest.mark.parametrize(
    'expected', [
        (
            (
                {
                    'name': 'type_1',
                    'category': 'cat_1'
                }
            )
        )
    ]
)
def test_get_expense_type_by_name(db, expected, init_expense_types):
    exp1, _ = init_expense_types

    expense_type = expense_type_by_name(db, exp1.name)

    assert expense_type.id == exp1.id
    assert expense_type.name == expected['name']
    assert expense_type.category == expected['category']


def test_get_expense_type_by_name_wrong_name(db, init_expense_types):
    with pytest.raises(BudgetteException):
        expense_type_by_name(db, TEST_NAME)


@pytest.mark.parametrize(
    'expected', [
        (
            (
                2
            )
        )
    ]
)
def test_get_expense_type_all(db, expected, init_expense_types):
    expense_types = get_all_expense_types(db)

    assert len(expense_types) == expected


@pytest.mark.parametrize(
    'expected', [
        (
            (
                0
            )
        )
    ]
)
def test_get_expense_type_by_all_no_results(db, expected):
    expense_types = get_all_expense_types(db)

    assert len(expense_types) == expected


@pytest.mark.parametrize(
    'test_input,expected', [
        (
            (
                {
                    'name': 'new_test_name',
                    'category': 'test_category'
                }
            ),
            ('new_test_name', 'test_category')
        )
    ]
)
def test_edit_expense_type(db, test_input, expected, init_expense_types):
    exp1, _ = init_expense_types
    exp_type_data = test_input

    new_exp_type = edit_expense_type(
        db, ExpenseTypeEdit(
            name=exp_type_data['name'],
            category=exp_type_data['category']
        ),
        expense_type_id=exp1.id
    )
    assert new_exp_type.name == expected[0]
    assert new_exp_type.category == expected[1]


@pytest.mark.parametrize(
    'test_input', [
        (
            {
                'name': 'type_1',
                'category': 'test_category'
            }
        )
    ]
)
def test_edit_expense_type_non_existent_id(db, test_input):
    exp_type_data = test_input

    with pytest.raises(BudgetteException):
        edit_expense_type(
            db, ExpenseTypeEdit(
                name=exp_type_data['name'],
                category=exp_type_data['category']
            ),
            expense_type_id=uuid.uuid4()
        )


@pytest.mark.parametrize(
    'expected', [
        (
            (
                1
            )
        )
    ]
)
def test_remove_expense_type(db, expected, init_expense_types):
    exp1, _ = init_expense_types
    removed_exp = remove_expense_type(db, exp1.id)

    assert removed_exp.name == exp1.name
    assert removed_exp.category == exp1.category
    assert len(get_all_expense_types(db)) == expected


def test_remove_expense_type_non_existent_id(db, init_expense_types):
    with pytest.raises(BudgetteException):
        remove_expense_type(db, uuid.uuid4())
