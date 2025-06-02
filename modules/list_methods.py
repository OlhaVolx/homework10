import requests
from faker import Faker
fake=Faker()

my_headers = {'Authorization':'pk_200540491_JF747JSA50120BFLS6W7U8ETGOF9HG9V'}

def get_goals():
    return requests.get('https://api.clickup.com/api/v2/team/90151244811/goal', headers=my_headers)

def create_goal():
    random_name = fake.first_name()
    body = {
        "name": random_name
    }
    return requests.post('https://api.clickup.com/api/v2/team/90151244811/goal', headers=my_headers, json=body)

def get_goal(goal_id):
    return requests.get('https://api.clickup.com/api/v2/goal/' + goal_id, headers=my_headers)

def update_goal(goal_id):
    random_name_for_update = fake.first_name()
    body_updated = {
        "name": random_name_for_update
    }
    result = requests.put('https://api.clickup.com/api/v2/goal/' + goal_id, headers=my_headers, json=body_updated)
    return result, random_name_for_update

def delete_goal(goal_id):
    result = requests.delete('https://api.clickup.com/api/v2/goal/' + goal_id, headers=my_headers)
    return result