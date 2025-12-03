#!/usr/bin/env python
#
# uuid_check.py -- Scan an XML file and see that all UUID values
#                  conform to RFC-4122
#
# $Id$
#
from __future__ import print_function

import sys, re

# regular expressions for use below
urn_uuid_re = re.compile('urn:uuid:([^<]*)')
uuid_re = re.compile('^[0-9a-f]{8}-[0-9a-f]{4}-\
([1-5])[0-9a-f]{3}-[8-9a-b][0-9a-f]{3}-[0-9a-f]{12}$', re.IGNORECASE)

#
def uuid_scan(text):
    uuid_list = []
    while text:
        match = urn_uuid_re.search(text)
        if not match: break

        uuid_val = match.group(1)
        text = text[match.end():]

        match = uuid_re.match(uuid_val)
        if not match:
            sys.stderr.write("urn:uuid: value is not an RFC-4122 UUID: %s\n" % (uuid_val))
            continue

        type = int(match.group(1)[0])
        if type not in (1, 4, 5):
            sys.stderr.write("Unexpected UUID type: %d for value %s\n" % (type, uuid_val))

        uuid_list.append(uuid_val)

    return uuid_list

#
#
if len(sys.argv) < 2:
    sys.stderr.write("usage: uuid_check.py <xml-file> [...]\n")
    sys.exit(1)

for filename in sys.argv[1:]:
    try:
        handle = open(filename)
        text = handle.read()
        handle.close()

    except Exception as e:
        print("{0}: {1}".format(filename, e))

    else:
        for uuid in uuid_scan(text):
            print("UUID: {0}".format(uuid))

#
# end uuid_check.py
#
