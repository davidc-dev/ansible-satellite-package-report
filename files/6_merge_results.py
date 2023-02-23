import json
import csv
import os

# Read in the input CSV file
input_file = 'packages_errata_with_package_id_and_repos.csv'
input_rows = []
with open(input_file, 'r') as f:
    reader = csv.reader(f)
    headers = next(reader)
    for row in reader:
        input_rows.append(row)

# Read in the CVE data from the JSON file
cve_data_file = 'package_cves.json'
with open(cve_data_file, 'r') as f:
    cve_data = json.load(f)

# Create a new CSV file with an added row for CVEs
output_file = 'cve_temp.csv'
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers + ['cves'])  # Add the new 'cves' column header
    for row in input_rows:
        package_name = row[0]
        if package_name in cve_data:
            cves = ', '.join(cve_data[package_name])
        else:
            cves = ''
        writer.writerow(row + [cves])

with open('cve_temp.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    rows = [row for row in reader]

# move the cves column to the 4th column
for row in rows:
    cves = row.pop()  # remove the last element (cves)
    row.insert(3, cves)  # insert cves at the 4th position

with open('final_report.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(rows)

os.remove("cve_temp.csv")
# # Read package_cves.json file and parse JSON data
# with open('package_cves.json') as f:
#     package_cves = json.load(f)

# ## load package id csv

# with open('packages_errata_with_package_id_and_repos.csv', 'r') as f:
#     package_repos = list(csv.DictReader(f))

# # Create a new list of dictionaries with the desired columns
# output_data = []
# for package_name, cves in package_cves.items():
#     row = {
#         'package_name': package_name,
#         'applicable_cves': ', '.join(cves),
#         'satellite_repo_path': package_repos[package_name]['satellite_repo_path'],
#         'source_repo_path': package_repos[package_name]['source_repo_path']
#     }
#     output_data.append(row)

# # Write output to a new CSV file
# with open('output.csv', 'w', newline='') as f:
#     writer = csv.DictWriter(f, fieldnames=['package_name', 'applicable_cves', 'satellite_repo_path', 'source_repo_path'])
#     writer.writeheader()
#     writer.writerows(output_data)


# # # read the errata_packages.csv into a pandas DataFrame
# # errata_df = pd.read_csv('errata_packages.csv')

# # # read the original CSV file into a pandas DataFrame
# # original_df = pd.read_csv('output.csv')

# # # create a new DataFrame that matches the package name between the two files
# # merge_df = pd.merge(original_df, errata_df, on='package_name')

# # # save the merged DataFrame to a new CSV file
# # merge_df.to_csv('merged.csv', index=False)