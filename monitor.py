import os
import time
import psutil
import pprint 
import socket 
from flask import Flask
import urllib.request
import multiprocessing as mp
app = Flask(__name__)

data_generator_name = 'generator.py'

@app.route('/')
def hello():
    results = list_log()
    return results

@app.route('/show_peers')
def show_peers():
    available_urls = find_peers()
    # all_content = ''
    # for url in available_urls:
    #     response = urllib.request.urlopen(url)
    #     webContent = response.read()
    #     all_content += webContent.decode('utf-8')
    #     all_content += '<br>'
    pool = mp.Pool(processes=8)
    all_content = pool.map(get_html, available_urls)
    pool.close()
    return ''.join(all_content)

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')

def find_peers():
    this_ip = get_Host_name_IP()
    available_servers = ['http://127.0.0.1:5000','http://127.0.0.1:5000']
    # first_part_ip = '.'.join(this_ip.split('.')[0:3])
    # last_part_ip = this_ip.split('.')[-1]
    # print(this_ip)
    # print(first_part_ip)
    # print(last_part_ip)
    # a = list(range(0,256))
    # # a.remove(int(last_part_ip))
    # for guess_ip in a:
    #     hostname = first_part_ip + '.' + str(guess_ip)
    #     # response = os.system("ping " + hostname)
    #     response = os.system("ping -c 1 " + hostname)
    #     #and then check the response...
    #     if response == 0:
    #         print(hostname, 'is up!')
    #         available_servers.append(hostname)
    #     else:
    #         print(hostname, 'is down!')
    return available_servers


# Function to display hostname and 
# IP address 
def get_Host_name_IP(): 
    try: 
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname(host_name) 
        print("Hostname :  ",host_name) 
        print("IP : ",host_ip) 
    except: 
        print("Unable to get Hostname and IP")     
        host_ip=None
    return host_ip

def is_running(processName):
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

def list_log():
    output_str = get_Host_name_IP() + '<br>'
    output_str += data_generator_name
    if is_running(data_generator_name):
        output_str += ' is RUNNING<br>'
    else:
        output_str += ' is STOPPED<br>'
    output_str += '<table border="1"><tr><td><b>date created</b></td><td><b>filename</b></td></tr>'
    filenames = os.listdir('./logs')
    for filename in filenames:
        create_time = str(time.ctime(os.path.getctime('./logs/' + filename)))
        output_str += '<tr><td>'+ create_time + '</td><td>' + filename + '</td></tr>'
    output_str += '</table>'
    return output_str

if __name__ == '__main__':
    app.run()