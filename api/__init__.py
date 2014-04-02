# -*- coding: utf-8 -*-

import base64, zlib, sx, flt

def b64c(s,needcompress):
    if needcompress: cnt = zlib.compress(s.encode('utf-8'))
    else: cnt = s.encode('utf-8')
    return base64.urlsafe_b64encode(cnt)

def b64d(s):
    cnt = base64.b64decode( s.replace('-','+').replace('_','/') )
    try:
        return zlib.decompress(cnt)
    except:
        return cnt

def _parze(msg):
    pz = msg.splitlines()
    mo = sx.mydict()
    optz = pz[0].split('/')
    mo.update( dict(zip(optz[::2],optz[1::2])) )
    for i,n in enumerate(('echoarea','date','msgfrom','addr','msgto','subj'),1):
        mo[n] = pz[i]
    mo.msg = '\n'.join(pz[8:])
    mo.date = int(mo.date)
    return mo

def _out(mo):
    pz = ['','','','','','','','','']
    for i,n in enumerate(('echoarea','date','msgfrom','addr','msgto','subj'),1):
        pz[i] = unicode(mo.get(n,''))
    pz[0] = '/'.join( [x+'/'+y for (x,y) in [('ii','ok')] + mo.items() if x not in ('echoarea','date','msgfrom','addr','msgto','subj','msg')] )
    return '\n'.join(pz) + mo.msg


def get_msgs(msglist):
    out = []
    for h in msglist:
        msg = raw_msg(h)
        if msg: out.append( _parze(msg) )
    return out

def get_msg(msgid):
    out = get_msgs([msgid])
    return out[0] if out else sx.mydict(msg='no message',date=0)

def raw_msg(h):
    if not flt.msg_flt(h): return ''
    try:
        return open('msg/%s' % h).read().decode('utf-8')
    except:
        return ''

def new_msg(obj,rh=None):
    s = _out(obj).encode('utf-8')
    h = rh or sx.hsh(s)
    if len(s) < 65536:
        open('msg/%s' % h,'wb').write(s)
        return h

def get_echoarea(name):
    if not flt.echo_flt(name): return []
    try:
        return open('echo/%s' % name).read().splitlines()
    except:
        return []

def echoareas(names):
    out = ''
    for ea in names:
        out += ea + '\n'
        ge = get_echoarea(ea)
        if ge: out += '\n'.join(ge) + '\n'
    return out

def echoarea_count(name):
    return len(get_echoarea(name))

def load_echo():
    echoareas = open('list.txt').read().splitlines()
    return [(x,echoarea_count(x)) for x in echoareas]

def msg_to_echoarea(msgid,echoarea):
    if echoarea: open('echo/%s' % echoarea,'ab').write(msgid + '\n')


def mk_jt(mh,mb,nc=True):
    return mh + ':' + b64c(mb,nc)

def un_jt(txt):
    obj = txt.split(':',1)
    return (obj[0],  b64d(obj[1]) )

def ins_fromjt(n):
    (o,m) = un_jt(n)
    if not raw_msg(o):
        mo = _parze(m)
        mkmsg(mo,o)
    return o

def parse_jt(dta):
    for n in dta.splitlines():
        ins_fromjt(n)

def toss(msgfrom,addr,tmsg):
    lines = b64d(tmsg).decode('utf-8').splitlines()
    if flt.echo_flt(lines[0]):
        mo = sx.mydict(date=sx.gts(),msgfrom=msgfrom,addr=addr,echoarea=lines[0],msgto=lines[1],subj=lines[2],msg='\n'.join(lines[4:]))
        return mo

def mkmsg(obj,rh=None):
    if not flt.echo_flt(obj.echoarea): return
    if rh and not flt.msg_flt(rh): return
    if len(obj.msg) > 64099: return
    h = new_msg(obj,rh)
    if h:
        msg_to_echoarea(h,obj.echoarea)
        return h
