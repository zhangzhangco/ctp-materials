#!/usr/bin/env python
#
# dsig_cert.py -- Re-order certificates in an XML signature
#
# NOTE: This program requires Python 2.7 or greater
#
# $Id$
#
from __future__ import print_function

import sys, re
from subprocess import Popen, PIPE
import xml.etree.ElementTree as ET


# regular expressions for use below
dnQualifier_re = re.compile('dnQualifier[ ]?=[ ]?["]?([\\w+/]+=)["]?')

NS = {
    "dsig": "http://www.w3.org/2000/09/xmldsig#"
}


#
def get_dnq_type(pem_text, field):
    """Extract the dnQualifier value for the given certificate and common name."""
    handle = Popen(['/usr/bin/openssl', 'x509', '-noout', '-{0:s}'.format(field)],
                   stdin=PIPE, stdout=PIPE)
    name_data, _ = handle.communicate(pem_text.encode('utf-8'))
    name_text = name_data.decode("utf-8")

    if handle.returncode != 0:
        raise Exception("No X509Certificate element in {0}".format(pem_text))

    dnq = dnQualifier_re.search(name_text.replace('\\', ''))
    if not dnq:
        raise Exception("Error retrieving dnQualifier from {0}.".format(field))

    return dnq.group(1)

#
def PEMify(base64_text):
    """ create canonical PEM lines from any base64 input"""
    in_text = re.sub('[\r\n]', '', base64_text)
    idx = 0
    end = len(in_text)
    retval = ''
    while idx < end:
        retval += in_text[idx:idx+64] + '\n'
        idx += 64

    return retval

#
class dsig_certificate_set:
    """An object for manipulating XML Signature certificates."""
    def __init__(self, xml_doc):
        self.root = ET.fromstring(xml_doc)

        self.X509Data_list = []
        for data in self.root.findall(".//dsig:Signature/dsig:KeyInfo/dsig:X509Data", NS):
            cert_elem = data.find("./dsig:X509Certificate", NS)
            if cert_elem is not None and cert_elem.text:
                cert = "-----BEGIN CERTIFICATE-----\n{0:s}-----END CERTIFICATE-----\n".format(PEMify(cert_elem.text.strip()))
                self.X509Data_list.append({
                    "subject_dnq": get_dnq_type(cert, "subject"),
                    "issuer_dnq": get_dnq_type(cert, "issuer"),
                    "pem_cert": cert,
                    "data_element": data
                })
        if not len(self.X509Data_list):
            raise Exception("Document does not contain (XML digital signature conformant) X.509 certificates.")


    def order_by_dnq(self):
        """Arrange certificates in leaf-root order."""
        root_x509 = None
        issuer_map = {}

        for x509_data in self.X509Data_list:
            if x509_data['subject_dnq'] == x509_data['issuer_dnq']:
                if root_x509:
                    raise Exception("Certificate list contains multiple roots.")
                root_x509 = x509_data
            else:
                issuer_map[x509_data['issuer_dnq']] = x509_data

        if not root_x509:
            raise Exception("Self-signed root certificate not found.")

        tmp_list = [root_x509];
        try:
            key = tmp_list[-1]['subject_dnq']
            next = issuer_map.get(key)
            while next:
                tmp_list.append(next)
                key = tmp_list[-1]['subject_dnq']
                next = issuer_map.get(key)
        except:
            pass

        if len(self.X509Data_list) != len(tmp_list):
            raise Exception("Certificates do not form a complete chain.")

        tmp_list.reverse()
        self.X509Data_list = tmp_list
        return self


    def write_certs(self, prefix='cert_set_'):
        """Write PEMcertificates to files using the optional filename prefix value."""
        for count, x509_data in enumerate(self.X509Data_list):
            filename = "{0:s}{1:d}.pem".format(prefix, count + 1)
            with open(filename, 'w') as handle:
                handle.write(x509_data['pem_cert'])


    def __repr__(self):
        key_info = self.root.find(".//dsig:Signature/dsig:KeyInfo", NS)
        if key_info is not None:
            key_info.clear()
            for cert in self.X509Data_list:
                key_info.append(cert["data_element"])

        return ET.tostring(self.root, encoding="utf-8").decode('utf-8')


#
if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write("usage: dsig_cert.py <xml-file>\n")
        sys.exit(1)

    try:
        with open(sys.argv[1]) as handle:
            xml_doc = handle.read()

        cert_set = dsig_certificate_set(xml_doc)
        cert_set.order_by_dnq()
        print(cert_set)
    except Exception as e:
        print(e)

#
# end dsig_cert.py
#
