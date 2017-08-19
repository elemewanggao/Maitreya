#!/usr/bin/env python
# -*- coding: utf-8 -*-

from blinker import signal
import log


sig_call_done = signal(2000)
sig_call_ok = signal(2001)
sig_call_user_exc = signal(2002)
sig_call_sys_exc = signal(2003)
sig_call_unexcepted_exc = signal(2004)
sig_call_req = signal(2005)
sig_call_final = signal(2006)
sig_call_custom_exc = signal(2007)


def signal_init():
    """信号注册."""
    sig_call_ok.connect(log.log_info)
    sig_call_user_exc.connect(log.log_warn)
    sig_call_custom_exc.connect(log.log_warn)
    sig_call_sys_exc.connect(log.log_error)
    sig_call_unexcepted_exc.connect(log.log_error)
    sig_call_req.connect(log.log_request_info)
