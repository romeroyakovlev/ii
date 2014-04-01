import re

def echo_flt(ea):
    rr = re.compile(r'^[a-z0-9_!.-]{1,60}\.\d{1,9}$')
    if rr.match(ea): return True

def msg_flt(msgid):
    rr = re.compile(r'^[a-z0-9A-Z]{20}$')
    if rr.match(msgid): return True
