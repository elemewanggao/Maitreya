#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""爬取URL"""
from datetime import datetime
from . import Base, BaseModel
from sqlalchemy import (
    Column, Integer, BigInteger, DateTime, String, SmallInteger
)


class TbUserLog(Base, BaseModel):
    """用户浏览新闻日志表."""
    __tablename__ = 'tb_user_log'
    _db_name = 'matreya'

    id = Column(BigInteger, nullable=False, primary_key=True)
    user_id = Column(String(255), nullable=False, default="")
    new_id = Column(BigInteger, nullable=False, default=1)
    begin_time = Column(DateTime, nullable=False, default=datetime.now)
    end_time = Column(DateTime, nullable=False, default=datetime.now)
    time = Column(Integer, nullable=False, default=0)
    is_look = Column(SmallInteger, nullable=False, default=0)
    is_like = Column(SmallInteger, nullable=False, default=0)
    is_unlike = Column(SmallInteger, nullable=False, default=0)
    is_collect = Column(SmallInteger, nullable=False, default=0)
    is_share = Column(SmallInteger, nullable=False, default=0)
    remark = Column(String(255), default="")
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)
