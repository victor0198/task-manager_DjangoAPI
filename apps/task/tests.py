from rest_framework.test import APIClient

client = APIClient()
client.post('/create/', {'title': 'new idea'}, format='json')