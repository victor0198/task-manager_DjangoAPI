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


# DELETE TASK

def losttask(url):
    r = requests.get(url).json()
    last = (r['results'][0]['id'])
    return last


def firsttask(url):
    r = requests.get(url).json()

    alltask = (r['count'])
    last_page = math.ceil(alltask / 10)
    r = requests.get('https://tasks.devebs.net/task/?page=' + str(last_page)).json()
    for result in r['results']:
        firstid = (result['id'])
    return firstid


def test_delete_task(token, last, firstid):
    print("Deleting tasks..")
    import time
    start = time.time()
    for i in range(firstid, last + 1):
        r = requests.delete("https://tasks.devebs.net/task/delete_task/" + str(i) + "/",
                            headers={"authorization": "Bearer " + token})
    end = time.time()
    print("execution time: " + str(end - start))


rezoult_create = test_delete_task(token, losttask('https://tasks.devebs.net/task/?page=1'),
                               firsttask('https://tasks.devebs.net/task/?page=1'))
