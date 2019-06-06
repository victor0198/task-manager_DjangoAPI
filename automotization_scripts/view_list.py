import math

import requests
from requests.auth import HTTPBasicAuth
import requests


def token(url):
    values = {'username': 'admintest',
              'password': '123'}

    r = requests.post(url, data=values)
    data = r.json()
    return data["access"]


token = token('https://tasks.devebs.net/users/token/')


# View List Task
def test_list(token):
    print("List tasks..")

    cycles = 10
    show = True
    import time
    start = time.time()

    while show and cycles >= 0:
        cycles = cycles - 1
        r = requests.get("https://tasks.devebs.net/task/?page=1",
                         headers={'content-type': 'application/json', "authorization": "Bearer " + token})
        if r.json()['count'] == 0:
            show = False
    end = time.time()
    print("execution time: " + str(end - start))

rezoul_test_list = test_list(token)
