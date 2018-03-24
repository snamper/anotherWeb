#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/24 0024 下午 1:19
 @Author  : yitian
 @Software: PyCharm
 @Description: 
"""
from views.base import BaseHandler, authenticated


class IndexHandler(BaseHandler):

    def get(self, *args, **kwargs):
        user = self.current_user
        render_settings = dict()
        render_settings["name"] = user
        if not user:
            self.render("index/login.html", **render_settings)
        else:
            self.render("index/index.html", **render_settings)

    @authenticated
    def post(self, *args, **kwargs):
        pass
