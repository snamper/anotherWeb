#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/25 0025 上午 9:11
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""

import datetime
import sqlalchemy as SA
from sqlalchemy.orm import object_session
from sqlalchemy.ext.declarative import declarative_base

from config import settings


class tBase(object):
    session = property(lambda self: object_session(self)) # 记录已有的session,hold住一个数据传输通道

    create_date = SA.Column(SA.DateTime, default=datetime.datetime.now)
    modified_date = SA.Column(SA.DateTime, default=datetime.datetime.now, onupdate=SA.text("current_timestamp"))

    @classmethod
    def create(cls, session, **kwargs):
        info = cls()
        for k, v in kwargs.iteritems():
            setattr(info, k, v)
        session.add(info)
        session.commit()


machine_no = None

Base = declarative_base(cls=tBase)


echo = settings.echo_sql
db_info = settings.db

db = SA.create_engine(
    "mysql://%s:%s@%s/%s?charset=utf8" % (db_info["user"], db_info["password"], db_info["host"], db_info["db_name"]),
    echo=echo,
    pool_recycle=3600,
    pool_size=30,
    max_overflow=60
)

metadata = Base.metadata