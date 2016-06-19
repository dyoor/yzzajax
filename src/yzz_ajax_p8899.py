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
import simplejson

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
        rows = db.execute('SELECT * FROM test_table')
        str = json.dumps(rows)
        self.write(str)
    def post(self):
        res = {}
        res['result']='success'
        # data = YZZ_JSON(res)
        # print type(res)
        self.write(res)

application = tornado.web.Application([
    (r"/?",MainQr),
])

if __name__ == "__main__":
    application.listen(8899)
    tornado.ioloop.IOLoop.instance().start()
