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
