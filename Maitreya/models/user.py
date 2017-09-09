#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""爬取URL"""
from datetime import datetime
from . import Base, BaseModel
from sqlalchemy import (
    Column, BigInteger, DateTime, String
)


class TbUser(Base, BaseModel):
    """记录用户信息."""
    __tablename__ = 'tb_user'
    _db_name = 'matreya'

    id = Column(BigInteger, nullable=False, primary_key=True)
    user_id = Column(String(32), nullable=False, default='')
    user_name = Column(String(64), nullable=False, default='')
    remark = Column(String(255), default="")
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)
