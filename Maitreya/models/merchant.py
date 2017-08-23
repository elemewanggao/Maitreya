#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
    商家账单Model
'''
from . import Base, BaseModel
from sqlalchemy import (
    Column,
    Integer)


class MerchantBillDetail(Base, BaseModel):
    """商家账单"""
    __tablename__ = 'merchant_bill_detail'
    _db_name = 'merchant_clear'

    id = Column(Integer, primary_key=True)
    rst_walle_id = Column(Integer)
