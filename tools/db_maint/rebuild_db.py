import os

msgs = os.listdir('msg')
for h in msgs:
    if os.path.getsize('msg/%s' % h) == 0:
        os.remove('msg/%s' % h)
        msgs.remove(h)

echoes = os.listdir('echo')

for ea in echoes:
    passed = []
    echo = open('echo/%s' % ea).read().splitlines()
    for h in echo:
        if h in msgs:
            msgs.remove(h)
            passed.append(h)
    if passed != echo:
        open('echo/%s' % ea,'w').write('\n'.join(passed + ['']))

for h in msgs:
    os.remove('msg/%s' % h)