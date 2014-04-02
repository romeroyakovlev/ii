# -*- coding: utf-8 -*-

import api,points
from api.bottle import *

NODE='unnamed'
YOURURL='51t.ru'

@route('/list.txt')
def list_txt():
    response.set_header ('content-type','text/plain; charset=utf-8')
    return '\n'.join(['%s:%s:' % t for t in api.load_echo()])

@route('/<qp:re:z|u>/m/<h:path>')
def jt_outmsg(qp,h):
    response.set_header ('content-type','text/plain; charset=iso-8859-1')
    us = True if qp == 'u' else False
    lst = [x for x in h.split('/') if len(x) == 20]
    return '\n'.join( [api.mk_jt(x,api.raw_msg(x),us) for x in lst] )

@route('/u/e/<names:path>')
@route('/z/e/<names:path>')
def index_list(names):
    response.set_header ('content-type','text/plain; charset=utf-8')
    return api.echoareas(names.split('/'))

def _point_msg(pauth,tmsg,qp):
    msgfrom, addr = points.check_hash(pauth)
    if not addr: return 'auth error!'
    mo = api.toss(msgfrom,'%s,%s' % (NODE,addr),tmsg,True if qp == 'u' else False)
    if mo.msg.startswith('@repto:'):
        tmpmsg = mo.msg.splitlines()
        mo.repto = tmpmsg[0][7:]
        mo.msg = '\n'.join(tmpmsg[1:])
        # а ещё лучше - засунуть это в api.toss
    if len(mo.msg.encode('utf-8')) < 64100:
        h = api.point_newmsg(mo)
        if h:
            return 'msg ok:%s: <a href="/%s">%s</a>' % (h, mo.echoarea, mo.echoarea)
        else:
            return 'error:unknown'
    else:
        return 'msg big!'

@route('/<qp:re:z|u>/point/<pauth>/<tmsg>')
def point_msg_get(qp,pauth,tmsg):
    return _point_msg(qp,pauth,tmsg,qp)

@post('/<qp:re:z|u>/point')
def point_msg_get(qp):
    return _point_msg(request.POST['pauth'],request.POST['tmsg'],qp)

@route('/m/<msg>')
def get_msg(msg):
    response.set_header ('content-type','text/plain; charset=utf-8')
    return api.raw_msg(msg)

@route('/e/<echoarea>')
def get_echolist(echoarea):
    response.set_header ('content-type','text/plain; charset=utf-8')
    return api.get_echoarea(echoarea,True)

import tpl
tpl.YOURURL = YOURURL
tpl.NODE = NODE

run(host='127.0.0.1',port=62220,debug=False)
