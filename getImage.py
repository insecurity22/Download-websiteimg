import re
import sys
import requests
from bs4 import BeautifulSoup
import base64
import urllib.request

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

def download_img(url):
    # 403 forbiden because you know bot
    # urllib reference : https://docs.python.org/3.4/library/urllib.html
    hdr = {'User-Agent': 'Mozila/5.0', 'referer': 'http:/m.naver.com'}
    req = urllib.request.Request(url, hdr)
    try:
        #urllib.request.urlopen(req) # call web document
        full_name = naming(num)
        #urllib.request.urlretrieve(url, full_name)
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

        for i in find_img(decodedtags):
            print(i)
            num += 1
            download_img(i)

        print("\nDownloading...")

    else:
        print("Can't connect\n")

if(len(sys.argv)!=2): # Usage
    help()

start(sys.argv[1])