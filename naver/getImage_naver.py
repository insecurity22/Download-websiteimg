import sys
import requests
from bs4 import BeautifulSoup
import re
import os
import time
import urllib

def help():
    # getImage url save_path
    #   save_path = C:\Webtoon_name
    print('Usage: getImage url save_path')
    sys.exit(1)

def create_folder(save_path):
    if os.path.isdir(save_path) == False:
        print("Creating new folder...\n")
        os.makedirs(save_path)

def find_url(content):
    regex = re.compile('https:\/\/image.*\.jpg')
    return regex.findall(str(content))

def naming(num):
    # save_path + number(ex: 1) + ".jpg"
    name = sys.argv[2] + "\\" + str(num) + ".jpg"
    print(name)
    return name

def download_img(url):
    hdr = {'User-Agent':'Mozilla/5.0', 'referer':'http://m.naver.com'}
    img = requests.get(url, headers=hdr).content # 403 forbiden
    print(img) # response content is binary ex) b'\xff\xd8 ...
    try:
        global num
        num += 1
        imgfile_name = naming(num) # 1.jpg, 2.jpg, 3.jpg ...
        with open(imgfile_name, 'wb') as f:
            f.write(img)
    except urllib.request.HTTPError as e:
        print(e)

# Start
def download_webtoon(url, num):
    # HTTP GET Request
    resp = requests.get(url)

    # If is_ok is a valid response, return True
    is_ok = resp.ok
    if(is_ok == True):
        html = resp.text    # html Source
        soup = BeautifulSoup(html, 'html.parser')

        id_num = 0
        while True:
            try:
                img_tag_id = "#content_image_" + str(id_num)
                tags = soup.select(img_tag_id) # Find "img tag" to id value in html
                url_img_tag = find_url(tags) # Find "an url" in img tag
                print(url_img_tag)

                download_img(url_img_tag[num])
                id_num += 1
                time.sleep(2)
            except:
                break

        print("\nDownload complete.\n")

if(len(sys.argv)!=3): # Usage
    help()

print("\nPlease check it...")
print("argv[1] = " + sys.argv[1])
print("argv[2] = " + sys.argv[2] + "\n")
time.sleep(1)

num = 0
create_folder(sys.argv[2])
download_webtoon(sys.argv[1], num)

