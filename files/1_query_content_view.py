import requests
import json
import sys

# Authenticate with the Satellite API
username = sys.argv[2]
password = sys.argv[3]
auth = (username, password)
url = f'https://{sys.argv[1]}/katello/api/'
session = requests.Session()
session.auth = auth

# Get a list of all content views on the Satellite server
content_views_url = url + 'content_views/'
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
content_view_versions_url = url + 'content_view_versions/'
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

# # Get a list of all erratas in the selected content view version
full_version = sys.argv[6]
errata_url = f'{url}errata?content_view_version_id={str(my_content_view_version_id)}&full_result={full_version}'
errata_response = session.get(errata_url, verify=False)
errata=json.loads(errata_response.content)['results']


# Search for CVEs, bugs, and packages in the errata and output as separate JSON files
cves_output = {}
bugs_output = {}
packages_output = {}
for e in errata:
    cves = []
    bugs = []
    packages = []
    for cve in e['cves']:
        cves.append(cve['cve_id'])
    for bug in e['bugs']:
        bugs.append(bug['bug_id'])
    for package in e['packages']:
        packages.append(package)
    if cves:
        cves_output[str(e['errata_id'])] = cves
    if bugs:
        bugs_output[str(e['errata_id'])] = bugs
    if packages:
        packages_output[str(e['errata_id'])] = packages

# Combine the data into a single JSON object with the errata ID as the parent
combined_output = {}
for e in errata:
    combined_output[str(e['errata_id'])] = {
        'CVEs': cves_output.get(str(e['errata_id']), []),
        'bugs': bugs_output.get(str(e['errata_id']), []),
        'packages': packages_output.get(str(e['errata_id']), [])
    }

# Output the results as a single JSON object to a file
with open('combined.json', 'w') as f:
    json.dump(combined_output, f)

