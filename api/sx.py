# -*- coding: utf-8 -*-

import time, bottle, re, base64, hashlib
from splitparser import sp

class mydict(dict):
    def __getattr__(self, key):
        return self.get(key,'')
    def __setattr__(self, key, value):
        self[key] = value
    def __add__(self, data):
        return mydict(self.items() + data.items())
    def __sub__(self, key):
        return mydict((k,v) for (k,v) in self.items() if k != key)

def hsh(s):
    return base64.urlsafe_b64encode( hashlib.sha256(s).digest() ).replace('-','A').replace('_','z')[:20]

def datef(d,f):
    return time.strftime(f, time.localtime(int(d)))

def dateg(d,f):
    return time.strftime(f, time.gmtime(int(d)))

def ts_get(d,f=None):
    return time.strptime(d, f or '%d.%m.%Y %H:%M')

def gts():
    return int(time.time())

def rend(txt):
    out = bottle.html_escape(txt)
    out = sp(out)
    return out.replace('\n', '<br />')

def g_opts(*n):
    opts = []
    for i in n:
        if i[1]: opts.append('%s=%s' % i)
    if opts: return '?' + '&'.join(opts)
    else: return ''