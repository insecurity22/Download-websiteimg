import sys
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os

def createFolder(savepath):
    if os.path.isdir(savepath) == False:
        print("Creating new folder ...\n")
        os.makedirs(savepath)

def getDomain(url):
    return re.compile("https:\/\/.*\/").search(str(url)).group()

def download(url, savepath):
    id_num = 0

    # Set header
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "max-age=0",
        "if-modified-since": "Fri, 14 Jun 2019 17: 32:02 GMT",
        "if-none-match": "424c1614d722d51:0",
        "referer": getDomain(url),
        "sec-ch-ua": "Chromium;v = \"88\", \"Google Chrome\";v = \"88\", \";Not A Brand\";v = \"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "document",
        "sec - fetch - mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "user-agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome / 88.0.4324.190 Safari/537.36"
    }

    path = "./chromedriver.exe"
    driver = webdriver.Chrome(path)

    resp = requests.get(url)
    if(resp.ok == True):
        html = resp.text
        soup = BeautifulSoup(html, 'html.parser')
        img_tag = soup.select("img[src*='https://i5.bacloud1.com']")
        for tag in img_tag:
            # print(tag['  src'])
            # https://stackoverflow.com/questions/43982002/extract-src-attribute-from-img-tag-using-beautifulsoup/47166671

            # Create folder
            createFolder(savepath)
            filename = savepath + "\\" + str(id_num) + re.compile('(.png|.jpg|.jpeg|.gif)').search(tag['src']).group()
            print(filename + "에 저장 중...")

            # Get cookies
            driver.get(url)
            cookies = {}
            for cookie in driver.get_cookies():
                cookies['cookie'] = cookie['name'] + "=" + cookie['value']

            # Download
            img = requests.get(tag['src'], headers=headers, cookies=cookies).content
            with open(filename, 'wb') as f:
                f.write(img)

            id_num += 1
	driver.quit()

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print('Usage: ./getImage url save_path')
        sys.exit(1)

    print("Parameter is ...")
    print('argv[1] : ', sys.argv[1])
    print('argv[2] : ', sys.argv[2], "\n")

    download(sys.argv[1], sys.argv[2])