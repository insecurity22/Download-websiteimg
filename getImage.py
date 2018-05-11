import re
import sys
import requests
from bs4 import BeautifulSoup
import base64
import urllib.request
import os
import time

def help():
    print('Usage : getImage url file_path_for_save')
    sys.exit(1)

# regex = Regular expression
# regex reference : https://wikidocs.net/4308
def remove_htmltag(content):
    regex = re.compile('\[<.*?>|<.*?>\]') # pattern object
    return regex.sub('', str(content))

def find_img(content):
    regex = re.compile('src\s*=\s*"([^"]+)"') # <img src="" alt="">
    return regex.findall(str(content))

def naming(num):
    full_name = save_path + "\\" + str(num) + ".jpg"
    print(full_name)
    return full_name

# I can't use urllib because 403 forbiden error, So I found other way.
def download_img(url):
    img = requests.get(url).content
    # response content is binary ex) b'\xff\xd8 ...
    try:
        file_name = naming(num)
        with open(file_name, 'wb')as f:
            f.write(img)
    except urllib.request.HTTPError as e:
        print(e)

def start(url):
    resp = requests.get(url)

    is_ok = resp.ok  # HTTP (True/False)
    if(is_ok == 1):
        html = resp.text    # html source
        soup = BeautifulSoup(html, 'html.parser')   # parsing
        tags = soup.select('#tooncontentdata')  # id = tooncontentdata

        # This part was base 64 Encoding -> base 64 Decoding
        decodedtags = base64.b64decode(remove_htmltag(tags))

        global num
        num = 0

        for i in find_img(decodedtags): # url
            print(i)
            num += 1
            download_img(i)
            time.sleep(4) # because web server can refuse to 10054 error

        print("\nDownload complete.")

    else:
        print("Can't connect\n")

if(len(sys.argv)!=3): # Usage
    help()

global save_path
save_path = sys.argv[2]

if not os.path.isdir(save_path): # folder
    print("Creating Folder...")
    os.makedirs(save_path)

start(sys.argv[1])