import os, time

def raw_msg(h):
    try: return open('msg/%s' % h).read().decode('utf-8')
    except: return ''

def dateg(d,f):
    return time.strftime(f, time.gmtime(int(d)))

d = dict()

for n in os.listdir('msg'):
    txt = raw_msg(n)
    if txt:
        mdate = int(txt.splitlines()[2])
        ds = dateg(mdate,'%Y-%m-%d')
        d.setdefault(ds,0)
        d[ds] += 1

mi = max([y for x,y in d.items()])

for n,v in sorted(d.items()):
    print '%s %5d %s' % (n, v, '=' * (v*50/mi) )