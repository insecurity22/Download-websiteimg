import sys
import requests
from bs4 import BeautifulSoup
import re
import base64

def help():
    print('Usage: getImage [url]')

# regex = Regular expression
def remove_tag(content):
    regex = re.compile('\[<.*?>|<.*?>\]') # pattern object
    cleantext = regex.sub('', str(content))
    return cleantext

def find_url(content):
    regex = re.compile('^(https?:\/\/)([0-9a-z\.-]+).([a-z]\/)') # http:// or https://
    text = regex.findall(str(content))
    print(text)

def download_web_image(url):
    resp = requests.get(url)

    is_ok = resp.ok  # HTTP (True/False)
    if(is_ok == 1):
        html = resp.text    # Check print(html) = html source
        soup = BeautifulSoup(html, 'html.parser')    # interpret html
        tags = soup.select('#tooncontentdata')       # id = tooncontentdata
        # This part was base 64 Encoding -> base 64 Decoding

        decodetags = base64.b64decode(remove_tag(tags))
        remove_tag(decodetags)
        print(decodetags)
        print("\n\n")
        find_url(decodetags)
    else:
        print("Can't connect\n")

if(len(sys.argv)!=2): # Usage
    help()

download_web_image(sys.argv[1])