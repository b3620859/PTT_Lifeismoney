from bs4 import BeautifulSoup
import requests
import urllib.request
import re # 正規表示
import os # 操作系統資料夾、檔案


pattern = "Line"
out_path = "output.txt"

def main():
    # 頁面URL
    URL_now = "https://www.ptt.cc/bbs/Lifeismoney/index.html"
    # 跑的次數
    targetLoop = 10
    countLoop = 1
    while countLoop<=targetLoop:
        print("Page: " + str(countLoop) + "/ " + str(targetLoop))
        returnURL = parsePage(URL_now)
        URL_now = returnURL
        countLoop+=1

def parsePage(pageURL):
    res = requests.get(pageURL, cookies={})
    soup = BeautifulSoup(res.text, 'html.parser')
    articleList = findAllTitle(soup)
    href_list = list()
    for div in articleList:
        try:
            if (((div.find('div', class_='title').text.split('['))[1].split(']'))[0]) != "創作" and (((div.find('div', class_='title').text.split('['))[1].split(']'))[0]) != "公告":
                content_list = list()
                content_list.append(div.find('div', class_='title').text.split('\n')[1])
                content_list.append(div.find('div', class_='title').a.get('href'))
                content_list.append(div.find('div', class_='date').getText())# TEST
                href_list.append(content_list)

        except:
            try:
                if (((div.find('div', class_='title').text.split('［'))[1].split(']'))[0]) != "創作" and (((div.find('div', class_='title').text.split('['))[1].split(']'))[0]) != "公告":
                    content_list = list()
                    content_list.append(div.find('div', class_='title').text.split('\n')[1])
                    content_list.append(div.find('div', class_='title').a.get('href'))
                    content_list.append(div.find('div', class_='date').getText())# TEST
                    href_list.append(content_list)
            except:
                pass

    for item in href_list:
        # print(item) # use Test
        pattern = re.compile(r'LINE', re.I)
        result = pattern.search(item[0])
        if result:
            loadArticle(item)
        else:
            continue

    # 前往下一頁
    nextURL = findNextPageURL(soup)
    URL_now = "https://www.ptt.cc" + nextURL
    return URL_now

""" 下一頁URL """
# 此function將回傳下一頁的URL。
def findNextPageURL(HTMLdata):
    return (HTMLdata.find('div', id='action-bar-container').find_all('a'))[3].get('href')

""" 取當前頁面所有文章列 """
# 此function將回傳當前文章列表所有文章標題，唯一list。
def findAllTitle(HTMLdata):
    # data.find_all('div', class_='title')
    rows = HTMLdata.find_all('div', class_='r-ent')
    return rows

""" 讀取文章標題以及連結 """
def loadArticle(data):
    title = fixFilePath(data[0])
    URL = "https://www.ptt.cc" + data[1]
    date = data[2]
    # save file
    save(title, URL, date)

def save(title, url, date):
    print(date+" "+title+" "+url)
    with open(out_path, 'a') as f:
        f.write(title + " "+url+ " "+ date+ "\n")

""" Fix the illegal file path charactors """
# 處理txt檔案名稱，針對windows不合法的檔案名稱字元進行replace。
def fixFilePath(oriPath):
    title = oriPath.replace('/', ' ')
    title = title.replace('\\', ' ')
    title = title.replace('"', ' ')
    title = title.replace('*', ' ')
    title = title.replace('?', ' ')
    title = title.replace(':', ' ')
    title = title.replace(';', ' ')
    title = title.replace('|', ' ')
    title = title.replace(',', ' ')
    title = title.replace('<', ' ')
    title = title.replace('>', ' ')
    return title

if __name__ == "__main__":
    main()