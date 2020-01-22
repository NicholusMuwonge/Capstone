import os
import json
import http.client

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
TEST_PRODUCER_CLIENT_ID = os.getenv('TEST_PRODUCER_CLIENT_ID')
TEST_PRODUCER_CLIENT_SECRET = os.getenv('TEST_PRODUCER_CLIENT_SECRET')
TEST_ASSISTANT_CLIENT_ID = os.getenv('TEST_ASSISTANT_CLIENT_ID')
TEST_ASSISTANT_CLIENT_SECRET = os.getenv('TEST_ASSISTANT_CLIENT_SECRET')
TEST_DIRECTOR_CLIENT_ID = os.getenv('TEST_DIRECTOR_CLIENT_ID')
TEST_DIRECTOR_CLIENT_SECRET = os.getenv('TEST_DIRECTOR_CLIENT_SECRET')
API_AUDIENCE = os.getenv('API_AUDIENCE')


def get_token(type):
    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
    if type == 'producer':
        client_id = TEST_PRODUCER_CLIENT_ID
        client_secret = TEST_PRODUCER_CLIENT_SECRET
    elif type == 'assistant':
        client_id = TEST_ASSISTANT_CLIENT_ID
        client_secret = TEST_ASSISTANT_CLIENT_SECRET
    elif type == 'director':
        client_id = TEST_DIRECTOR_CLIENT_ID
        client_secret = TEST_DIRECTOR_CLIENT_SECRET
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'audience': API_AUDIENCE,
        'grant_type': 'client_credentials'
    }
    headers = {'content-type': 'application/json'}

    conn.request('POST', '/oauth/token', json.dumps(payload), headers)

    response = conn.getresponse()
    data = response.read()
    payload = json.loads(data.decode('utf-8'))
    return payload["access_token"]