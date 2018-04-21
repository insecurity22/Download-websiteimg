import sys
import base64
import requests
from bs4 import BeautifulSoup

def help():
    print('Usage: getImage [url]')

def download_web_image(url):

    resp = requests.get(url)

    is_ok = resp.ok  # HTTP (True/False)
    if(is_ok == 1):
        html = resp.text    # html source
        # print(html)
        # < Compare >
        # F12 Debug mode
        # Parsing html
        # == because two codes can different

        soup = BeautifulSoup(html, 'html.parser')    # interpret html
        tags = soup.select('#tooncontentdata')       # parsing html tag
        # base 64 Encoding -> base 64 Decoding
        print(str(base64.b64decode(tags)))

    else:
        print("Can't connect\n")

if(len(sys.argv)!=2): # Usage
    help()

download_web_image(sys.argv[1])