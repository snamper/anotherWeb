#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/25 0025 上午 11:52
 @Author  : Administrator
 @Software: PyCharm
 @Description:
"""
import ujson as json
from task.mail import send_mail
from views.base import BaseHandler


class WebHookHandler(BaseHandler):

    def post(self, *args, **kwargs):
        import subprocess
        headers = self.headers
        body = self.params
        send_body = ["网站更新成功!", "头部: %s" % json.dumps(headers), "body: %s" % json.dumps(body)]
        cwd = "/root/src/anotherWeb"
        subprocess.Popen("git pull origin master; supervisorctl restart all; echo '更新成功!!!'", cwd=cwd, shell=True)
        send_mail.delay("更新通知", '\n'.join(send_body), to=["fengzhibushang@163.com"])

