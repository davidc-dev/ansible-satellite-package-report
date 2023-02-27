import requests
import json
import sys
import csv

# Variables from arguments
satellite_hostname = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
host_collection_name = sys.argv[4]

# Authenticate with the Satellite API
auth = (username, password)
url = f'https://{satellite_hostname}/'
session = requests.Session()
session.auth = auth

# Get list of hosts from defined host collection name
host_collection_url = f'{url}katello/api/host_collections'
host_collection_response = session.get(host_collection_url, verify=False)
host_collections=json.loads(host_collection_response.content)['results']

## Get ID for specified host collection
host_collection_id = None
for host_collection in host_collections:
    if host_collection['name'] == host_collection_name:
        host_collection_id = host_collection['id']
        break

## Get list of hosts from specified ID

host_collection_id_url = f'{url}katello/api/host_collections/{host_collection_id}'
host_collection_id_response = session.get(host_collection_id_url, verify=False)
host_list=json.loads(host_collection_id_response.content)

## Get all host details 

hosts_url = f'{url}api/hosts'
hosts_response = session.get(hosts_url, verify=False)
hosts = json.loads(hosts_response.content)

## Get details for each host matching IDs from host collections and put into csv


# Open a CSV file for writing
with open('host_info.csv', 'w', newline='') as f:
    writer = csv.writer(f)

    # Write the header row
    writer.writerow(['host_id', 'host_name', 'operating_system_name', 'organization_name', 'errata_status_label', 'hostgroup_name', 'lifecycle_environment_name', 'content_view_name'])

    # Loop through the host_ids in file2
    for host_id in host_list['host_ids']:
        # Find the matching host in file1
        for host in hosts['results']:
            if host['id'] == host_id:
                # Extract the desired fields
                row = [
                    host['id'],
                    host['name'],
                    host['operatingsystem_name'],
                    host['organization_name'],
                    host['errata_status_label'],
                    host['hostgroup_name'],
                    host['content_facet_attributes']['lifecycle_environment_name'],
                    host['content_facet_attributes']['content_view_name']
                ]

                # Write the row to the CSV file
                writer.writerow(row)

                # Stop searching for this host
                break