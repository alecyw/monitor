import os
import time
import psutil
import socket 
from flask import Flask
import urllib.request
import multiprocessing as mp
app = Flask(__name__,static_url_path='/static')

target_dir = './static/'
number_of_processors = 8
data_generator_name = 'generator.py'
net_prefix = 'http://192.168.0.'
net_suffix = ':5000/id'

@app.route('/') 
def initialize():
    global available_urls
    all_urls = [net_prefix + str(i) + net_suffix for i in list(range(0,256))]
    pool = mp.Pool(processes=number_of_processors)
    results = pool.map(get_html, all_urls)
    pool.close()
    available_urls = [result for result in results if result] 
    print('initial available_urls = ', available_urls)
    return 'Workstations found on this network:<br>'+'<br>'.join([url for url in available_urls if url]) + \
           '<br><a href=http://'+get_Host_name_IP()+':5000/report_all>report all</a>'

@app.route('/report_all')
def report_all():
    pool = mp.Pool(processes=number_of_processors)
    all_content = pool.map(get_html, available_urls)
    pool.close()
    return '<a href=http://'+get_Host_name_IP()+':5000/>Find workstation IP addresses</a><br><br>' + \
           '<a href=http://'+get_Host_name_IP()+':5000/report_all>report all</a><br><br>' + \
           '<br>'.join([content for content in all_content if content])

@app.route('/report')
def report():
    return generate_report()

@app.route('/id')
def id():
    return 'http://' + get_Host_name_IP() + ':5000/report'

def get_html(url):
    try:
        response = urllib.request.urlopen(url,timeout=1)
        return response.read().decode('utf-8')
    except:
        return 

def get_Host_name_IP(): 
    try: 
        host_name = socket.gethostname() 
        host_ipad = socket.gethostbyname(host_name) 
    except: 
        print("Unable to get Hostname and IP")     
        host_ipad=None
    return host_ipad

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

def generate_report():
    output_str = '<a href=http://' + get_Host_name_IP() 
    output_str += ':5000/report>' +get_Host_name_IP() + '</a><br>'
    output_str += data_generator_name
    if check_is_running(data_generator_name):
        output_str += ' is RUNNING<br>'
    else:
        output_str += ' is STOPPED<br>'
    output_str += '<table border="1">'
    output_str += '<tr><td><b>date created</b>'
    output_str += '</td><td><b>filename</b></td></tr>'
    filenames = os.listdir(target_dir)
    for filename in filenames:
        create_time = str(time.ctime(os.path.getctime(target_dir + filename)))
        output_str += '<tr><td>' + create_time 
        output_str += '</td><td><a href='
        output_str += 'http://'+get_Host_name_IP()+':5000'
        output_str += '/static/'
        output_str += filename
        output_str += '>'+filename+'</a></td></tr>'
    output_str += '</table>'
    return output_str

if __name__ == '__main__':
    app.run(host='0.0.0.0')