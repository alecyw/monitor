import os
import time
import psutil
import socket 
import argparse
from flask import Flask
import urllib.request
import multiprocessing as mp
app = Flask(__name__,static_url_path='/static')

# Output directory of data generator
target_dir = './static/'
number_of_processors = 8
net_suffix = ':5000/id'

# Initial entry point to web app, finds available urls on subnet
# Should only be run once to get list of responding workstations
@app.route('/') 
def initialize():
    global available_urls
    # 256 possible workstation IP addresses
    all_urls = [net_prefix + str(i) + net_suffix for i in list(range(0,256))]
    pool = mp.Pool(processes=number_of_processors)
    # Find the IPs that respond to url request
    results = pool.map(get_html, all_urls)
    pool.close()
    # Filter out the Nones
    available_urls = [result for result in results if result] 
    print('initial available_urls = ', available_urls)
    return 'Workstations found on this network:<br>'+'<br>'.join([url for url in available_urls if url]) + \
           '<br><a href=http://'+get_Host_name_IP()+':5000/report_all>report all</a>'

# Show all the reports from all available workstations
@app.route('/report_all')
def report_all():
    pool = mp.Pool(processes=number_of_processors)
    # Create list of report responses
    all_content = pool.map(get_html, available_urls)
    pool.close()
    return '<a href=http://'+get_Host_name_IP()+':5000/>Find workstation IP addresses</a><br><br>' + \
           '<a href=http://'+get_Host_name_IP()+':5000/report_all>report all</a><br><br>' + \
           '<br>'.join([content for content in all_content if content])

# Return a single report from this requested workstation
@app.route('/report')
def report():
    return generate_report()

# Return the url for this workstation's report
@app.route('/id')
def id():
    return 'http://' + get_Host_name_IP() + ':5000/report'

# Return the string from a url request to workstation
def get_html(url):
    try:
        response = urllib.request.urlopen(url,timeout=1)
        return response.read().decode('utf-8')
    except:
        return 

# Return the IP address of this workstation
def get_Host_name_IP(): 
    try: 
        host_name = socket.gethostname() 
        host_ipad = socket.gethostbyname(host_name) 
    except: 
        print("Unable to get Hostname and IP")     
        host_ipad=None
    return host_ipad

# Check if a processName is running
def check_is_running(processName):
    listOfProcessObjects = []
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['cmdline'])
            if pinfo['cmdline']:
                if processName.lower() in ''.join(pinfo['cmdline']):
                    listOfProcessObjects.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return len(listOfProcessObjects) > 0

# Create the report string for this workstation
def generate_report():
    # Show this workstation's IP address
    output_str = '<a href=http://' + get_Host_name_IP() 
    output_str += ':5000/report>' +get_Host_name_IP() + '</a><br>'
    output_str += data_generator_name
    # Is the processName running on this workstation?
    if check_is_running(data_generator_name):
        output_str += ' is RUNNING<br>'
    else:
        output_str += ' is STOPPED<br>'
    # Create the report table
    output_str += '<table border="1">'
    output_str += '<tr><td><b>date created</b>'
    output_str += '</td><td><b>filename</b></td></tr>'
    # Find the list of all the files in the generator directory
    filenames = os.listdir(target_dir)
    # Loop through the list of files
    for filename in filenames:
        # When was this file created
        create_time = str(time.ctime(os.path.getctime(target_dir + filename)))
        output_str += '<tr><td>' + create_time 
        output_str += '</td><td><a href='
        output_str += 'http://'+get_Host_name_IP()+':5000'
        output_str += '/static/'
        # What is the filename
        output_str += filename
        output_str += '>'+filename+'</a></td></tr>'
    output_str += '</table>'
    return output_str

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='File display server')
    parser.add_argument('--net_prefix', type=str, help='net prefix', default='http://192.168.0.')
    parser.add_argument('--generator_name', type=str, help='generator name', default='generator.py')
    args = parser.parse_args()
    net_prefix = args.net_prefix
    data_generator_name = args.generator_name
    app.run(host='0.0.0.0')