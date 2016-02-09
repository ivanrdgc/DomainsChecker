-----
domainschecker
-----

Small tool that uses the RPPproxy API to check the availability of a given domain name per all entities in tld.csv file. Before using it, add API credentials to config.ini file.

Usage (command line):
 `./app.py <domain_to_check>`

You can also run the UI wrapper for this app:
 `./gtkapp.py`

To build standalone for Windows (create .exe file), you will need to have py2exe for python 3 and python3 installed. Run the script build_win32.py inside the dist folder.

![App started](/_app_images/open-gtk-app.png?raw=true "App started")
![Domain search started](/_app_images/init-domain-search.png?raw=true "Domain search started")
![Domain search in progress](/_app_images/mid-domain-search.png?raw=true "Domain search in progress")
![Domain search finished](/_app_images/end-domain-search.png?raw=true "Domain search finished")
![Result example](/_app_images/result-example.png?raw=true "Result example")
