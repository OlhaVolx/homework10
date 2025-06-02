import requests
from faker import Faker
fake=Faker()

my_headers = {'Authorization':'pk_200434380_RZKCSHSPV4593XTRTU5P7UCT2RRT3FVY'}

def get_goals():
    return requests.get('https://api.clickup.com/api/v2/team/90151218231/goal', headers=my_headers)

def create_goal():
    random_name = fake.first_name()
    body = {
        "name": random_name
    }
    return requests.post('https://api.clickup.com/api/v2/team/90151218231/goal', headers=my_headers, json=body)

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