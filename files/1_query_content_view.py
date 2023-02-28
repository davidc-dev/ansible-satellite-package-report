import requests
import json
import sys

# Authenticate with the Satellite API
username = sys.argv[2]
password = sys.argv[3]
auth = (username, password)
url = f'https://{sys.argv[1]}/katello/api/v2/'
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

## Apply content view filter
content_filter_id = None
if len(sys.argv[7]) > 0:
    content_filter_name = sys.argv[7]
    content_filter_url = f'{url}/content_views/{my_content_view_id}/filters'
    content_filter_response = session.get(content_filter_url, verify=False)
    content_filter = json.loads(content_filter_response.content)['results']
    for cf in content_filter:
        if cf['name'] == content_filter_name:
            content_filter_id = cf['id']
            print(content_filter_id)
            break

# # Get a list of all erratas in the selected content view version
full_version = sys.argv[6]
if len(str(content_filter_id)) > 0:
    errata_url = f'{url}errata?content_view_version_id={str(my_content_view_version_id)}&content_filter_id={content_filter_id}&full_result={full_version}'
    print(errata_url)
    errata_response = session.get(errata_url, verify=False)
    errata=json.loads(errata_response.content)['results']
else:
    errata_url = f'{url}errata?content_view_version_id={str(my_content_view_version_id)}&full_result={full_version}'
    errata_response = session.get(errata_url, verify=False)
    errata=json.loads(errata_response.content)['results']

# Count the number of errata_ids
count = 0
for erratum in errata:
    if 'errata_id' in erratum:
        count += 1

# Output the count
print(f"There are {count} errata_ids in the JSON data.")

# print(errata)

## Search for CVEs, bugs, and packages in the errata and output as separate JSON files
cves_output = {}
bugs_output = {}
packages_output = {}
for e in errata:
    if e['hosts_available_count'] > 0:
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
    if e['hosts_available_count'] > 0:
        combined_output[str(e['errata_id'])] = {
            'severity': str(e['severity']),
            'errata_type': str(e['type']),
            'CVEs': cves_output.get(str(e['errata_id']), []),
            'bugs': bugs_output.get(str(e['errata_id']), []),
            'packages': packages_output.get(str(e['errata_id']), [])
        }

# Output the results as a single JSON object to a file
with open('1_content_view_query_results.json', 'w') as f:
    json.dump(combined_output, f)

