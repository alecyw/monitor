import os
import sys
import time
from random import random

def get_date_time_string():
    return time.strftime('%Y-%m-%d_%H-%M-%S')

def save_data():
    if not os.path.isdir(os.path.join(os.getcwd(), 'static')):
        os.mkdir(os.path.join(os.getcwd(), 'static'))
    filename = 'static/'+ get_date_time_string() + '.txt'
    with open(filename,'w') as f:
        f.write(filename)

def random_poll():
    while True:
        time.sleep(10)
        val = int(random() * 10)
        if val == 1:
            save_data()

if __name__ == '__main__':
    random_poll()
