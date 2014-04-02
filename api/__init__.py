# -*- coding: utf-8 -*-

import base64, zlib, sx, flt

def b64c(s,us):
    if us: return base64.b64encode(s)
    else: return base64.urlsafe_b64encode(zlib.compress(s))

def b64d(s,us):
    cnt = base64.b64decode( s.replace('-','+').replace('_','/') )
    if us: return cnt
    else: return zlib.decompress(cnt)

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

def raw_msg(h):
    if not flt.msg_flt(h): return ''
    try: return open('msg/%s' % h).read().decode('utf-8')
    except: return ''

def get_msg(h):
    txt = raw_msg(h)
    return _parze(txt) if txt else sx.mydict(msg='no message',date=0)

def get_echoarea(name,raw=False):
    if not flt.echo_flt(name): return '' if raw else []
    try:
        txt = open('echo/%s' % name).read()
        return txt if raw else txt.splitlines()
    except:
        return '' if raw else []

def echoareas(names):
    out = ''
    for ea in names:
        out += ea + '\n' + get_echoarea(ea,True)
    return out

def echoarea_count(name):
    return len(get_echoarea(name))

def load_echo():
    echoareas = open('list.txt').read().splitlines()
    return [(x,echoarea_count(x)) for x in echoareas]


def mk_jt(mh,mb,us=True):
    return mh + ':' + b64c(mb.encode('utf-8'),us)

def parse_jt(dta,us=True):
    for n in dta.splitlines():
        o,m = txt.split(':',1)
        if not raw_msg(o):
            mo = _parze( b64d(m,us) )
            mkmsg(mo,o)

def toss(msgfrom,addr,tmsg,us=True):
    lines = b64d(tmsg,us).decode('utf-8').splitlines()
    if flt.echo_flt(lines[0]):
        mo = sx.mydict(date=sx.gts(),msgfrom=msgfrom,addr=addr,echoarea=lines[0],msgto=lines[1],subj=lines[2],msg='\n'.join(lines[4:]))
        return mo

def mkmsg(obj,rh=None):
    if not flt.echo_flt(obj.echoarea): return
    if rh and not flt.msg_flt(rh): return
    s = _out(obj).encode('utf-8')
    h = rh or sx.hsh(s)
    if len(s) < 65536:
        open('msg/%s' % h,'wb').write(s)
        open('echo/%s' % obj.echoarea,'ab').write(h + '\n')
        return h

def point_newmsg(tags):
    mo = sx.mydict(date=sx.gts())
    mo.update(**tags)
    return mkmsg(mo)
