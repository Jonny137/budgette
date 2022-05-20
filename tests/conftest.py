import pytest
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from sqlalchemy_utils import database_exists, create_database

from app import app
from db.base_class import Base
from dependencies import get_db
from core.config import settings

from schemas.expense import ExpenseCreate
from schemas.expense_type import ExpenseTypeCreate
from services.expense import create_expense
from services.expense_type import create_expense_type


@pytest.fixture(scope='session', autouse=True)
def db_engine():
    engine = create_engine(settings.TEST_DATABASE_URL)
    if not database_exists:
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope='function')
def db(db_engine):
    connection = db_engine.connect()

    # begin a non-ORM transaction
    connection.begin()

    # bind an individual Session to the connection
    db = Session(bind=connection)

    yield db

    db.rollback()
    connection.close()


@pytest.fixture(scope='function')
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c


@pytest.fixture
def init_expense_types(db):
    exp_type_1 = create_expense_type(
        db, ExpenseTypeCreate(name='type_1', category='cat_1')
    )
    exp_type_2 = create_expense_type(
        db, ExpenseTypeCreate(name='type_2', category='cat_2')
    )

    return exp_type_1, exp_type_2


@pytest.fixture
def init_expenses(db, init_expense_types):
    expense1 = create_expense(
        db,
        ExpenseCreate(
            name='name1',
            person='person1',
            amount='100.0',
            expense_type_name='type_1',
            made_at=datetime.utcnow().isoformat()
        )
    )
    expense2 = create_expense(
        db,
        ExpenseCreate(
            name='name2',
            person='person2',
            amount='200.0',
            expense_type_name='type_2',
            made_at=datetime.utcnow().isoformat()
        )
    )

    return expense1, expense2
