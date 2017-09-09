#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""爬取URL"""
from datetime import datetime
from . import Base, BaseModel
from sqlalchemy import (
    Column, BigInteger, DateTime, String
)


class TbOriginUrl(Base, BaseModel):
    """网站下爬取的入口URL及爬取的策略."""
    __tablename__ = 'tb_origin_url'
    _db_name = 'matreya'

    id = Column(BigInteger, nullable=False, primary_key=True)
    website_id = Column(BigInteger, nullable=False, default=1)
    url = Column(String(255), nullable=False, default="")
    title = Column(String(255), nullable=False, default="")
    content = Column(String(255), nullable=False, default="")
    date = Column(String(255), nullable=False, default="")
    label = Column(String(255), nullable=False, default="")
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)
