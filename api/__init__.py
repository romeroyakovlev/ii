# -*- coding: utf-8 -*-

import base64, sx, flt

def b64c(s):
    return base64.b64encode(s)

def b64d(s):
    return base64.b64decode( s.replace('-','+').replace('_','/') )

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
    pz[0] = '/'.join( [x+'/'+y for (x,y) in [('ii','ok')] + mo.items() if x not in ('echoarea','date','msgfrom','addr','msgto','subj','msg') and y] )
    return '\n'.join(pz) + mo.msg

def ru(fn):
    try: return open(fn).read().decode('utf-8')
    except: return ''

def raw_msg(h):
    if not flt.msg_flt(h): return ''
    return ru('msg/%s' % h)

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

def get_echoarea_f(name):
    bl = set(ru('blacklist.txt').split())
    return [x for x in get_echoarea(name) if x not in bl]

#def get_echoarea_f(name,limit=0):
#    bl = set(ru('blacklist.txt').splitlines())
#    lst = [x for x in get_echoarea(name) if x not in bl][-limit:]

def echoareas(names):
    out = ''
    for ea in names:
        out += ea + '\n' + get_echoarea(ea,True)
    return out

def echoarea_count(name):
    return len(get_echoarea(name))

def _g(l):
    for n in l:
        x = n.strip().split(' ',1)
        if len(x) > 1:
            yield x
        elif len(x) == 1 and x[0]:
            yield x[0], ''

def load_echo(filter_star=False):
    lst = [x for x in _g(open('server.cfg').read().splitlines())]
    if filter_star:
        elst = [(x,echoarea_count(x),y) for (x,y) in lst[1:] if not x.startswith('*')]
    else:
        elst = [(x.lstrip('*'),echoarea_count(x),y) for (x,y) in lst[1:]]
    return [tuple(lst[0])] + elst


def mk_jt(mh,mb):
    return mh + ':' + b64c(mb.encode('utf-8'))

def parse_jt(dta):
    for n in dta.splitlines():
        o,m = txt.split(':',1)
        if not raw_msg(o):
            mo = _parze( b64d(m) )
            mkmsg(mo,o)

def toss(msgfrom,addr,tmsg):
    lines = b64d(tmsg).decode('utf-8').splitlines()
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

def _filter_msg_call(tags):
    try:
        import filter_msg
        return filter_msg.check(tags)
    except:
        return True

def point_newmsg(tags):
    mo = sx.mydict(date=sx.gts())
    mo.update(**tags)
    if _filter_msg_call(tags): return mkmsg(mo)
