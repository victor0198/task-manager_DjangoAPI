import math

import requests
from requests.auth import HTTPBasicAuth
import requests

# Create User

def test_add_user():
    print("Creating user..")
    import time
    start = time.time()
    x =0
    for i in range(35):
        x=x+1
        payload = {
            "first_name": "test"+str(x),
            "last_name": "admintest11",
            "username": "abb"+str(x),
            "password": "123"
        }
        print(payload)
        r = requests.post("https://tasks.devebs.net/users/register/", data=payload)
        print(r.status_code)
    end = time.time()
    print("execution time: " + str(end - start))
user = test_add_user()
