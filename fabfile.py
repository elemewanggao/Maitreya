#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
    Fab命令函数定义
'''
from __future__ import with_statement
from fabric.api import *

env.hosts = ['106.14.224.110']
env.use_ssh_config = True
env.keepalive = 60


# def test():
#     with settings(warn_only=True):
#         result = local('./manage.py test my_app', capture=True)
#     if result.failed and not confirm("Tests failed. Continue anyway?"):
#         abort("Aborting at user request.")


def git_add_and_commit():
    """git add & git commit."""
    local("git add ~/git/Maitreya && git commit")


def git_push():
    """git push."""
    with settings(warn_only=True):
        push_result = local("git push")
    if push_result.failed:
        local("git push --set-upstream origin develop")


def pre_d():
    """git operation."""
    git_add_and_commit()
    git_push()


def d():
    code_dir = '/srv/ves/Maitreya'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone https://github.com/elemewanggao/Maitreya.git %s" % code_dir)
    with cd(code_dir):
        run("git pull")
        print 'prod deploy success!'
