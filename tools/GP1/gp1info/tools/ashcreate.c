// gcc ashcreate.c -o ashcreate

/*
Convert a binary file to writel-commands
(C) 2010 Jeroen Domburg (jeroen AT spritesmods.com)

This program is free software: you can redistribute it and/or modify
t under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
	    
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
			    
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

// I compiled this with mingw   gcc ashcreate.c -o ashcreate.exe

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

char UsageString[] = \
"\nUsage: ashcreate <linkerscript> <binary_file.bin> <output_file.c>\n" \
"\t ashcreate file.lds go.bin gcontrol.c";

#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAXLEN 80

typedef struct
{
  char eval[MAXLEN];
  char dest[MAXLEN];
}parameters_t;

int main(int argc, char **argv) {
	FILE *ptr_binfile;
	FILE *ptr_outfile;
	unsigned int patch_addr;
	unsigned int evalfcn_addr;
				
	if(argc != 4){
		puts(UsageString);
	}
	else{
		parameters_t parms;
			
		if(parse_config (argv[1], &parms)){
			evalfcn_addr = (int)strtoul(parms.eval, NULL, 16);
			patch_addr    = (int)strtoul(parms.dest, NULL, 16);
		  	printf ("\nFound parameters Eval Location: 0x%08x, Patch entry: 0x%08x\n", evalfcn_addr, patch_addr);
		}		
		else
			exit(-1);
		
		/*		
		patch_addr   = strtoul(argv[1], NULL, 0);
		evalfcn_addr = strtoul(argv[2], NULL, 0);
		*/
		
		ptr_binfile=fopen(argv[2],"rb");
		if (!ptr_binfile)
		{
			printf("Unable to open input binary %s",argv[2]);
			exit(-1);
		}
		else{		
			long p;
			
			// Now create the output file
			ptr_outfile = fopen(argv[3], "wb");
			if(!ptr_outfile)
				printf("Unable to create output file: %s",argv[3]);
			else{
				fprintf(ptr_outfile, "// patch pairs\npatch[][] = {"); //  writel 0xc02c9664 0xc0020000
				fprintf(ptr_outfile, "{0x%08x,0x%08x}", evalfcn_addr, patch_addr); //  writel 0xc02c9664 0xc0020000
				
				while(!feof(ptr_binfile)) {
					p=fgetc(ptr_binfile);
					p|=fgetc(ptr_binfile)<<8;
					p|=fgetc(ptr_binfile)<<16;
					p|=fgetc(ptr_binfile)<<24;

					// write the file
					fprintf(ptr_outfile, ",\n{0x%08x,0x%08lx}", patch_addr, p);

					patch_addr+=4;
				}
				
			
				// Now call the eval!
				fputs("}\n",ptr_outfile);
				
				// close it and write it
				fclose(ptr_outfile);
			}
			
			fclose(ptr_binfile);
		}
	}
	
	exit(0);
}

//http://www.linuxquestions.org/questions/programming-9/read-parameters-from-config-file-file-parser-362188/

/*
 * trim: get rid of trailing and leading whitespace...
 *       ...including the annoying "\n" from fgets()
 */
char *
trim (char * s)
{
  /* Initialize start, end pointers */
  char *s1 = s, *s2 = &s[strlen (s) - 1];

  /* Trim and delimit right side */
  while ( ((isspace (*s2)) || *s2 == ';')  && (s2 >= s1) )
    s2--;
  *(s2+1) = '\0';

  /* Trim left side */
  while ( (isspace (*s1)) && (s1 < s2) )
    s1++;

  /* Copy finished string */
  strcpy (s, s1);
  
  return s;
}

/*
 * parse external parameters file
 *
 * NOTES:
 * - There are millions of ways to do this, depending on your
 *   specific needs.
 *
 * - In general:
 *   a) The client will know which parameters it's expecting
 *      (hence the "struct", with a specific set of parameters).
 *   b) The client should NOT know any specifics about the
 *      configuration file itself (for example, the client
 *      shouldn't know or care about it's name, its location,
 *      its format ... or whether or not the "configuration
 *      file" is even a file ... or a database ... or something
 *      else entirely).
 *   c) The client should initialize the parameters to reasonable
 *      defaults
 *   d) The client is responsible for validating whether the
 *      pararmeters are complete, or correct.
 */
int parse_config (char *str, parameters_t * parms)
{
  char *s, buff[256];
  FILE *fp = fopen (str, "r");
  if (fp == NULL)
  {
    printf ("LDS file failed to open\n");
    return 0;
  }

	printf ("Reading lds file...\n");
	parms->eval[0] = 0;
	parms->dest[0] = 0;
	

  /* Read next line */
  while ((s = fgets (buff, sizeof buff, fp)) != NULL)
  {
    /* Skip blank lines and comments */
    if (buff[0] == '\n' || buff[0] == '#')
      continue;

    /* Parse name/value pair from line */
    char name[MAXLEN], value[MAXLEN];
        
    s = strtok (buff, "=");
    if (s==NULL)
      continue;
    else{
      strncpy (name, s, MAXLEN);
      trim(name);
  	}
        
    s = strtok (NULL, "=");
    if (s==NULL)
      continue;
    else
      strncpy (value, s, MAXLEN);
    trim (value);

    /* Copy into correct entry in parameters struct */
    if (strcmp(name, "overwrite_loc")==0){ 
  		strncpy (parms->eval, value, MAXLEN);
  	}
    else if (strcmp(name, "patch_dest")==0){ 
  		strncpy (parms->dest, value, MAXLEN);
  	}
  }

  /* Close file */
  fclose (fp);
  
  if(parms->eval[0] == 0 || parms->dest[0] == 0)
  	return 0;
  else
  	return 1;
}

