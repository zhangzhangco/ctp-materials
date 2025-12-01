/*
 * dc-thumbprint.c -- calculate certificate thumbprint of PEM-encoded
 *                    X.509 document per SMPTE 430-2
 *
 * $Id$
 *
 * This program requires OpenSSL. To build:
 *  $ cc -o dc-thumbprint dc-thumbprint.c -lcrypto
 */

#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <openssl/crypto.h>
#include <openssl/err.h>
#include <openssl/evp.h>
#include <openssl/pem.h>
#include <openssl/x509.h>


int
main(int argc, char* argv[])
{
    /* pointer to SHA-1 hash details */
    const EVP_MD *md = EVP_sha1();
    /* PEM source file pointer */
    FILE *fp = NULL;
    /* pointer to an X509 structure */
    X509 *x = NULL;
    /* pointer to DER-encoded TBSCertificate */
    unsigned char *p_tbs = NULL;
    /* length of DER-encoded TBSCertificate (p_tbs) */
    int tbs_len = 0;
    /* buffer for the message digest */
    unsigned char md_value[EVP_MAX_MD_SIZE];
    /* return value from digest calculation */
    int digest_rc = 0;
    /* buffer for base64 encoding of the message digest */
    char md_base64[EVP_MAX_MD_SIZE * 4 / 3 + 2];

    if (argc != 2)
      {
        fprintf(stderr, "Usage: dc-thumbprint cert-file.pem\n");
        return 1;
      }

    fp = fopen(argv[1], "r");
    if (fp == NULL)
      {
        fprintf(stderr, "ERROR: Cannot open %s: %s\n", argv[1], strerror(errno));
        return 2;
      }

    x = PEM_read_X509(fp, NULL, NULL, NULL);
    (void) fclose(fp);
    if (x == NULL)
      {
        ERR_print_errors_fp(stderr);
        return 3;
      }

    /* get the tbsCertificate as a DER string */
    tbs_len = i2d_re_X509_tbs(x, &p_tbs);
    X509_free(x);
    if (tbs_len <= 0)
      {
        ERR_print_errors_fp(stderr);
        return 4;
      }

    /* perform the message digest */
    digest_rc = EVP_Digest(p_tbs, tbs_len, md_value, NULL, md, NULL);
    OPENSSL_free(p_tbs);
    if (digest_rc == 0)
      {
        ERR_print_errors_fp(stderr);
        return 5;
      }

    /* perform the base64 encoding */
    (void) EVP_EncodeBlock((unsigned char *)md_base64, md_value,
                           EVP_MD_meth_get_result_size(md));

    printf("%s\n", md_base64);
    return 0;
}

/*
 * end dc-thumbprint.c
 */
