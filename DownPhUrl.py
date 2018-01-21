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
col2=db['downurl']
col2.ensure_index('title', unique=True)
num=0
renum=0
gonum=0
sunum=0

#最大下载进程
max_thread=2
#待完善功能
#1.更换header




def Save_url_mongo(title,downurl):
    global renum
    global gonum
    detail1 = {'时间':date,'标题': title,'下载URL':downurl}
    try:
        gonum +=1
        print("正在插入:",gonum,"\ndownurl",downurl)
        col2.insert(detail1)
    except:
        print("exit code:2 url插入重复:",renum,"\ndownurl:",downurl)
        renum += 1

def callbackfunc(blocknum, blocksize, totalsize):
    '''回调函数
    @blocknum: 已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
    '''
    global url
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    downsize=blocknum * blocksize
    if downsize >= totalsize:
       downsize=totalsize
    s ="%.2f%%"%(percent)+"====>"+"%.2f"%(downsize/1024/1024)+"M/"+"%.2f"%(totalsize/1024/1024)+"M \r"
    sys.stdout.write(s)
    sys.stdout.flush()
    if percent == 100:
        print('')


def down_file(downurl,title):
    global sunum
    title=title+'.mp4'
    filename=os.path.basename(title+".mp4")
    print("开始下载文件",title)
    try:
        request.urlretrieve(downurl, filename, callbackfunc)
    except:
        print("exit code: 5 无法下载该文件:",title,"\ndownurl:")
    sunum +=1
    print("下载成功 开始记录到数据库",sunum)
    Save_url_mongo(title,downurl)


def get_down_url(url):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    try:
        r = request.Request(url)
    except request.RequestException as e:
        print("网页失败请求！1")
    response=request.urlopen(r)
    try:
        response=response.read().decode('utf-8')
        # print("response:",response)
        rtitle = re.findall(r'<title>.*?</title>', response)
        rdownurl = re.findall(r'videoUrl.*?}', response)
        # print("rdownurl:",rdownurl,"rtitle",rtitle)
        rtitle = str(rtitle)
        title = re.sub('<.*?title>', '', rtitle)
        title = re.sub('\[', '', title)
        title = re.sub(']', '', title)
        # for i in range(1):
        downurl = rdownurl[1].split('"')[2]
        if downurl == None:
            downurl = rdownurl[2].split('"')[2]
        downurl = re.sub('\\\\', '', downurl)
        # print("get_down_url函数中 downurl:",downurl)
        down_file(downurl, title)
    except:
        print("exit code:4")


def Get_url_mongo():
    global num
    for item in col1.find():
        num +=1
        print("open url :",num,item['ph_url'])
        get_down_url(item['ph_url'])


if __name__=='__main__':
    Get_url_mongo()
    # 启动线程下载
    # threading.Thread(target=Get_url_mongo,args=('')).start()
