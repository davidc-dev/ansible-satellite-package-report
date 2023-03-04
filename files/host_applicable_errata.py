import requests
import sys
import csv
import datetime

# Variables from arguments
satellite_hostname = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
output_filename = sys.argv[4]


# Authenticate with the Satellite API
auth = (username, password)
url = f'https://{satellite_hostname}/'
session = requests.Session()
session.auth = auth

# Read in the input CSV file
input_file = 'host_list.csv'

# Create a new CSV file with an added row for CVEs
output_file = output_filename

# Define the names of the input and output columns
input_columns = ["host_id", "host_name"]
output_columns = input_columns + ["errata_ids", "script_run_time"]

# Export the input CSV data to a list of dictionaries
hosts = []
with open(input_file, "r") as f:
    reader = csv.DictReader(f, fieldnames=input_columns)
    next(reader)
    for row in reader:
        hosts.append(row)

# Make HTTP requests to the Satellite API for each host and extract errata IDs
for host in hosts:
    # Construct the API endpoint URL for the host's errata
    api_url = f"{url}api/v2/hosts/{host['host_id']}/errata?full_result=true"
    # Make an HTTP request to the API and authenticate using credentials
    response = session.get(api_url, verify=False)

#     Parse the response to extract the errata IDs
    if response.status_code == 200:
        errata = response.json()
        errata_ids = [e["errata_id"] for e in errata["results"]]
        host["errata_ids"] = ",".join(errata_ids)
    else:
        host["errata_ids"] = "Error fetching errata"

# Add a new column with the current date and time
current_time = datetime.datetime.now()
for host in hosts:
    host["script_run_time"] = current_time.strftime("%Y-%m-%d %H:%M:%S")


# Export the updated list of dictionaries to a new CSV file
with open(output_file, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=output_columns)
    writer.writeheader()
    for host in hosts:
        writer.writerow(host)