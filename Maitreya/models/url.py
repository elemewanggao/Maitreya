#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""爬取URL"""
from datetime import datetime
from . import Base, BaseModel
from sqlalchemy import (
    Column, BigInteger, DateTime, String, SmallInteger
)


class TbUrl(Base, BaseModel):
    """记录URL爬取信息,包括URL链接，是否爬取."""
    __tablename__ = 'tb_url'
    _db_name = 'matreya'

    id = Column(BigInteger, nullable=False, primary_key=True)
    website_id = Column(BigInteger, nullable=False, default=1)
    origin_url_id = Column(BigInteger, nullable=False, default=1)
    method = Column(SmallInteger, nullable=False, default=1)
    url = Column(String(255), nullable=False, default="")
    is_crawled = Column(SmallInteger, nullable=False, default=0)
    remark = Column(String(255), default="")
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)
