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

import tornado.database

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

class ImageQr(tornado.web.RequestHandler):
    def get(self):
        res = {}
        res['result']='success'
        self.write(YZZ_JSON(res))
    def post(self):
        # height = self.get_argument("height")
        img_file = self.request.files['img'][0]
        nowclock = datetime.datetime.utcnow() + datetime.timedelta(hours=+8)
        nowtime = nowclock.isoformat()
        timenum = re.compile('[0-9]+')
        trimtime = timenum.findall(nowtime)
        sig = '_'
        types = img_file['filename'].split('.')
        new_file_name = sig.join(trimtime) + '.' + types[1]
        filepath = os.path.join(UPLOAD_DIR,new_file_name)
        output_file = open(filepath,'w')
        output_file.write(img_file['body'])
        output_file.close()
        xfs_wx_face_main.face_main(filepath)
        res = {}
        res['result']='success'
        self.write(YZZ_JSON(res))

application = tornado.web.Application([
    (r"/face/?",ImageQr),
])

if __name__ == "__main__":
    application.listen(8899)
    tornado.ioloop.IOLoop.instance().start()
