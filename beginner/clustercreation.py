import requests
import os
import json

API_KEY = os.getenv('ELASTIC_CLOUD_API_KEY')
HEADERS = {
    'Authorization': f'ApiKey {API_KEY}',
    'Content-Type': 'application/json'
}

# Deployment configuration
deployment_config = {
    "name": "github-actions-cluster",
    "resources": {
        "elasticsearch": [
            {
                "region": "us-west-1",
                "plan": {
                    "cluster_topology": [
                        {
                            "instance_configuration_id": "aws.data.highio.i3",
                            "size": {
                                "value": 2,
                                "resource": "memory"
                            }
                        }
                    ],
                    "elasticsearch": {
                        "version": "7.10.1"
                    }
                }
            }
        ]
    }
}

response = requests.post(
    'https://api.elastic-cloud.com/api/v1/deployments',
    headers=HEADERS,
    data=json.dumps(deployment_config)
)

response_data = response.json()
deployment_id = response_data['id']

with open('deployment_info.json', 'w') as f:
    json.dump(response_data, f)

print(f'Deployment ID: {deployment_id}')
