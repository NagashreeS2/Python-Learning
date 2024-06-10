import requests
import json
import os
#import urllib3

# Disable SSL certificate verification
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

elasticloud_api_endpoint = os.getenv('ELASTICLOUD_API_ENDPOINT')
elasticloud_api_key = os.getenv('ELASTICLOUD_API_KEY')

def create_cluster():
    # Define the Elasticsearch cluster configuration
    cluster_config = {
        "resources": {
            "elasticsearch": [
                {
                    "region": "azure-eastus2",
                    "ref_id": "main-elasticsearch",
                    "plan": {
                        "cluster_topology": [
                            {
                                "zone_count": 1,
                                "elasticsearch": {
                                    "node_attributes": {
                                        "data": "hot"
                                    }
                                },
                                "instance_configuration_id": "azure.es.datahot.edsv4",
                                "node_roles": [
                                    "master",
                                    "ingest",
                                    "transform",
                                    "data_hot",
                                    "remote_cluster_client",
                                    "data_content"
                                ],
                                "id": "hot_content",
                                "size": {
                                    "value": 4096,
                                    "resource": "memory"
                                }
                            },
                            {
                                "zone_count": 2,
                                "elasticsearch": {
                                    "node_attributes": {
                                        "data": "warm"
                                    }
                                },
                                "instance_configuration_id": "azure.es.datawarm.edsv4",
                                "node_roles": [
                                    "data_warm",
                                    "remote_cluster_client"
                                ],
                                "id": "warm",
                                "size": {
                                    "resource": "memory",
                                    "value": 0
                                }
                            },
                            {
                                "zone_count": 1,
                                "elasticsearch": {
                                    "node_attributes": {
                                        "data": "cold"
                                    }
                                },
                                "instance_configuration_id": "azure.es.datacold.edsv4",
                                "node_roles": [
                                    "data_cold",
                                    "remote_cluster_client"
                                ],
                                "id": "cold",
                                "size": {
                                    "resource": "memory",
                                    "value": 0
                                }
                            },
                            {
                                "zone_count": 1,
                                "elasticsearch": {
                                    "node_attributes": {
                                        "data": "frozen"
                                    }
                                },
                                "instance_configuration_id": "azure.es.datafrozen.edsv4",
                                "node_roles": [
                                    "data_frozen"
                                ],
                                "id": "frozen",
                                "size": {
                                    "resource": "memory",
                                    "value": 0
                                }
                            },
                            {
                                "zone_count": 3,
                                "instance_configuration_id": "azure.es.master.fsv2",
                                "node_roles": [
                                    "master",
                                    "remote_cluster_client"
                                ],
                                "id": "master",
                                "size": {
                                    "resource": "memory",
                                    "value": 0
                                }
                            },
                            {
                                "zone_count": 2,
                                "instance_configuration_id": "azure.es.coordinating.fsv2",
                                "node_roles": [
                                    "ingest",
                                    "remote_cluster_client"
                                ],
                                "id": "coordinating",
                                "size": {
                                    "resource": "memory",
                                    "value": 0
                                }
                            },
                            {
                                "zone_count": 1,
                                "instance_configuration_id": "azure.es.ml.fsv2",
                                "node_roles": [
                                    "ml",
                                    "remote_cluster_client"
                                ],
                                "id": "ml",
                                "size": {
                                    "resource": "memory",
                                    "value": 0
                                }
                            }
                        ],
                        "elasticsearch": {
                            "version": "8.13.2",
                            "enabled_built_in_plugins": []
                        },
                        "deployment_template": {
                            "id": "azure-storage-optimized"
                        }
                    }
                }
            ],
            "kibana": [
                {
                    "elasticsearch_cluster_ref_id": "main-elasticsearch",
                    "region": "azure-eastus2",
                    "plan": {
                        "cluster_topology": [
                            {
                                "instance_configuration_id": "azure.kibana.fsv2",
                                "zone_count": 1,
                                "size": {
                                    "resource": "memory",
                                    "value": 1024
                                }
                            }
                        ],
                        "kibana": {
                            "version": "8.13.2"
                        }
                    },
                    "ref_id": "main-kibana"
                }
            ],
            "integrations_server": [],
            "enterprise_search": []
        },
        "name": "my-first-api-deployment"
    }


    # Send a request to create the cluster
    response = requests.post(elasticloud_api_endpoint + "/api/v1/deployments",
                             headers={"Authorization": f"ApiKey {elasticloud_api_key}"},
                             json=cluster_config)

    # Print the response
    print(response.text)


if __name__ == "__main__":
    create_cluster()
