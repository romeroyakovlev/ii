cfg = open('config.user').read().splitlines()
bonecho = open('bone.echo').read().strip()
el = open('echo/%s' % bonecho).read().splitlines()
lastbone = open('msg/%s' % el[-1]).read().splitlines()[8:]

if lastbone:
    open('bone.echo','w').write(lastbone[0])
    open('config.cfg','w').write('\n'.join(cfg+lastbone+['']))
