import requests
import json
import time
import random

API_ENDPOINT = "https://zl75rl3xxb.execute-api.us-east-1.amazonaws.com/prod/users"  # Replace with the URL from the stack output

def send_request(user_id, user_data):
    payload = {
        'userId': user_id,
        'userData': user_data
    }
    response = requests.post(API_ENDPOINT, json=payload)
    return response

# Inject load
for i in range(1000):
    user_id = f'user_{i}'
    user_data = {
        'name': f'User {i}',
        'age': random.randint(18, 80),
        'email': f'user{i}@example.com'
    }
    response = send_request(user_id, user_data)
    print(f"Request {i}: Status Code {response.status_code}")
    time.sleep(0.1)  # Small delay to control request rate
