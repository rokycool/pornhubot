import urllib.request
from urllib import request
import sys
import os
import io
import ssl
import re
from  bs4 import BeautifulSoup
import threading
import pymongo
import time
import random
import requests

ssl._create_default_https_context = ssl._create_unverified_context

UA_LIST = [ "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24" ]
header={ 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, sdch', 'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6', 'Connection': 'keep-alive','User-Agent': random.choice(UA_LIST) }
clients=pymongo.MongoClient('106.15.224.237')
date=time.strftime("%F-%T", time.localtime())
dbname="pornhub"
db=clients[dbname]
col1=db['detail']
col2=db['viurl']
col2.ensure_index('ph_url', unique=True)
num=0
renum=0
gonum=0
sunum=0

#最大下载进程
max_thread=2
#待完善功能
#1.更换header




def Save_url_mongo(title,downurl,url):
    global renum
    global gonum
    detail1 = {'时间':date,'标题': title,'下载URL':downurl,'ph_url':url}
    try:
        global sunum
        gonum +=1
        sunum +=1
        print("正在插入:",gonum,"downurl",downurl)
        col2.insert(detail1)
        print("插入成功:",sunum,"downurl",downurl)
    except:
        renum += 1
        print("exit code:1 url插入重复:",renum)




def get_down_url(url):
    try:
        r = request.Request(url)
    except request.RequestException as e:
        print("网页失败请求！1")
    try:
        response = request.urlopen(r)
        response=response.read().decode('utf-8')
        # print("response:",response)
        rtitle = re.findall(r'<title>.*?</title>', response)
        rdownurl = re.findall(r'videoUrl.*?}', response)
        rviews = re.findall(r"<span class=\"count\">.*?</span> views</div>",response)
        # print("rdownurl:",rdownurl,"rtitle",rtitle)
        rtitle = str(rtitle)
        title = re.sub('<.*?title>', '', rtitle)
        title = re.sub('\[', '', title)
        title = re.sub(']', '', title)
        # for i in {}:
        downurl = rdownurl[0].split('"')[2]
        if downurl == '':
            downurl = rdownurl[1].split('"')[2]
        downurl = re.sub('\\\\', '', downurl)
        # print("get_down_url函数中 downurl:",downurl)
        Save_url_mongo(title, downurl,url)
    except IOError as e:
        print("exit code:2",e)
    except:
        pass


def Get_url_mongo():
    global num
    for item in col1.find():
        num +=1
        print("open url :",num,item['ph_url'])
        if 'playlist' in item['ph_url'] or 'users' in item['ph_url']:
            pass
        else:
            get_down_url(item['ph_url'])


if __name__=='__main__':
    Get_url_mongo()