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

def int_value(value):
	if "%" in value:
		newint = int(value.strip("%")) /100
		return newint
	elif isinstance(value, int):
		print(value)
	else:
		print("数值错误")



def Save_url_mongo(title, downurl, url, percent,votesUp, votesDown, views):
    global renum
    global gonum
    detail1 = {'时间':date,'标题': title,'下载URL': downurl,'ph_url': url,'percent':percent,'votesUp': votesUp,'votesDown':votesDown,}
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
        def del_span(value):
            value = str(value)
            value = re.sub('\[', '', value)
            value = re.sub(']', '', value)
            value = re.sub('\'', '', value)
            return value
        response = request.urlopen(r)
        response=response.read().decode('utf-8')
        # print("response:",response)
        rtitle = re.findall(r'<title>.*?</title>', response)
        rdownurl = re.findall(r'videoUrl.*?}', response)
        rviews = re.findall(r"<span class=\"count\">.*?</span> views</div>",response)
        rviews = re.findall(r"<span class=\"count\">.*?</span>",response)
        rpercent = re.findall(r"<span class=\"percent\">.*?</span>",response)
        rvotesUp = re.findall(r"<span class=\"votesUp\">.*?</span>",response)
        rvotesDown = re.findall(r"<span class=\"votesDown\">.*?</span>",response)
        rviews = str(rviews)
        views = re.sub('<span class=\"count\">','',rviews)
        views = re.sub('</span>','',views)
        rpercent = str(rpercent)
        percent = re.sub('<span class="percent">','',rpercent)
        percent = re.sub('</span>','',percent)
        percent = re.sub('</span>','',percent)
        rvotesUp = str(rvotesUp)
        votesUp = re.sub('<span class="votesUp">','',rvotesUp)
        votesUp = re.sub('</span>','',votesUp)
        rvotesDown = str(rvotesDown)
        votesDown = re.sub('<span class="votesDown">','',rvotesDown)
        votesDown = re.sub('</span>','',votesDown)
        # print("rdownurl:",rdownurl,"rtitle",rtitle)
        rtitle = str(rtitle)
        title = re.sub('<.*?title>', '', rtitle)
        title = re.sub('\[', '', title)
        title = re.sub(']', '', title)
        downurl = rdownurl[0].split('"')[2]
        if downurl == '':
            downurl = rdownurl[1].split('"')[2]
        downurl = re.sub('\\\\', '', downurl)
        # print("get_down_url函数中 downurl:",downurl)
        percent=del_span(percent)
        percent=int_value(percent)
        votesDown=del_span(votesDown)
        votesDown=int(votesDown)
        votesUp=del_span(votesUp)
        votesUp=int(votesUp)
        views=del_span(views)
        views=int(re.sub(',','',views))
        print("\n", "percent", percent,"votesUp:",votesUp,"votesDown:", votesDown,"views:", views)
        # print("\n",title, downurl, url,"percent", percent,"votesUp:",votesUp,"votesDown:", votesDown,"views:", views)
        Save_url_mongo(title, downurl, url, percent,votesUp, votesDown, views)
    except IOError as e:
        print("exit code:2",e)
    except:
        pass


def Get_url_mongo():
    global num
    for item in col1.find(no_cursor_timeout=True):
        num +=1
        print("open url :",num,item['ph_url'])
        if 'playlist' in item['ph_url'] or 'users' in item['ph_url']:
            pass
        else:
            get_down_url(item['ph_url'])


if __name__=='__main__':
    Get_url_mongo()