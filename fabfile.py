#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
    Fab命令函数定义
'''
from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['root@106.14.224.110']
env.use_ssh_config = True
env.keepalive = 60


# def test():
#     with settings(warn_only=True):
#         result = local('./manage.py test my_app', capture=True)
#     if result.failed and not confirm("Tests failed. Continue anyway?"):
#         abort("Aborting at user request.")


def git_add_and_commit():
    """git add & git commit."""
    local("git add ~/git/Maitreya -p && git commit")


def git_push():
    """git push."""
    with settings(warn_only=True):
        push_result = local("git push")
    if push_result.failed:
        local("git push --set-upstream origin develop")


def git():
    """git operation."""
    print 'pushing code to origin branch!'
    git_add_and_commit()
    git_push()


def merge_to_master(branch='develop'):
    """将指定分支merge到master分支."""
    local("git checkout master")
    local("git merge {branch}".format(branch=branch))
    local("git push")
    local("git checkout {branch}".format(branch=branch))


def deploy():
    """deploy in production environment."""
    if not confirm('You are ready to deploy in production environment.'
                   'Do your code has pushed master?'):
        abort('stop deploy beacuse your code not push to master!')

    code_dir = '/srv/ves/Maitreya/Maitreya'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone https://github.com/elemewanggao/Maitreya.git %s" % code_dir)
    with cd(code_dir):
        run("git pull")
        print 'prod deploy success!'
