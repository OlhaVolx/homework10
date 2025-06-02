import json
import pytest
import requests
from docutils.parsers import null
from docutils.parsers.rst.directives import body
from pytest_steps import test_steps
from requests import delete

from modules.list_methods import get_goals, create_goal,get_goal, update_goal, delete_goal
from faker import Faker
fake=Faker()

my_headers = {'Authorization':'pk_200434380_RZKCSHSPV4593XTRTU5P7UCT2RRT3FVY'}
invalid_token = {'Authorization': 'invalid_200434380_RZKCSHSPV4593XTRTU5P7UCT2RRT3FVY'}
invalid_teamId = fake.random_number(digits=11)
invalid_goal_id = fake.uuid4()

@test_steps('CRUD_Create new goal', 'CRUD_Check created goal in a goal list','CRUD_Update goal','CRUD_Delete goal','CRUD_Check deleted goal is not in a goal list')
def test_goal_lifecycle():
    create_result = create_goal()
    goal_id = create_result.json()['goal']['id']
    assert create_result.status_code == 200
    yield
    get_result=get_goals()
    goals = get_result.json()
    ids = [goal['id'] for goal in goals['goals']]
    assert get_result.status_code == 200
    yield
    assert goal_id in ids
    yield

    update_result, random_name_for_update = update_goal(goal_id)
    assert update_result.status_code == 200
    yield
    assert update_result.json()['goal']['name'] == random_name_for_update
    yield

    delete_result = delete_goal(goal_id)
    assert delete_result.status_code == 200
    yield

    get_deleted = get_goal(goal_id)
    assert get_deleted.status_code == 404
    yield

@test_steps('Check GET goals with invalid token')
def test_get_goals_with_invalid_token():
    result = requests.get('https://api.clickup.com/api/v2/team/90151218231/goal', headers=invalid_token)
    assert result.status_code == 401
    yield

@test_steps('Check CREATE goal with invalid token')
def test_create_with_invalid_token():
    random_name = fake.first_name()
    body = {
        "name": random_name
    }
    result = requests.post('https://api.clickup.com/api/v2/team/90151218231/goal', headers=invalid_token, json=body)
    assert result.status_code == 401
    yield

@test_steps('Create Goal','Check GET goal with invalid token','Delete goal')
def test_get_goal_with_invalid_token():
    create_result = create_goal()
    goal_id = create_result.json()['goal']['id']
    assert create_result.status_code == 200
    yield
    result = requests.get('https://api.clickup.com/api/v2/goal/' + goal_id, headers=invalid_token)
    assert result.status_code == 401
    yield
    delete_result = delete_goal(goal_id)
    assert delete_result.status_code == 200
    yield

@test_steps('Create Goal','UPDATE goal with invalid token','Delete goal')
def test_update_goal_with_invalid_token():
    create_result = create_goal()
    goal_id = create_result.json()['goal']['id']
    assert create_result.status_code == 200
    yield
    random_name_for_update = fake.first_name()
    body_updated = {
        "name": random_name_for_update
    }
    result = requests.put('https://api.clickup.com/api/v2/goal/' + goal_id, headers=invalid_token, json=body_updated)
    assert result.status_code == 401
    yield
    delete_result = delete_goal(goal_id)
    assert delete_result.status_code == 200
    yield

@test_steps('Create Goal','DELETE goal with invalid token','Delete goal')
def test_delete_goal_with_invalid_token():
    create_result = create_goal()
    goal_id = create_result.json()['goal']['id']
    assert create_result.status_code == 200
    yield
    result = requests.delete('https://api.clickup.com/api/v2/goal/' + goal_id, headers=invalid_token)
    assert result.status_code == 401
    yield
    delete_result = delete_goal(goal_id)
    assert delete_result.status_code == 200
    yield

@test_steps('Check GET goals with invalid team_id')
def test_get_goals_with_invalid_team_id():
    result = requests.get('https://api.clickup.com/api/v2/team/{invalid_teamId}]/goal', headers=my_headers)
    assert result.status_code == 400
    yield

@test_steps('Check CREATE goals with invalid team_id')
def test_create_goal_with_invalid_team_id():
    result = requests.post('https://api.clickup.com/api/v2/team/{invalid_teamId}]/goal', headers=my_headers)
    assert result.status_code == 400
    yield

@test_steps('Create Goal','Check GET goal with invalid goal_id','Delete goal')
def test_get_goal_with_invalid_goal_id():
    create_result = create_goal()
    goal_id = create_result.json()['goal']['id']
    assert create_result.status_code == 200
    yield
    result = requests.get('https://api.clickup.com/api/v2/goal/' + invalid_goal_id, headers=my_headers)
    assert result.status_code == 404
    yield
    delete_result = delete_goal(goal_id)
    assert delete_result.status_code == 200
    yield

@test_steps('Create Goal','UPDATE goal with invalid goal_id','Delete goal')
def test_update_goal_with_invalid_goal_id():
    create_result = create_goal()
    goal_id = create_result.json()['goal']['id']
    assert create_result.status_code == 200
    yield
    random_name_for_update = fake.first_name()
    body_updated = {
        "name": random_name_for_update
    }
    result = requests.put('https://api.clickup.com/api/v2/goal/' + invalid_goal_id, headers=my_headers, json=body_updated)
    assert result.status_code == 404
    yield
    delete_result = delete_goal(goal_id)
    assert delete_result.status_code == 200
    yield

@test_steps('Create Goal','DELETE goal with invalid goal_id','Delete goal')
def test_delete_goal_with_invalid_goal_id():
    create_result = create_goal()
    goal_id = create_result.json()['goal']['id']
    assert create_result.status_code == 200
    yield
    result = requests.delete('https://api.clickup.com/api/v2/goal/' + invalid_goal_id, headers=my_headers)
    assert result.status_code == 404
    yield
    delete_result = delete_goal(goal_id)
    assert delete_result.status_code == 200
    yield