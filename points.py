# -*- coding: utf-8 -*-

import hashlib, random

def sha(s):
    return hashlib.sha256(s).hexdigest()[:16]

def _salt():
    return str(random.randint(1,99999999))

def save_point(phash,u):
    open('points.txt','a').write('%s:%s\n' % (phash,u))

def check_hash(s):
    p = open('points.txt').read().splitlines()
    for i,n in enumerate(p,1):
        ud = n.split(':',1)
        if ud[0] == s: return ud[1].decode('utf-8'),i
    return '', None

if __name__ == '__main__':
    import sys
    user = ' '.join(sys.argv[1:])
    if user:
        phash = sha(user+_salt())
        save_point(phash,user)
        print user; print phash
