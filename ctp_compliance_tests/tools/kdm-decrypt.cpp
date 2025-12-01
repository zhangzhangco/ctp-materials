//
// kdm-decrypt.cpp -- decrypt and display KDM EncryptedKey elements
//
// $Id$
//
// This program requires the Xerces-c XML, XMLSecurity, OpenSSL
// and asdcplib libraries. To build:
//
// c++ -o kdm-decrypt kdm-decrypt.cpp 
//     -lxerces-c -lxml-security-c -lkumu -lcrypto
//

#include <KM_util.h>
#include <KM_fileio.h>
#include <ctype.h>
#include <iostream>
#include <string>
#include <openssl/pem.h>
#include <xercesc/util/OutOfMemoryException.hpp>
#include <xercesc/parsers/XercesDOMParser.hpp>
#include <xercesc/framework/MemBufInputSource.hpp>
#include <xsec/framework/XSECProvider.hpp>
#include <xsec/framework/XSECException.hpp>
#include <xsec/enc/XSECCryptoException.hpp>
#include <xsec/enc/OpenSSL/OpenSSLCryptoKeyRSA.hpp>

XERCES_CPP_NAMESPACE_USE
using std::cout;
using std::cerr;
using std::endl;
using namespace Kumu;

const size_t KeyType_Length = 4;
const size_t DateTime_Length = 25;
const ui32_t X509Thumbprint_Length = 20;

// A structure to hold key block data retrieved during a decrypt operation.
struct S430_2_KeyBlock
{
  byte_t CipherDataID[UUID_Length];
  byte_t SignerThumbprint[X509Thumbprint_Length];
  byte_t CPLId[UUID_Length];
  byte_t KeyType[KeyType_Length];
  byte_t KeyId[UUID_Length];
  byte_t NotBefore[DateTime_Length];
  byte_t NotAfter[DateTime_Length];
  byte_t KeyData[SymmetricKey_Length];

  S430_2_KeyBlock() {
    memset(this, 0, sizeof(S430_2_KeyBlock));
  }

  std::string Dump() const;
};

std::string safe_char(char c) {
  char b[2] = {'*', 0};
  if ( isprint(c) ) b[0] = c;
  return b;
}

// Pretty-print key block data.
std::string
S430_2_KeyBlock::Dump() const
{
  using std::string;
  Kumu::Identifier<X509Thumbprint_Length> TmpThumbprint;
  UUID   TmpUUID;
  char   tmp_buf[64];
  string out_string;

  bin2hex(CipherDataID, UUID_Length, tmp_buf, 64);
  out_string = "    CipherDataID: " + string(tmp_buf);
  TmpThumbprint.Set(SignerThumbprint);
  out_string += "\nSignerThumbprint: " + string(TmpThumbprint.EncodeBase64(tmp_buf, 64));
  TmpUUID.Set(CPLId);
  out_string += "\n          CPL Id: " + string(TmpUUID.EncodeHex(tmp_buf, 64));
  TmpUUID.Set(KeyId);
  out_string += "\n          Key Id: " + string(TmpUUID.EncodeHex(tmp_buf, 64));
  out_string += "\n        Key Type: "
    + safe_char(KeyType[0]) + safe_char(KeyType[1])
    + safe_char(KeyType[2]) + safe_char(KeyType[3]);
  assert(DateTime_Length<64);
  tmp_buf[DateTime_Length] = 0;
  memcpy(tmp_buf, NotBefore, DateTime_Length);
  out_string += "\n      Not Before: " + string(tmp_buf);
  memcpy(tmp_buf, NotAfter, DateTime_Length);
  out_string += "\n       Not After: " + string(tmp_buf);
  bin2hex(KeyData, UUID_Length, tmp_buf, 64);
  out_string += "\n        Key Data: " + string(tmp_buf);
  out_string += "\n";
  return out_string;
}

// Given a KDM string and a parsed RSA key, decrypt the key blocks
// in the KDM and print them to stdout.
int
decrypt_kdm(const std::string& KDMDocument, EVP_PKEY* Target)
{
  assert(Target);

  XercesDOMParser* parser = new XercesDOMParser;
  parser->setDoNamespaces(true);
  parser->setCreateEntityReferenceNodes(true);

  try
    {
      MemBufInputSource xmlSource(reinterpret_cast<const XMLByte*>(KDMDocument.c_str()),
				  static_cast<XMLSize_t>(KDMDocument.length()),
				  "pidc_rules_file");
      parser->parse(xmlSource);
      int errorCount = parser->getErrorCount();
      if ( errorCount > 0 )
	{
	  cerr << "XML parse errors: " << errorCount << endl;
	  return -1;
	}
    }
  catch ( const OutOfMemoryException& )
    {
      cerr << "Out of memory exception." << endl;
    }
  catch ( const XMLException& e )
    {
      char* emsg = XMLString::transcode(e.getMessage());
      cerr << "An error occurred during parsing" << endl
	   << "   Message: " << emsg << endl;
	  XSEC_RELEASE_XMLCH(emsg);
    }
  catch ( const DOMException& e )
    {
      const unsigned int maxChars = 2047;
      XMLCh errText[maxChars + 1];
      
      cerr << endl
	   << "DOM Exception code is:  " << e.code << endl;
      
      if ( DOMImplementation::loadDOMExceptionMsg(e.code, errText, maxChars) )
	{
	  char* emsg = XMLString::transcode(errText);
	  cerr << "Message is: " << emsg << endl;
	  XSEC_RELEASE_XMLCH(emsg);
	}
    }
  catch (...)
    {
      cerr << "Unexpected XML parser error." << endl;
    }

  try
    {
      XSECProvider prov;
      OpenSSLCryptoKeyRSA* PrivateKey = new OpenSSLCryptoKeyRSA(Target);
      if ( PrivateKey == 0 )
	{
	  cerr << "Error reading private key" << endl;
	  return -1;
	}

      DOMDocument* doc = parser->getDocument();
      assert(doc);
      XENCCipher* cipher = prov.newCipher(doc);
      cipher->setKEK(PrivateKey);

      DOMNodeIterator* Iter =
	((DOMDocumentTraversal*)doc)->createNodeIterator(doc,
							 (DOMNodeFilter::SHOW_ELEMENT),
							 0,  false);
      assert(Iter);
      DOMNode* Node;
      int keys_accepted = 0;
      int key_nodes_found = 0;

      while ( (Node = Iter->nextNode()) != 0 )
	{
	  char* n = XMLString::transcode(Node->getLocalName());
	  if ( n == 0 ) continue;

	  if ( strcmp(n, "EncryptedKey") == 0 )
	    {
	      key_nodes_found++;
	      S430_2_KeyBlock CipherData;
	      ui32_t decrypt_len =
		cipher->decryptKey((DOMElement*)Node,
				   (byte_t*)&CipherData, sizeof(CipherData));

	      if ( decrypt_len == sizeof(CipherData) )
		{
		  keys_accepted++;
		  cout << CipherData.Dump();
		}
	      else if ( decrypt_len > 0 )
		cerr << "Unexpected cipher block length: " << decrypt_len << endl;
	      else
		cerr << "Error decoding key block: " << key_nodes_found << endl;
	    }

	  XSEC_RELEASE_XMLCH(n);
	}

      Iter->release();
    }
  catch (XSECException &e)
    {
      char* emsg = XMLString::transcode(e.getMsg());
      cerr << "Key decryption error: " << emsg << endl;
      XSEC_RELEASE_XMLCH(emsg);
      return -1;
    }
  catch (XSECCryptoException &e)
    {
      cerr << "Crypto error: " << e.getMsg() << endl;
      return -1;
    }
  catch (...)
    {
      cerr << "Unexpected decryption error." << endl;
    }

  delete parser;
  return 0;
}

//
int
main(int argc, const char** argv)
{
  if ( argc < 3 )
    {
      cerr << "USAGE: kdm-decrypt <kdm-file> <RSA-PEM-file>" << endl;
      return 2;
    }

  try
    {
      XMLPlatformUtils::Initialize();
      XSECPlatformUtils::Initialise();
    }
  catch(const XMLException& e)
    {
      char* emsg = XMLString::transcode(e.getMessage());
      cerr << "Xerces or XMLSecurity initialization error: " << emsg << endl;
      XSEC_RELEASE_XMLCH(emsg);
      return 3;
    }
  catch (...)
    {
      cerr << "Unexpected Xerces or XMLSecurity initialization error." << endl;
    }

  FILE* fp = fopen (argv[2], "r");
  if ( fp == 0 )
    {
      perror(argv[2]);
      return 4;
    }

  EVP_PKEY* Target = PEM_read_PrivateKey(fp, 0, 0, 0);
  fclose(fp);

  if ( Target == 0 )
    {
      cerr << "Error reading RSA key in file " << std::string(argv[2]) << endl;
      return 5;
    }

  std::string XML_doc;
  Result_t result = ReadFileIntoString(argv[1], XML_doc);
  if ( KM_FAILURE(result) )
    {
      cerr << "Error reading XML file " << std::string(argv[1]) << endl;
      return 6;
    }

  if ( decrypt_kdm(XML_doc, Target) != 0 )
    return 1;

  return 0;
}

//
// end kdm-decrypt.cpp
//
