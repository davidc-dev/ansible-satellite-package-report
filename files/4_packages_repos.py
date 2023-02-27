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

## load package id csv

with open('3_packages_errata_id.csv', 'r') as f:
    packages_ids = list(csv.DictReader(f))

output = []
for row in packages_ids:
    pckg_id = row['package_id']
    api_url = f'{satellite_url}/repositories?content_view_version_id={my_content_view_version_id}&environment_id=1&organization_id=1&rpm_id={pckg_id}&search='
    response = session.get(api_url, verify=False)
    if response.status_code == 200:
        data = json.loads(response.content)
        if data['total'] > 0:
            satellite_repo_path = data['results'][0]['full_path']
            source_repo_path = data['results'][0]['url']
            package_name = row['package_name']
            architecture = row['arch']
            package_id   = row['package_id']
            errata_id = row['errata_id']
            severity = row['severity']
            errata_type = row['errata_type']
            row = {
                "package_name": package_name,
                "arch": architecture,
                "package_id": package_id,
                "errata_id": errata_id,
                "severity": severity,
                "errata_type": errata_type,
                "satellite_repo": satellite_repo_path,
                "source_repo": source_repo_path
            }
            output.append(row)

# Output the results to a new CSV file with unique package names as the parent
with open('4_packages_errata_id_repos.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["package_name", "arch", "package_id", "errata_id", "severity", "errata_type", "satellite_repo", "source_repo"])
    writer.writeheader()
    for row in output:
        writer.writerow(row)
