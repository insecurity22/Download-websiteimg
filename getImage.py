import re
import sys
import requests
from bs4 import BeautifulSoup
import base64
import urllib.request
import time

def help():
    print('Usage : getImage [url]')

# regex = Regular expression
# regex reference : https://wikidocs.net/4308
def remove_htmltag(content):
    regex = re.compile('\[<.*?>|<.*?>\]') # pattern object
    return regex.sub('', str(content))

def find_img(content):
    regex = re.compile('src\s*=\s*"([^"]+)"') # <img src="" alt="">
    return regex.findall(str(content))

def naming(num):
    full_name = str(num) + ".jpg"
    print(full_name)
    return full_name

# I can't use urllib because 403 forbiden error, So I found other way.
def download_img(url):
    image = requests.get(url).content
    # response content is binary ex) b'\xff\xd8 ...
    try:
        file_name = naming(num)
        with open(file_name, 'wb')as f:
            f.write(image)
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

        print("\nDownloading...")

    else:
        print("Can't connect\n")

if(len(sys.argv)!=2): # Usage
    help()

start(sys.argv[1])