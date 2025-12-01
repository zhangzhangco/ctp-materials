/*
 * j2c-scan.cpp -- parse j2c file and display data concerning it
 *
 * $Id$
 *
 * This program requires version 1.5.2 of the OpenJPEG
 * library. Furthermore, it requires the header files "openjpeg.h" and
 * "j2k.h" from its source distribution. Copy these headers to your
 * build directory. After doing so, execute the following to build:
 *  $ c++ -o j2c-scan j2c-scan.cpp -lopenjpeg
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "openjpeg.h"
#include "j2k.h"

static void
j2k_dump_cp (opj_image_t * image, opj_cp_t * cp)
{
  const char *s;
  int i, j;
  int step_size_pairs;
  printf ("coding parameters\n");
  if (cp->comment != NULL)
    {
      printf ("  coding comment: %p\n", cp->comment);
    }
  switch (cp->cinema)
    {
    case OFF:      s = "none";      break;
    case CINEMA2K_24:      s = "2k @ 24 fps";      break;
    case CINEMA2K_48:      s = "2k @ 48 fps";      break;
    case CINEMA4K_24:      s = "4k @ 24 fps";      break;
    default:      s = "unknown";      break;
    }
  printf ("  digital cinema profile: %s\n", s);
  switch (cp->rsiz)
    {
    case STD_RSIZ:      s = "standard";      break;
    case CINEMA2K:      s = "2k digital cinema";      break;
    case CINEMA4K:      s = "4k digital cinema";      break;
    default:      s = "unknown";      break;
    }
  printf ("  rsiz capabilities: %s\n", s);
  printf ("  pixel offset from top-left corner: (%d, %d)\n", cp->tx0,
	  cp->ty0);
  printf ("  tile width/height in pixels: (%d, %d)\n", cp->tdx, cp->tdy);
  printf ("  image width/height in tiles: (%d, %d)\n", cp->tw, cp->th);
  for (i = 0; i < cp->tw * cp->th; i++)
    {
      printf ("  tile #%d\n", i + 1);
      printf ("    coding style: %x\n", cp->tcps[i].csty);
      switch (cp->tcps[i].prg)
	{
	case LRCP:	  s = "Layer-Resolution-Component-Position";	  break;
	case RLCP:	  s = "Resolution-Layer-Component-Position";	  break;
	case RPCL:	  s = "Resolution-Position-Component-Layer";	  break;
	case PCRL:	  s = "Position-Component-Resolution-Layer";	  break;
	case CPRL:	  s = "Component-Position-Resolution-Layer";	  break;
	default:	  s = "unknown";	  break;
	}
      printf ("    progression order: %s\n", s);
      printf ("    POC marker flag: %d\n", cp->tcps[i].POC);
      printf ("    number of quality layers: %d\n", cp->tcps[i].numlayers);
      for (j = 0; j < cp->tcps[i].numlayers; j++)
	{
	  printf ("      rate for layer #%d: %.1f\n", j + 1,
		  cp->tcps[i].rates[j]);
	}
      printf ("    multi-component transform flag: %d\n", cp->tcps[i].mct);
      for (j = 0; j < image->numcomps; j++)
	{
	  printf ("    component #%d\n", j + 1);
	  printf ("      coding style: %x\n", cp->tcps[i].tccps[j].csty);
	  printf ("      number of resolutions: %d\n",
		  cp->tcps[i].tccps[j].numresolutions);
	  printf ("      code block width/height: (%d, %d)\n",
		  cp->tcps[i].tccps[j].cblkw, cp->tcps[i].tccps[j].cblkh);
	  printf ("      code block coding style: %x\n",
		  cp->tcps[i].tccps[j].cblksty);
	  printf ("      discrete wavelet transform identifier: %d\n",
		  cp->tcps[i].tccps[j].qmfbid);
	  printf ("      quantization style: %d\n",
		  cp->tcps[i].tccps[j].qntsty);
	  printf ("      number of guard bits: %d\n",
		  cp->tcps[i].tccps[j].numgbits);
	  step_size_pairs =
	    (cp->tcps[i].tccps[j].qntsty ==
	     J2K_CCP_QNTSTY_SIQNT) ? 1 : cp->tcps[i].tccps[j].numresolutions *
	    3 - 2;
	  printf ("      step size pairs: %d\n", step_size_pairs);
	  printf ("      region of interest shift: %d\n",
		  cp->tcps[i].tccps[j].roishift);
	}
    }
}

void
error_callback (const char *msg, void *client_data)
{
  FILE *stream = (FILE *) client_data;
  fprintf (stream, "[ERROR] %s", msg);
}

void
warning_callback (const char *msg, void *client_data)
{
  FILE *stream = (FILE *) client_data;
  fprintf (stream, "[WARNING] %s", msg);
}


int
main (int argc, char *argv[])
{
  char *filename;		/* name of the file to process */
  FILE *fp;			/* input file pointer */
  int file_length;		/* length of the input file */
  unsigned char *buffer = NULL;	/* in-memory buffer containing the input file */
  opj_cio_t *cio = NULL;	/* OpenJPEG wrapper around file buffer */
  opj_dparameters_t parameters;	/* decompression parameters */
  opj_dinfo_t *dinfo = NULL;	/* pointer to a JPEG-2000 decompressor */
  opj_event_mgr_t event_mgr;	/* manager of events' callback functions */
  opj_image_t *image = NULL;	/* pointer to the decoded image */

  memset (&event_mgr, 0, sizeof (opj_event_mgr_t));
  event_mgr.error_handler = error_callback;
  event_mgr.warning_handler = warning_callback;
  event_mgr.info_handler = NULL;

  /* establish default decoding parameters for JPEG-2000 codestreams */
  opj_set_default_decoder_parameters (&parameters);
  parameters.decod_format = 0;

  if (argc != 2)
    {
      fprintf (stderr, "USAGE: j2c-scan file.j2c\n");
      return 1;
    }
  filename = argv[1];
  strncpy (parameters.infile, filename, sizeof (parameters.infile) - 1);

  /* read the input file and put it in memory */
  fp = fopen (parameters.infile, "rb");
  if (fp == NULL)
    {
      perror ("fopen");
      return 2;
    }
  fseek (fp, 0, SEEK_END);
  file_length = (int) ftell (fp);
  fseek (fp, 0, SEEK_SET);
  buffer = (unsigned char *) malloc (file_length);
  fread (buffer, sizeof (unsigned char), file_length, fp);
  fclose (fp);

  /* decode the JPEG-2000 codestream */
  dinfo = opj_create_decompress (CODEC_J2K);
  opj_set_event_mgr ((opj_common_ptr) dinfo, &event_mgr, stderr);
  opj_setup_decoder (dinfo, &parameters);
  cio = opj_cio_open ((opj_common_ptr) dinfo, buffer, file_length);
  image = opj_decode (dinfo, cio);
  if (image == NULL)
    {
      fprintf (stderr, "ERROR -> j2c-scan: failed to decode image!\n");
      opj_destroy_decompress (dinfo);
      opj_cio_close (cio);
      free (buffer);
      return 1;
    }
  opj_cio_close (cio);
  free (buffer);

  /* display information about the image */
  j2k_dump_cp (image, ((opj_j2k_t *) dinfo->j2k_handle)->cp);

  /* free the memory */
  opj_destroy_decompress (dinfo);
  opj_image_destroy (image);

  return 0;
}
