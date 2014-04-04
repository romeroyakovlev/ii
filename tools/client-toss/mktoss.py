import sys, base64

for f in sys.argv[1:]:
    tx = open(f).read()
    ctx = base64.urlsafe_b64encode( (tx) )
    open(f + '.toss','w').write(ctx)
