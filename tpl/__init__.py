# -*- coding: utf-8 -*-

import api, api.sx as sx, api.flt as flt, points, rssg
from api.bottle import *

def allstart():
    ip=request.headers.get('X-Real-Ip') or request.environ.get('REMOTE_ADDR')
    local.r = sx.mydict(url='http://%s.ru/' % YOURURL,ua=request.headers.get('User-Agent'),ip=ip,kuk=sx.mydict(request.cookies),fz=sx.mydict(request.forms),getl=sx.mydict(request.GET),NODE=NODE)
    local.r.auth = local.r.kuk.auth

def _msg(o,ml):
    allstart()
    if o == 'msg':
        mo = api.get_msg(ml) + {'msgid':ml}
        local.r.page_title =  mo.subj + ' @ ' + mo.echoarea
        lst = [mo]
    elif o == 'lst':
        lst=[api.get_msg(n) + {'msgid':n} for n in ml.split('/')]
        local.r.page_title = u'Список сообщений'
    return template('tpl/msg.html',lst=[mo] if o != 'lst' else lst,r=local.r)


@route('/')
def start_page():
    allstart()
    lst=[(e,api.get_echoarea(e)) for e,c in api.load_echo()]
    local.r.page_title = u'ii : ваше домашнее фидо'
    return template('tpl/index.html',r=local.r,lst=lst)

@route('/rss/<echo>.<year:int>')
def rss_echo(echo,year):
    response.set_header('content-type','application/rss+xml; charset=utf-8')
    return rssg.gen_rss('%s.%s' % (echo, year),YOURURL)

@route('/reply/<ea>/<repto>')
def index_list(ea,repto):
    allstart()
    if repto and repto != '-': 
        local.r.repto = repto
        local.r.rmsg = api.get_msg(repto)
    if not flt.echo_flt(ea): return ea
    local.r.page_title = u'message to ' + ea
    return template('tpl/mform.html',r=local.r,ea=ea)

@route('/<echo>.<year:int>')
def index_list(echo,year):
    allstart()
    ea = '%s.%s' % (echo,year)
    if not flt.echo_flt(ea): return ea
    local.r.update(page_title=ea,echolist=api.load_echo(),ea=ea)
    return template('tpl/echoarea.html',r=local.r,j=api.get_echoarea(ea))

@post('/a/newmsg/<ea>')
def msg_post(ea):
    allstart()
    ufor = request.forms.msgfrom.encode('utf-8')
    if not flt.echo_flt(ea): return ea
    if not local.r.fz.msg or not local.r.fz.subj: return local.r.fz.subj
    uname, uaddr = points.check_hash(ufor or local.r.auth)
    if uaddr:
        mo = sx.mydict()
        for _ in ('subj', 'msg', 'repto'):
            mo[_] = local.r.fz[_].decode('utf-8')
        mo['msgfrom'] = uname
        mo['msg']=mo['msg'].replace('\r\n','\n')
        mo.update(addr='%s,%s' % (NODE, uaddr),msgto=request.forms.msgto,echoarea=ea)
        h = api.point_newmsg(mo)
        if not h: return 'bad message'
    else:
        return 'no auth'
    redir = local.r.fz.goback or '/%s' % ea
    if ufor:
        response.set_cookie('auth',ufor,path='/',max_age=7776000)
        return ('<html><head><meta http-equiv="refresh" content="0; %s" /></head><body></body></html>' % redir)
    else:
        redirect (redir)

@route('/h/logout')
def logout_page():
    allstart()
    response.set_cookie('auth','',path='/',max_age=7776000)
    return ('<html><head><meta http-equiv="refresh" content="0; /" /></head><body></body></html>')

@route('/h/showhash')
def show_my_hash():
    allstart()
    return local.r.auth

@route('/s/<filename:path>')
def new_style(filename):
    return static_file(filename,root='./s')


@route('/data/<msgid>')
def data_render(msgid):
    mo = api.get_msg(msgid)
    if mo.subj.startswith('bindata::'):
        response.set_header ('content-type', mo.subj[9:].strip())
        return api.b64d( mo.msg )
    else:
        return 'no data'

@route('/q/<msglst:path>')
def msg_qpage(msglst):
    return _msg('lst',msglst)

@route('/<msghash:re:[^/]{20}>')
def msg_page(msghash):
    return _msg('msg', msghash)
