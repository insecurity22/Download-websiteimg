import re
import sys
import requests
from bs4 import BeautifulSoup
import base64
import urllib.request
import os
import string

def help():
    # getImage 다운로드할url 다운로드할파일경로 웹툰마지막화숫자
    print('Usage : getImage url file_path_for_save webtoon_end_number')
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
    full_name = folder + "\\" + str(num) + ".jpg"
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

        print("\nDownload complete.\n")

    else:
        print("Can't connect\n")

def automatic(episode_num):
    # start first episode folder
    global site
    if episode_num < 10:
        site = (sys.argv[1])[:-7] + "0" + str(episode_num) + ".html"
    else:
        site = (sys.argv[1])[:-7] + str(episode_num) + ".html"
    print(site)

    global folder
    folder = (sys.argv[2])[:-2] + str(episode_num) + (sys.argv[2])[-1:]
    print(folder)

def createfolder(save_path):
    if not os.path.isdir(save_path):
        print("\nCreating Folder...\n")
        os.makedirs(save_path)

if(len(sys.argv)!=4): # Usage
    help()

episode_num = 1
for i in range(0, int(sys.argv[3])):
    automatic(episode_num)
    createfolder(folder)
    start(site)
    episode_num += 1


