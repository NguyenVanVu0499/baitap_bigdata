import requests
import os
from os import listdir
from os.path import isfile, join
import time
mypath = './fake_data/'

for root, directories, files in os.walk(mypath):
    for filename in files:
        # Join the two strings in order to form the full filepath.
        filepath = os.path.join(root, filename)

        url = 'http://127.0.0.1:8081/uploadfile/'
        myfiles = { 'uploaded_file': open('{}'.format(filepath) ,'rb') }

        x = requests.post(url, files = myfiles)
        # time.sleep(3)
        # print(x.status_code)