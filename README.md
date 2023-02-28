# **ansible-satellite-package-report**
Ansible playbook that runs python scripts to assemble custom reports in csv format.

## **package_errata_report.yml**

Outputs a series of json files and csv files with information about errata, packages, repos, cves based on specified content view and content view version.  See examples in ***example_outputs*** directory.  Files from this package have 1-6 prefix.

Variable Name   |  Example                       |  Description
----------------|----------------------- | ----------------------------------------
inventory_host  |  test.example.com      |  Host to execute scripts and output reports
satellite_host  |  satellite.example.com  |  Hostname of Satellite Server
satellite_user  |  admin                 |  Satellite Server usernamne
satellite_pswd  |  password               |  Satellite Server password
content_view    |  RHEL8                    |  Name of Content View to run against
content_view_version|   6.0              |  Version of Content View to run against
full_results    |  True/False            |  Set to True to get full resuts from content view query.  **Warning** Will increase run time dramatically.
content_view_filter_name | security_only | Set name of Content view filter to use.  Leave blank ```content_view_filter_name: ""``` if no filter used.

## **host_errata_pre_patch.yml**

Generates a list of hosts (***host_info.csv***) in specified host collection and then outputs a csv (***pre-patch-host-errata.csv***) adding all applicable errata to that host and column for data/time script is run.  Run this before applying patchs/updates to get a baseline.  Example files in ***example_outputs*** directory.

Variable Name   |  Example                       |  Description
----------------|----------------------- | ----------------------------------------
inventory_host  |  test.example.com      |  Host to execute scripts and output reports
satellite_host  |  satellite.example.com  |  Hostname of Satellite Server
satellite_user  |  admin                 |  Satellite Server usernamne
satellite_pswd  |  password               |  Satellite Server password
host_collection    |  RHEL8-Hosts         |  Name of host collection to query 

## **host_errata_pre_patch.yml**
Generates a list of hosts (***host_info.csv***) in specified host collection and then outputs a csv (***post-patch-host-errata.csv***) adding all applicable errata to that host and column for data/time script is run.  Run this after applying patchs/updates and then compare to ***pre-patch-host-errata.csv*** to verify applicate errata was installed.  Example files in ***example_outputs*** directory.

Variable Name   |  Example                       |  Description
----------------|----------------------- | ----------------------------------------
inventory_host  |  test.example.com      |  Host to execute scripts and output reports
satellite_host  |  satellite.example.com  |  Hostname of Satellite Server
satellite_user  |  admin                 |  Satellite Server usernamne
satellite_pswd  |  password               |  Satellite Server password
host_collection    |  RHEL8-Hosts         |  Name of host collection to query 