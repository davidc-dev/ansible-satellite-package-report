import json

with open("combined.json", "r") as f:
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
            })
            packages.add(package)

with open('packages_errata.csv', 'w') as f:
    f.write('package_name,errata_id\n')
    for row in rows:
        f.write('{},{}\n'.format(row['package_name'], row['errata_id']))
