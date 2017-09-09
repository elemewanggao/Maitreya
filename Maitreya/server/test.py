# -*-coding:utf-8 -*-
from flask import Blueprint
from Maitreya.utils.decorator import api

test = Blueprint('test', __name__)


@test.route('/test_blueprint')
@api
def test_blueprint():
    return 'blueprint'


@test.route('/exc')
@api
def test_exc():
    return 1 / 0


@test.route('/query_param')
@api
def query(id):
    return id
