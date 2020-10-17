import os
import time
import psutil
import pprint 
import socket 
from flask import Flask
import urllib.request
import multiprocessing as mp
app = Flask(__name__)

number_of_processors = 8
data_generator_name = 'generator.py'

@app.route('/id')
def id():
    return 'http://' + get_Host_name_IP() + ':5000'

@app.route('/')
def hello():
    results = list_log()
    return results

@app.route('/show_peers')
def show_peers():
    all_content = find_peers()
    return '<br>'.join(all_content)
    # available_urls = find_peers()
    # pool = mp.Pool(processes=number_of_processors)
    # all_content = pool.map(get_html, available_urls)
    # pool.close()
    # return '<br>'.join([content for content in all_content if content])

def get_html(url):
    try:
        response = urllib.request.urlopen(url,timeout=1)
        return response.read().decode('utf-8')
    except:
        return 

def find_peers():
    all_urls = ['http://192.168.0.'+str(i)+':5000' for i in list(range(0,256))]
    # all_urls = ['http://192.168.0.'+str(i)+':5000/id' for i in list(range(0,256))]
    pool = mp.Pool(processes=number_of_processors)
    results = pool.map(get_html, all_urls)
    pool.close()
    return [result for result in results if result] 


# Function to display hostname and 
# IP address 
def get_Host_name_IP(): 
    try: 
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname(host_name) 
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
    app.run(host='0.0.0.0')
    # print(find_peers())