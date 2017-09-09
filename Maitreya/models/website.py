#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""爬取URL"""
from datetime import datetime
from . import Base, BaseModel
from sqlalchemy import (
    Column, BigInteger, DateTime, String
)


class TbWebsite(Base, BaseModel):
    """爬取网站的信息."""
    __tablename__ = 'tb_website'
    _db_name = 'matreya'

    id = Column(BigInteger, nullable=False, primary_key=True)
    domain_name = Column(String(255), nullable=False, default="")
    remark = Column(String(255), default="")
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)
