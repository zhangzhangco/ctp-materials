#!/usr/bin/env python
#
# dsig_extract.py -- Extract certificates from an XML signature
#
# $Id$
#
from __future__ import print_function

from dsig_cert import dsig_certificate_set
import sys


def usage():
    sys.stderr.write("usage: dsig_extract.py [-p <prefix>] <xml-file>\n")
    sys.exit(1)


def main():
    prefix = 'xmldsig_cert_'

    if len(sys.argv) < 2:
        usage()

    if sys.argv[1] == '-p':
        if len(sys.argv) < 4:
            usage()
        prefix = sys.argv[2]
        filename = sys.argv[3]
    else:
        filename = sys.argv[1]

    try:
        with open(filename) as handle:
            xml_doc = handle.read()

        cert_set = dsig_certificate_set(xml_doc)
        cert_set.write_certs(prefix=prefix)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()

#
# end dsig_extract.py
#
