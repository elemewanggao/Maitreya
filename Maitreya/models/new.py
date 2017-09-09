#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""爬取URL"""
from datetime import datetime
from . import Base, BaseModel
from sqlalchemy import (
    Column, Integer, BigInteger, DateTime, String, Text
)


class TbNew(Base, BaseModel):
    """记录推送新闻信息."""
    __tablename__ = 'tb_new'
    _db_name = 'matreya'

    id = Column(BigInteger, nullable=False, primary_key=True)
    url_id = Column(BigInteger, nullable=False, default=1)
    url = Column(String(255), nullable=False, default="")
    title = Column(String(255), nullable=False, default="")
    content = Column(Text, nullable=False, default="")
    date = Column(String(32), nullable=False, default="")
    label = Column(String(32), nullable=False, default="")
    origin = Column(String(32), nullable=False, default="")
    like_num = Column(Integer, nullable=False, default=0)
    unlike_num = Column(Integer, nullable=False, default=0)
    look_num = Column(Integer, nullable=False, default=0)
    collect_num = Column(Integer, nullable=False, default=0)
    share_num = Column(Integer, nullable=False, default=0)
    remark = Column(String(255), default="")
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)
