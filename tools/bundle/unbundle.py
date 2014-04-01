import api, sys

# unbundle.py 1.jt 2.jt 3.jt

for n in sys.argv[1:]:
    api.parse_jt(open(n).read().strip())
