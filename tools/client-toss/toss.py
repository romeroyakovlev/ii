import api, api.sx as sx, sys, ww

MSGFROM='51t'
ADDR='lenina,1'

for f in sys.argv[1:]:
    txt = open(f).read()
    mo = api.toss(MSGFROM,ADDR,txt)
    if mo:
        if mo.msg.startswith('@repto:'):
            tmpmsg = mo.msg.splitlines()
            mo.repto = tmpmsg[0][7:]
            mo.msg = '\n'.join(tmpmsg[1:])
        h = ww.send_msg(mo)
        print '%s to %s' % ( h , mo.echoarea )
