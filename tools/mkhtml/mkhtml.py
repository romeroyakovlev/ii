# -*- coding: utf-8 -*-

import codecs, os, bottle

class df(dict):
    def __getattr__(self, key):
        return self.get(key,'')

def get_echoarea(name):
    try: return open('echo/%s' % name).read().splitlines()
    except: return ''

def _parz(msg):
    pz = msg.splitlines()
    mo = dict()
    optz = pz[0].split('/')
    mo.update( dict(zip(optz[::2],optz[1::2])) )
    for i,n in enumerate(('echoarea','date','msgfrom','addr','msgto','subj'),1):
        mo[n] = pz[i]
    mo['msg'] = '\n'.join(pz[8:])
    mo['date'] = int(mo['date'])
    return mo


for ea in os.listdir('echo'):
    t = ea.rsplit('.',1)
    if len(t) > 1 and t[1].isdigit():
        j = [(m,df(_parz(codecs.open('msg/%s' % m,'r','utf-8').read()))) for m in get_echoarea(ea) or []]
        codecs.open('html/%s.html' % ea,'w','utf-8').write(bottle.template('tpl.tpl',j=j,ea=ea))
