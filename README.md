Monitor files generated on workstations within a subnet

To install and execute please follow these instructions:

# install modules
pip install -r requirements.txt 

# monitor
monitor.py : Web app that finds all peer workstation urls and reports all simulated data information.
App will run on all workstations.  Each station is aware of the other stations so a given workstation will also report others.
If a workstation with the app is added or removed the other workstations the report will reflect this change.
The report will include:
    application (process) is running
    when data files were first created
    list of current files on disk

Install and run on each workstation:

usage: python monitor.py --net_prefix 192.168.0 --generator_name data_generator.py

# dummy data generator
data_generator.py : simulates data generating setup where data files are continuously written to workstation log directory.

usage: python data_generator.py

# Web interface
Open browser, go to url of the workstation(s)
Example: http://192.168.0.1:5000/
This will initialize the server by searching on this sub net (192.168.0) for all 256 IP address that will respond to server request.
This may take a few minutes to initialize but only need to do once or when new workstations are added.
When this is complete the page will show all the workstations that are running "monitor.py" with their ip address.  Click on the link
to show all the data.  This will request from each workstation to report the data being generated.  Click on the 
reported files to see content.