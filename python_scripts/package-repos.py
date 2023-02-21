import json
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

# Read the package_cves.json file
with open('package_cves.json', 'r') as f:
    package_cves_output = json.load(f)

# Query the Satellite API for package IDs for each unique package name
package_ids_output = {}
for package_name in package_cves_output:
    api_url = f'{satellite_url}/packages?search=filename~{package_name}'
    response = session.get(api_url, verify=False)
    if response.status_code == 200:
        data = json.loads(response.content)
        if data['total'] > 1:
            package_id = data['results'][0]['id']
            package_ids_output[package_name] = package_id

# Output the results to a new JSON file with unique package names as the parent
with open('package_ids.json', 'w') as f:
    json.dump(package_ids_output, f)


# Get a list of all content views on the Satellite server
content_views_url = satellite_url + 'content_views/'
content_views_response = session.get(content_views_url, verify=False)
content_views = json.loads(content_views_response.content)['results']


# # Select the content view you're interested in and get its ID
my_content_view = sys.argv[4]
my_content_view_id = None
for cv in content_views:
    if cv['name'] == my_content_view:
        my_content_view_id = cv['id']
        break

# # Get a list of all versions of the selected content view
content_view_versions_url = satellite_url + 'content_view_versions/'
content_view_versions_params = {'content_view_id': my_content_view_id}
content_view_versions_response = session.get(content_view_versions_url, params=content_view_versions_params, verify=False)
content_view_versions = json.loads(content_view_versions_response.content)['results']

# # Select the content view version you're interested in and get its ID
my_content_view_version = sys.argv[5]
my_content_view_version_id = None
for cvv in content_view_versions:
    if cvv['version'] == my_content_view_version:
        my_content_view_version_id = cvv['id']
        break

## load package id json

with open('package_ids.json', 'r') as f:
    package_ids_output = json.load(f)

# Get package repo id for content view version
output = []
for key, value in package_ids_output.items():
    api_url = f'{satellite_url}/repositories?content_view_version_id={my_content_view_version_id}&environment_id=1&organization_id=1&rpm_id={value}&search='
    response = session.get(api_url, verify=False)
    if response.status_code == 200:
        data = json.loads(response.content)
        if data['total'] > 0:
            satellite_repo_path = data['results'][0]['full_path']
            source_repo_path = data['results'][0]['url']
            package_name = key
            package_id = value
            row = {
                "package_name": package_name,
                "package_id": package_id,
                "satellite_repo_path": satellite_repo_path,
                "source_repo_path": source_repo_path
            }
            output.append(row)

# Output the results to a new CSV file with unique package names as the parent
with open('package_repos.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["package_name", "package_id", "satellite_repo_path", "source_repo_path"])
    writer.writeheader()
    for row in output:
        writer.writerow(row)

# Read package_cves.json file and parse JSON data
with open('package_cves.json') as f:
    package_cves = json.load(f)

# Read package_repos.csv file and store data in a dictionary
with open('package_repos.csv') as f:
    reader = csv.DictReader(f)
    package_repos = {row['package_name']: row for row in reader}

# Create a new list of dictionaries with the desired columns
output_data = []
for package_name, cves in package_cves.items():
    row = {
        'package_name': package_name,
        'applicable_cves': ', '.join(cves),
        'satellite_repo_path': package_repos[package_name]['satellite_repo_path'],
        'source_repo_path': package_repos[package_name]['source_repo_path']
    }
    output_data.append(row)

# Write output to a new CSV file
with open('output.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['package_name', 'applicable_cves', 'satellite_repo_path', 'source_repo_path'])
    writer.writeheader()
    writer.writerows(output_data)