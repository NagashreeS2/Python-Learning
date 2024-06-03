import requests
import os
import time
import json

API_KEY = os.getenv('ELASTIC_CLOUD_API_KEY')
HEADERS = {
    'Authorization': f'ApiKey {API_KEY}',
    'Content-Type': 'application/json'
}

with open('deployment_info.json', 'r') as f:
    deployment_info = json.load(f)

deployment_id = deployment_info['id']

def check_status():
    response = requests.get(
        f'https://api.elastic-cloud.com/api/v1/deployments/{deployment_id}',
        headers=HEADERS
    )
    response_data = response.json()
    status = response_data['resources']['elasticsearch'][0]['info']['status']
    return status

print("Waiting for Elasticsearch to be ready...")
while True:
    status = check_status()
    if status == 'started':
        break
    print(f'Current status: {status}')
    time.sleep(30)

endpoint = deployment_info['resources']['elasticsearch'][0]['info']['metadata']['service_url']
credentials = deployment_info['resources']['elasticsearch'][0]['credentials']
username = credentials['username']
password = credentials['password']

with open('elasticsearch_env.sh', 'w') as f:
    f.write(f'export ELASTICSEARCH_URL={endpoint}\n')
    f.write(f'export ELASTICSEARCH_USERNAME={username}\n')
    f.write(f'export ELASTICSEARCH_PASSWORD={password}\n')
