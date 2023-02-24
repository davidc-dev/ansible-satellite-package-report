import requests
import json


# Read the combined JSON file
with open('combined.json', 'r') as f:
    combined_output = json.load(f)

# Query the Red Hat Security Data API for package information for each CVE in each errata
cve_packages_output = {}
for errata_id, data in combined_output.items():
    for cve in data['CVEs']:
        api_url = f'https://access.redhat.com/hydra/rest/securitydata/cve/{cve}.json'
        response = requests.get(api_url)
        if response.status_code == 200:
            data = json.loads(response.content)
            packages_output = {}
            for package in data['affected_release']:
                if package['advisory'] == errata_id:
                    packages_output[package['package']] = {
                        'date': package['release_date'],
                        'advisory': package['advisory']
                    }
            cve_packages_output[cve] = packages_output

# Output the results to a new JSON file with the CVE ID as the parent
with open('cve_packages.json', 'w') as f:
    json.dump(cve_packages_output, f)

# Rearrange the data to create a new JSON object with unique package names as the parent
package_cves_output = {}
for cve, packages in cve_packages_output.items():
    for package_name, package_info in packages.items():
        # Remove the "0:" prefix from the package name
        package_name = package_name.replace('0:', '')
        if package_name not in package_cves_output:
            package_cves_output[package_name] = []
        if cve not in package_cves_output[package_name]:
            package_cves_output[package_name].append(cve)

# Output the results to a new JSON file with unique package names as the parent
with open('package_cves.json', 'w') as f:
    json.dump(package_cves_output, f)