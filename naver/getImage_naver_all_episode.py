import sys
import requests
from bs4 import BeautifulSoup
import re
import os
import time
import urllib

def help():
    #
    # ex) ./getImage url save_path episode_number
    #
    # url = https://...
    # save_path = C:\Webtoon_name\17화
    # episode_number = 17
    print('Usage: ./getImage url save_path episode_number')
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
    global path
    name = path + "\\" + str(num) + ".jpg"
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

def change_folder_path(path):
    global episode
    text = str(episode) + "화"
    path_text = re.sub(r'[0-9]*화', text, path) # 패턴과 일치하는 문자열 변경
    return path_text

def change_url(url):
    global episode
    no = "no=" + str(episode) + "&"
    url_text = re.sub(r'no=.*&', no, url)
    return url_text

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

if(len(sys.argv)!=4): # Usage
    help()

print("\nPlease check it...")
print("argv[1] = " + sys.argv[1]) # url
print("argv[2] = " + sys.argv[2]) # save path
print("argv[3] = " + sys.argv[3] + "\n") # episode
time.sleep(1)

num = 0
episode = int(sys.argv[3]) # begin the episode
path = sys.argv[2]

create_folder(sys.argv[2]) # make a folder
download_webtoon(sys.argv[1], num)
time.sleep(1)

while True:
    try:
        num = 0
        episode += 1
        path = change_folder_path(sys.argv[2])
        create_folder(path)

        changed_url = change_url(sys.argv[1])
        print(changed_url)
        download_webtoon(changed_url, num)
        print(episode)
    except:
        break


