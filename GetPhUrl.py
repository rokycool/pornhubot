import urllib.request
from urllib import request
import ssl
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import pymongo
import time
import random

url = 'https://jp.pornhub.com'
ssl._create_default_https_context = ssl._create_unverified_context

UA_LIST = [ "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24" ]
header={ 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, sdch', 'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6', 'Connection': 'keep-alive','User-Agent': random.choice(UA_LIST) }
clients=pymongo.MongoClient('106.15.224.237')
date=time.strftime("%F-%T", time.localtime())
dbname="pornhub"+date
db=clients[dbname]
col1=db['ph_url']

#待完善功能
#1.更换header
#2.存取mongo数据


def url_save_mongo(ph_url):
    pass
    # print("ph_url:"+ph_url)
    # detail1={'ph_url':ph_url,'时间':date}
    # print("正在插入"+detail1)
    # col1.insert(detail1)


def get_ph_url(response):
    #这一段经常出问题 尝试3次
    try:
        selector = Selector(text=response)
        divs = selector.xpath('//div[re:test(@class,"thumbnail-info-wrapper")]//@href').extract()
        for div in divs:
            ph_url = url + div
            # print("viewurl:" + ph_url)
            try:
                ph_url=str(ph_url)
                print("ph_url:"+ph_url)
                detail1={'ph_url':ph_url,'时间':date}
                print("正在插入"+detail1)
                col1.insert(detail1)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)

def start_url():
    try:
        r = request.Request(url=url)
    except request.RequestException as e:
        print("网页请求失败! 2")
    response = request.urlopen(r)
    try:
        response = response.read().decode('utf-8')
        get_ph_url(response)
    except Exception as e:
        print(e)


if __name__=='__main__':
    start_url()
