import math

import requests
from requests.auth import HTTPBasicAuth
import requests


def token(url):
    values = {'username': 'eugene',
              'password': 'eugene'}

    r = requests.post(url, data=values)
    data = r.json()
    return data["access"]


token = token('https://tasks.devebs.net/users/token/')


# Create Task

def test_add_task(token):
    print("Creating tasks..")
    import time
    start = time.time()
    for i in range(5):
        payload = {'title': 'TestTitle',
                   'description': 'Test1Description',
                   'status': 'created',
                   'user_assigned': 1,
                   'date_create_task': "2019-05-24T12:34:56.139Z"}

        r = requests.post("https://tasks.devebs.net/tasks/create", data=payload,
                          headers={"authorization": "Bearer " + token})
    end = time.time()
    print("execution time: " + str(end - start))


