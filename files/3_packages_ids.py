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

with open('2_packages_errata.csv', 'r') as f:
    errata_packages = list(csv.DictReader(f))

with open('3_packages_errata_id.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['package_name', 'arch', 'package_id', 'errata_id', 'severity', 'errata_type'])

    for row in errata_packages:
        package_name = row['package_name']
        errata_id = row['errata_id']
        severity = row['severity']
        type_row = row['errata_type']
        api_url = f'{satellite_url}/packages?search=filename~{package_name}'
        response = session.get(api_url, verify=False)
        if response.status_code == 200:
            packages = response.json()['results']
            for package in packages:
                package_id = package['id']
                arch_type = package['arch']
                writer.writerow([package_name, arch_type, package_id, errata_id, severity, type_row])
        else:
            print(f"Error: Failed to fetch package information for {package_name} with status code {response.status_code}")

