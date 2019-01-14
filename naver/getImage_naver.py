
import sys
import requests
from bs4 import BeautifulSoup
import re
import time
import os

def help():
    #
    # ./getImage url save_path
    #   save_path = C:\Webtoon_name\17화
    #
    print('Usage: ./getImage url save_path')
    sys.exit(1)

def create_folder(save_path):
    if os.path.isdir(save_path) == False:
        print("Creating new folder...\n")
        os.makedirs(save_path)

def find_img_url_to_regex(content):
    regex = re.compile('https:\/\/image.*\.jpg')
    return regex.findall(str(content))

def naming(num):
    # save_path + number(ex: 1) + ".jpg"
    name = sys.argv[2] + "\\" + str(num) + ".jpg"
    print(name)
    return name

def download_webtoon(url):
    resp = requests.get(url)
    is_ok = resp.ok
    if(is_ok == True):
        html = resp.text # html source
        soup = BeautifulSoup(html, 'html.parser') # for parsing

        # After img tag id find, all image download
        id_num = 0
        hdr = {'User-Agent':'Mozilla/5.0', 'referer':'http://m.naver.com'}
        while True:
            try:
                # Find
                img_tag_id = "#content_image_" + str(id_num)
                select = soup.select(img_tag_id) # ex) <img src="https:// ...
                regex = find_img_url_to_regex(select) # https:// ...
                print(regex)

                # Download
                img = requests.get(regex[0], headers=hdr).content
                print(img) # response content is binary ex) b'\xff\xd8 ...

                filename = naming(id_num+1)
                with open(filename, 'wb') as f:
                    f.write(img)
                id_num += 1
                time.sleep(2)

            except Exception as ex:
                break

if(len(sys.argv)!=3): # Usage
    help()

# Check input value
print("Your input value is ...\nargv[1] = ", sys.argv[1])
print("argv[2] = ", sys.argv[2], "\n")

create_folder(sys.argv[2])
download_webtoon(sys.argv[1])
