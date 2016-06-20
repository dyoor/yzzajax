# coding=utf-8

__author__ = 'shijian'

import tornado

import os.path
import re
import datetime
import os,sys

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import json

#apt-get install mysql
#apt-get install libmysqlclient-dev
#apt-get install MySQL-python

import torndb

db = torndb.Connection('127.0.0.1','yzzajax',user='yzz',password='yzz9988')

class YZZ_JSON(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        else:
            return super(YZZ_JSON, self).default(obj)

class MainQr(tornado.web.RequestHandler):
    def get(self):
        rows = db.query('SELECT * FROM test_table')
        str = json.dumps(rows)
        self.write(str)
    def post(self):
        res = {}
        res['result']='success'
        self.write(res)
    def put(self):
        res = {}
        res['method']='put'
        res['result']='success'
        self.write(res)

class PageQr(tornado.web.RequestHandler):
    def get(self,page):
        len = 3
        page_from = page*len
        sql = "SELECT * FROM test_table LIMIT {0},{1}".format(page_from,len)
        rows = db.query(sql)
        str = json.dumps(rows)
        self.write(str)

application = tornado.web.Application([
    (r"/?",MainQr),
    (r"/p/([0-9]+)/?",PageQr),
])

if __name__ == "__main__":
    application.listen(8899)
    tornado.ioloop.IOLoop.instance().start()
