import os
import sys
import time
import urllib
import requests
import re
from bs4 import BeautifulSoup
import time
header = {
'User-Agent':
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'
}
url = "https://cn.bing.com/images/async?q={0}&first={1}&count={2}&scenario-ImageBasicHover&datsrc=N_I&layout=ColumnBased&mmasync=1&dg5tate=c*9_y*2226s2180s2072s2043s2292s2295s2079s2203s2094_1*71_w*198&IG=0D6AD6CBAF43430EA716510A4754C951&SFX={3}&iid=images.5599"

def getImage(url, count):
    try:
        time.sleep(0.5)
        # 更新路径为 path 变量下的文件名
        filename = os.path.join(path, name + str(count + 1) + '.jpg')
        urllib.request.urlretrieve(url, filename)
    except Exception as e:
        time.sleep(1)
        print("圖片爬取異常,跳過...")
    else:
        print("成功保存" + str(count + 1) + "張圖")

def findImgUrlFromHtml(html, rule, url,key , first, loadNum, sfx, count):

    soup = BeautifulSoup (html, "lxml")
    link_list = soup.find_all("a", class_="iusc")
    url = []
    for link in link_list:
        if count >= countNum:  # 檢查是否已達到目標數量
            break
        result = re.search(rule, str(link))

        url = result.group(0)

        url = url[8:len(url)]

        getImage(url, count)
        count += 1

    return count

def getStartHtml (url, key, first, loadNum, sfx):

    page = urllib.request.Request(url.format(key, first, loadNum, sfx), headers=header)
    html = urllib.request.urlopen(page)
    return html
if __name__ == '__main__':
        name = input("請輸入要下載的圖片: ")

        path='./imgs/'+ name

        countNum = 5

        key = urllib.parse.quote(name)
        first = 1
        loadNum=35
        sfx = 1
        count = 0
        rule = re.compile(r"\"murl\"\:\"http\S[^\"]+")
        if not os.path.exists(path):
            os.makedirs (path)
        while count < countNum:
            html = getStartHtml (url, key, first, loadNum, sfx)
            count = findImgUrlFromHtml(html, rule, url, key, first, loadNum, sfx,count)
            first = count + 1
            sfx += 1