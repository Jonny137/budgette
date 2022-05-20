from datetime import datetime

EXPENSE_ENDPOINT = '/api/expense'


def test_create_new_expense(client, init_expense_types):
    exp_type_1, _ = init_expense_types
    req_body = {
        'name': 'name_1',
        'person': 'person_1',
        'amount': '100.0',
        'expense_type_name': 'type_1',
        'made_at': datetime.utcnow().isoformat()
    }
    response = client.post(f'{EXPENSE_ENDPOINT}/', json=req_body)

    assert response.status_code == 200
    assert response.json()['name'] == req_body['name']
    assert response.json()['person'] == req_body['person']
    assert response.json()['amount'] == req_body['amount']
    assert response.json()['made_at'] == req_body['made_at'] + '+02:00'
    assert response.json()['expense_type_id'] == str(exp_type_1.id)


def test_edit_expense(client, init_expenses):
    exp1, _ = init_expenses

    req_body = {
        'name': 'new_name',
        'person': 'same_cat',
        'amount': '202.2',
        'made_at': datetime.utcnow().isoformat()
    }
    response = client.put(f'{EXPENSE_ENDPOINT}/{exp1.id}', json=req_body)

    assert response.status_code == 200
    assert response.json()['name'] == req_body['name']
    assert response.json()['person'] == req_body['person']


def test_remove_expense(client, init_expenses):
    exp1, _ = init_expenses

    response = client.delete(f'{EXPENSE_ENDPOINT}/{exp1.id}')

    assert response.status_code == 200
    assert response.json()['id'] == str(exp1.id)
    assert response.json()['name'] == exp1.name
    assert response.json()['person'] == exp1.person


def test_get_expenses_by_timeframe(client, init_expenses):
    response = client.get(f'{EXPENSE_ENDPOINT}/filter')

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_balance(client, init_expenses):
    exp1, exp2 = init_expenses
    response = client.get(
        f'{EXPENSE_ENDPOINT}/monthly_balance'
        f'?name_1={exp1.person}&name_2={exp2.person}'
    )

    assert response.status_code == 200
    assert exp1.person in response.json()['persons']
    assert exp2.person in response.json()['persons']
    assert response.json()['user_diff']['name'] == exp2.person
    assert response.json()['user_diff']['difference'] == '100.0'
