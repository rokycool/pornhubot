import urllib.request
from urllib import request
import ssl
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import pymongo
import time
import json
import phmongo
pornhub_url={'https://jp.pornhub.com',
             'https://jp.pornhub.com/pornstar/faye-reagan',
             'https://jp.pornhub.com/view_video.php?viewkey=ph5a25fd66527ff',
             'https://jp.pornhub.com/view_video.php?viewkey=ph58abec05472e7',
             'https://www.pornhub.com/view_video.php?viewkey=ph59d6581c0c3e5',
             'https://www.pornhub.com/view_video.php?viewkey=ph59760c5b54040',
             'https://www.pornhub.com/view_video.php?viewkey=ph59ecb3af73456',
             'https://jp.pornhub.com/view_video.php?viewkey=ph57dfb291d5af9',
             'https://jp.pornhub.com/view_video.php?viewkey=ph5812166a71605',
             'https://jp.pornhub.com/playlist/62472362'}
ssl._create_default_https_context = ssl._create_unverified_context

# UA_LIST = [ "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24" ]
# header={ 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, sdch', 'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6', 'Connection': 'keep-alive','User-Agent': random.choice(UA_LIST) }

#待完善功能
#1.更换header
#最大抓取深度
# max_while=6
num=0
renum=0
gonum=0
def url_save_mongo(ph_url):
    global gonum
    global renum
    detail1={'时间':date,'ph_url':ph_url}
    print("正在插入",detail1['ph_url'])
    try:
        col1.insert(detail1)
        print("插入成功",gonum,detail1['ph_url'])
        gonum += 1
    except:
        renum += 1
        print("重复url:",renum)

def get_ph_url(response):
    #这一段经常出问题 尝试3次
    try:
        selector = Selector(text=response)
        divs = selector.xpath('//div[re:test(@class,"thumbnail-info-wrapper")]//@href').extract()
        for div in divs:
            _url='https://jp.pornhub.com'
            ph_url = _url + div
            ph_url = str(ph_url)
            print(ph_url)
            try:
                url_save_mongo(ph_url)
            except:
                print("exit code 2")
    except:
        print("exit code 3")

def start_url(url):
    try:
        r = request.Request(url=url)
    except:
        print("exit 4")
    response = request.urlopen(r)
    try:
        response = response.read().decode('utf-8')
        get_ph_url(response)
    except:
        print("exit code 6")

def parse_url__from_mongo():
    global num
    for i in pornhub_url:
        url_save_mongo(i)
    while (True):
        for item in phmongo.col1.find(no_cursor_timeout=True).batch_size(5):
            num +=1
            print("正在解析:",num,item['ph_url'])
            start_url(item['ph_url'])

if __name__=='__main__':
    # start_url()
    parse_url__from_mongo()
