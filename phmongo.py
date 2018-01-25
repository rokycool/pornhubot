#coding=utf-8
import pymongo
import time
clients=pymongo.MongoClient('106.15.224.237')
date=time.strftime("%F-%T", time.localtime())
dbname="pornhub"
db=clients[dbname]
col1=db['detail']
col1.ensure_index('ph_url', unique=True)
col2=db['viurl']
col2.ensure_index('title', unique=True)