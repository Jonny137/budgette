EXPENSE_TYPE_ENDPOINT = '/api/expense_type'
TEST_UUID = '3d50ec9e-72ac-4fff-ad42-ba39a2e9ab91'


def test_get_all_expense_types(client, init_expense_types):
    response = client.get(f'{EXPENSE_TYPE_ENDPOINT}/all')

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_all_expense_types_no_results(client):
    response = client.get(f'{EXPENSE_TYPE_ENDPOINT}/all')

    assert response.status_code == 200
    assert len(response.json()) == 0


def test_create_new_expense_type(client):
    req_body = {
        'name': 'expense_type',
        'category': 'some_cat'
    }
    response = client.post(f'{EXPENSE_TYPE_ENDPOINT}/', json=req_body)

    assert response.status_code == 200
    assert response.json()['name'] == req_body['name']
    assert response.json()['category'] == req_body['category']


def test_create_same_name_expense_type(client, init_expense_types):
    req_body = {
        'name': 'type_1',
        'category': 'some_cat'
    }
    response = client.post(f'{EXPENSE_TYPE_ENDPOINT}/', json=req_body)

    assert response.status_code == 400


def test_get_expense_type_by_id(client, init_expense_types):
    exp1, exp2 = init_expense_types

    response = client.get(f'{EXPENSE_TYPE_ENDPOINT}/{exp1.id}')

    assert response.status_code == 200
    assert response.json()['id'] == str(exp1.id)
    assert response.json()['name'] == exp1.name
    assert response.json()['category'] == exp1.category


def test_get_expense_type_by_id_non_existent(client, init_expense_types):
    response = client.get(f'{EXPENSE_TYPE_ENDPOINT}/{TEST_UUID}')

    assert response.status_code == 404


def test_edit_expense_type(client, init_expense_types):
    exp1, exp2 = init_expense_types

    req_body = {
        'name': 'new_exp_type_name',
        'category': 'same_cat'
    }
    response = client.put(f'{EXPENSE_TYPE_ENDPOINT}/{exp1.id}', json=req_body)

    assert response.status_code == 200
    assert response.json()['name'] == req_body['name']
    assert response.json()['category'] == req_body['category']


def test_edit_expense_type_non_existent(client, init_expense_types):
    req_body = {
        'name': 'new_exp_type_name',
        'category': 'same_cat'
    }
    response = client.put(
        f'{EXPENSE_TYPE_ENDPOINT}/{TEST_UUID}', json=req_body
    )

    assert response.status_code == 404


def test_edit_expense_type_missing_name(client, init_expense_types):
    req_body = {
        'category': 'same_cat'
    }
    response = client.put(
        f'{EXPENSE_TYPE_ENDPOINT}/{TEST_UUID}', json=req_body
    )

    assert response.status_code == 422


def test_edit_expense_type_missing_category(client, init_expense_types):
    req_body = {
        'name': 'new_exp_type_name'
    }
    response = client.put(
        f'{EXPENSE_TYPE_ENDPOINT}/{TEST_UUID}', json=req_body
    )

    assert response.status_code == 422


def test_remove_expense_type(client, init_expense_types):
    exp1, exp2 = init_expense_types

    response = client.delete(f'{EXPENSE_TYPE_ENDPOINT}/{exp1.id}')

    assert response.status_code == 200
    assert response.json()['id'] == str(exp1.id)
    assert response.json()['name'] == exp1.name
    assert response.json()['category'] == exp1.category


def test_remove_expense_type_non_existent(client, init_expense_types):
    response = client.delete(f'{EXPENSE_TYPE_ENDPOINT}/{TEST_UUID}')

    assert response.status_code == 404
