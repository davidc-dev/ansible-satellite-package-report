import requests
import sys
import csv
import json

# Variables from arguments
satellite_hostname = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
lifecycle_environment = sys.argv[4]

# Authenticate with the Satellite API
auth = (username, password)
url = f'https://{satellite_hostname}'
session = requests.Session()
session.auth = auth

lifecycle_url = f'{url}/api/v2/hosts?search=lifecycle_environment={lifecycle_environment}'
lifecycle_response = session.get(lifecycle_url, verify=False)
host_list=json.loads(lifecycle_response.content)['results']

if lifecycle_response.status_code == 200:
    hosts = lifecycle_response.json()['results']
    with open('host_list.csv', mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['ID', 'Name'])
        for host in hosts:
            writer.writerow([host['id'], host['name']])
else:
    print('Failed to retrieve host list')