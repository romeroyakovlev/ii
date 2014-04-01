# -*- coding: utf-8 -*-

def sp(s):
    pre = 0; code = 0; txt = ''
    for n in s.splitlines():
        if n == '====' and pre == 0:
            txt += u'</p>====<pre>'
            pre = 1
        elif n == '====' and pre == 1:
            if code == 1: txt += '</code>'
            txt += u'</pre>====<p>\n'
            pre = 0; code = 0
        elif n.startswith('====[') and n.endswith(']===='):
            txt += u'</p>====[%s]====\n<pre><code class="prettyprint lang-%s">' % (n[5:-5],n[5:-5].strip())
            code = 1; pre = 1
        elif pre == 1:
            txt += u'%s\n' % n
        else:
            txt += u'%s\n' % _ac(n)
    if code == 1: txt += '</code>'
    if pre == 1: txt += '</pre>'
    return txt

def _ac(t):
    o = t
    if o.rstrip().startswith('&gt;'):
        o = u'<em style="color:green">%s</em>\n' % o
    if 'http://' in o:
        o = _btn(o,'http://')
    if 'https://' in o:
        o = _btn(o,'https://')
    if 'ii://' in o:
        o = _btn(o,'ii://')
    return o


def _btn(s,tag):
    k = s.split(tag)
    buf = k[0]
    for x in k[1:]:
        endl = x.split(' ',1)
        xl = None
        for eol in '.,:':
            if endl[0].endswith(eol):
                xl = _settag(endl[0][:-1],tag) + eol + ' ' + ' '.join(endl[1:])
        if xl is None: xl = _settag(endl[0],tag) + ' ' + ' '.join(endl[1:])
        buf += xl
    return buf


def _settag(s,tag):
    if tag == 'http://' or tag == 'https://':
        return u'<a href="%s%s"><i class="fa fa-%s"></i>%s%s</a>' % (tag,s,'link' if tag == 'http://' else 'lock', tag,s)
    elif tag == 'ii://':
        endl = s.rsplit('.',1)
        if len(endl)>1 and endl[1].isdigit(): icon = 'plane'
        else: icon = 'envelope'
        return u'<a href="/%s"><span class="radius label success"><i class="fa fa-%s"></i> %s</span></a>' % (s,icon,s)
