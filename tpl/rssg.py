import api, api.flt as flt, PyRSS2Gen, api.sx as sx, datetime


def gen_rss(ea,url,num):
    if not flt.echo_flt(ea): return ea
    msgs = [api.get_msg(n) + {'msgid': n} for n in reversed(api.get_echoarea_f(ea)[-num:])]
    items = [PyRSS2Gen.RSSItem(
        title=n.subj,description=sx.rend(n.msg),link='http://%s/%s#%s' % (url,ea,n.msgid),
        guid='http://%s/%s#%s' % (url,ea,n.msgid),
        pubDate=datetime.datetime.fromtimestamp(n.date)
    ) for n in msgs ]
    rssout = PyRSS2Gen.RSS2(title=ea,link='http://%s/%s' % (url,ea),description='Echoarea: %s' % ea,
    lastBuildDate=datetime.datetime.now(),items=items)
    return rssout.to_xml('utf-8')
