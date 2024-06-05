import requests
import json
import os

def create_cluster():
    # Read the Elastic Cloud API endpoint and API key from environment variables
    elastic_cloud_api_endpoint = os.getenv("ELASTICCLOUD_API_ENDPOINT")
    elastic_cloud_api_key = os.getenv("ELASTICCLOUD_API_KEY")

    # Define the Elasticsearch cluster configuration
    cluster_config = {
        {
            
        }
    }

    # Send a request to create the cluster
    response = requests.post(elastic_cloud_api_endpoint + "/api/v1/deployments", 
                             headers={"Authorization": f"ApiKey {elasticcloud_api_key}"}, 
                             json=cluster_config)

    # Print the response
    print(response.text)

if __name__ == "__main__":
    create_cluster()