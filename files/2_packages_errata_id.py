import json

with open("1_content_view_query_results.json", "r") as f:
    data = json.load(f)

rows = []
packages = set()

for errata_id, errata_data in data.items():
    for package in errata_data['packages']:
        if package.endswith('.i686'):
            package = package[:-5] # remove the last 5 characters (.i686)
        elif package.endswith('.x86_64'):
            package = package[:-7] # remove the last 7 characters (.x86_64)
        elif package.endswith('.noarch'):
            package = package[:-7] # remove the last 7 characters (.noarch)
        if package not in packages:
            rows.append({
                'package_name': package,
                'errata_id': errata_id,
                'severity': errata_data.get('severity'),
                'errata_type': errata_data.get('errata_type')
            })
            packages.add(package)


with open('2_packages_errata.csv', 'w') as f:
    f.write('package_name,errata_id,severity,errata_type\n')
    for row in rows:
        f.write('"{0}","{1}","{2}","{3}"\n'.format(row['package_name'], row['errata_id'], row['severity'], row['errata_type']))