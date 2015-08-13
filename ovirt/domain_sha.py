#!/usr/bin/python
import hashlib
from optparse import OptionParser

if __name__  == "__main__":
    parser = OptionParser()
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("Missing metadata file")
    f = open(args[0], "r")
    mds = {}
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        try:
            key,value = line.split('=', 1)
            if key == '_SHA_CKSUM':
                continue
            mds[key] = value
        except Exception, e:
            continue
    f.close()
#print mds
csum = hashlib.sha1()
keys = mds.keys()
keys.sort()
for key in keys:
    value = mds[key]
    line = "%s=%s" % (key, value)
    csum.update(line)
print(csum.hexdigest())
