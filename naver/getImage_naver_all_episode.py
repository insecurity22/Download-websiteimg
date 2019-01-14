
import sys
import requests
from bs4 import BeautifulSoup
import re
import time
import os

def help():
    #
    # ./getImage url save_path episode_number
    # url = https://...
    # save_path = C:\Webtoon_name\17화
    # episode_number = 17
    #
    print('Usage: ./getImage url save_path episode_number')
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
                return regex
                break

def change_url_and_folder_path(url, path):
    global episode
    episode += 1

    # Change URL
    no = "no=" + str(episode) + "&"
    url_text = re.sub(r'no=.*&', no, url)
    print(url_text)

    # Change save path
    text = str(episode) + "화"
    path_text = re.sub(r'[0-9]*화', text, path)  # 패턴(text)과 일치하는 문자열(path중) 변경
    print(path_text)
    return (url_text, path_text)

if(len(sys.argv)!=4): # Usage
    help()

# Check input value
print("Your input value is ...\nargv[1] = ", sys.argv[1])
print("argv[2] = ", sys.argv[2])
print("argv[3] = ", sys.argv[3], "\n")

episode = int(sys.argv[3])

while True:
    try:
        create_folder(sys.argv[2])
        checklist = download_webtoon(sys.argv[1])
        print("Download complete", episode, "화")
        (sys.argv[1], sys.argv[2]) = change_url_and_folder_path(sys.argv[1], sys.argv[2])
    except Exception as ex:
        if not checklist: # If List is empty
            continue
        if ex:
            break
