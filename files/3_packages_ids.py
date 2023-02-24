import requests
import csv
import sys

# Define the Satellite API connection details
satellite_url = f'https://{sys.argv[1]}/katello/api/v2/'
username = sys.argv[2]
password = sys.argv[3]
auth = (username, password)
session = requests.Session()
session.auth = auth

with open('packages_errata.csv', 'r') as f:
    errata_packages = list(csv.DictReader(f))

with open('packages_errata_with_package_id.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['package_name', 'package_id', 'errata_id'])

    for row in errata_packages:
        package_name = row['package_name']
        errata_id = row['errata_id']
        api_url = f'{satellite_url}/packages?search=filename~{package_name}'
        response = session.get(api_url, verify=False)
        if response.status_code == 200:
            packages = response.json()['results']
            for package in packages:
                package_id = package['id']
                writer.writerow([package_name, package_id, errata_id])
        else:
            print(f"Error: Failed to fetch package information for {package_name} with status code {response.status_code}")

