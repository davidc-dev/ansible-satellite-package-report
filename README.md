# <h1>ansible-satellite-package-report</h1>
Ansible playbook that runs a few python scripts to assemble a csv report

Outputs a series of json files and csv files with information about errata, packages, repos, cves based on specified content view and content view version.

## Variables

Variable Name   |  Example                       |  Description
----------------|----------------------- | ----------------------------------------
satellite_host  |  satellite.example.com  |  Hostname of Satellite Server
satellite_user  |  admin                 |  Satellite Server usernamne
satellite_pswd  |  password               |  Satellite Server password
content_view    |  RHEL8                    |  Name of Content View to run against
content_view_version|   6.0              |  Version of Content View to run against
full_results    |  True/False            |  Set to True to get full resuts from content view query.  **Warning** Will increase run time dramatically.