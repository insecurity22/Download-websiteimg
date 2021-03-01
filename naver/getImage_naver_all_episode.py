import sys
import requests
from bs4 import BeautifulSoup
import re
import os
import time

def findImgSrc(tag):
    return re.compile('https:\/\/image.*\.jpg').findall(str(tag))

def createFolder(savepath):
    if os.path.isdir(savepath) == False:
        print("Creating new folder ...\n")
        os.makedirs(savepath)

def download(url, savepath, episodenum):
    resp = requests.get(url)
    if(resp.ok == True):
        html = resp.text
        soup = BeautifulSoup(html, 'html.parser')

        id_num = 0
        header = {'User-Agent':'Mozilla/5.0', 'Referer':'http://m.naver.com'}
        # User-Agent : 브라우저 종류
        # Referer : 이전 페이지 URL
        # Accept-Language : 어떤 언어의 응답을 원하는가
        # Authorization : 인증 정보
        # https://goodthings4me.tistory.com/140

        while True:
            try:
                # Get img src
                img_id_tag = '#content_image_' + str(id_num)
                img_tag = soup.select(img_id_tag) # <img src="https:// ...
                img_src = findImgSrc(img_tag)
                print(img_src, "has been downloaded")

                # Download
                filename = savepath + str(id_num) + re.compile('(.png|.jpg|.jpeg|.gif)').search(img_src[0]).group()
                img = requests.get(img_src[0], headers=header).content # ex) b'\xff\xd8 ...
                with open(filename, 'wb') as f:
                    f.write(img)

                id_num += 1
                time.sleep(2)

            except Exception as e:
                break

if __name__ == '__main__':

    if len(sys.argv) != 4:
        print('Usage: ./getImage url save_path episode_number')
        print('url : Webtoon URL')
        print('save_path : 다운 받을 이미지를 저장할 경로')
        print('episode_number : 1')
        sys.exit(1)

    print("Parameter is ...")
    print('argv[1] : ', sys.argv[1])
    print('argv[2] : ', sys.argv[2])
    print('argv[3] : ', sys.argv[3], "\n")

    url = sys.argv[1]
    savepath = sys.argv[2]
    episodenum = int(sys.argv[3])
    while True:
        try:
            # Create folder
            folder = savepath + "\\" + str(episodenum) + "\\"
            createFolder(folder)
            print(folder, "폴더 생성")

            print(str(episodenum) + "화 다운로드 시작")
            download(url, folder, episodenum)

            # Change URL
            episodenum += 1
            no = "no=" + str(episodenum)
            url = url.replace(re.compile("no=\d*").search(url).group(), no)

            time.sleep(5)
        except Exception as e:
            print(e)
            break
