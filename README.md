# monitor
data_generator.py : simulates data generating setup where data files are continuously written to workstation log directory.

monitor.py : web app that finds all peer workstation urls and reports all simulated data information.  app will run on all workstations.  each station is aware of the other stations so a given workstation will also report others.  if a workstation with the app is added or removed the other workstations the report will reflect this change.
