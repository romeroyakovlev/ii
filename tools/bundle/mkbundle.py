import api, sys

# mkbundle.py 5VnWrvebjUfA5DDgfs6p 6Dy6jfxHAhM3XFrqaMe3 > 1.jt
# mkbundle.py ii.test.2014:6Dy6jfxHAhM3XFrqaMe3 > 2.jt
# mkbundle.py ii.test.2014:10 > 3.jt

out = ''

def qua(ea,s):
    items =  api.get_echoarea(ea)
    if len(s) < 6 and s.isdigit():
        return items[-int(s):]
    else:
        if not s in items: return items
        return items[items.index(s)+1:]


def parse_echos(el):
    echos = el.split('/')
    pool = []
    for ea in echos:
        if ':' in ea:
            items = qua(*ea.split(':',1))
        else:
            items = api.get_echoarea(ea)
        for x in items:
            if not x in pool:
                pool.append(x)
    return pool

def get_bundle_msg(n):
    return api.mk_jt(n,api.raw_msg(n)) + '\n'

def get_bundle_echo(n):
    lo = ''
    for x in parse_echos(n):
        lo += api.mk_jt(x,api.raw_msg(x)) + '\n'
    return lo



for n in sys.argv[1:]:
    if '.' in n:
        out += get_bundle_echo(n)
    else:
        out += get_bundle_msg(n)

print out
