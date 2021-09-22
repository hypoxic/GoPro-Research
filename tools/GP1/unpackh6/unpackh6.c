/*
 * Break the Socionext Milbeaut SC2000 firmware into sections
*/

#include <ctype.h>
#include <dirent.h>
#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdarg.h>
#include <stddef.h>
#include <string.h>
#include <strings.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>
#include <utime.h>
#include <time.h>
#include <sys/stat.h>

#define MAGIC_KEY1	0x424c494d
#define MAGIC_KEY2	0x54554145

#define NAMELEN		0x74
#define OUTPUT_DIR  "output"

#define MAGIC_KEY	0x66FC328A
#define FWMAGIC_KEY	0x47504657

int GetNextFile(FILE *fbinary);
int SaveNextSection( FILE *fbinary);
int validatefw(FILE *fvalidate,FILE *fbinary);

uint32_t fileCRC(FILE *f,size_t offset,size_t size);

int main(int argc, char **argv)
{
    FILE 		*fbinary=0,*fvalidate=0;
    int 		nElements,i;
    char 		strUpData[512];
    char 		strUpVal[512];
	    
    printf("GoPro HERO6 Unpack Binaries - Hypoxic\nPass in the directory\n");
    
    if(argc != 2){
    	printf("Usage: %s <UPDATE directory>\n",argv[0] );
    	return -1;
    }
    
    sprintf(strUpVal,"%s\\CAMFWV.bin",argv[1]);	
    sprintf(strUpData,"%s\\DATA.bin",argv[1]);	
    	
    fbinary = fopen(strUpData,"rb"); 
    fvalidate = fopen(strUpVal,"rb"); 
    
    if (fbinary==NULL || fvalidate == NULL) {
    	printf ("Error opening UPDATE location, is %s correct?",argv[1]);
    	return EXIT_FAILURE;
    }
    else{
    	if(validatefw(fvalidate,fbinary)==EXIT_FAILURE)
    		return EXIT_FAILURE;
    	
	    // Make the directory for the outputs
	    struct stat st;
	    if (stat(OUTPUT_DIR, &st) == -1) {
	    	mkdir(OUTPUT_DIR);
		}
		
		nElements =0;
	    
	    while(SaveNextSection(fbinary) == EXIT_SUCCESS){
	    	nElements++;	
	    }
	    
	    printf("%d files created\n", nElements);
			
	    if(fbinary)
	        fclose(fbinary);
	}
        
    return EXIT_SUCCESS;
}

int validatefw(FILE *fvalidate,FILE *fbinary){
	uint32_t	magickey;
	char		verstr[9];
	uint32_t	crc_expected,crc_calc,binlen;
		
	if(fread(&magickey,sizeof(magickey),1,fvalidate)){
		if(magickey != FWMAGIC_KEY){
			printf("FW validation magic key is not correct!\n");
		}
		else{
			//read the version
			fseek(fvalidate,0x14,SEEK_SET);
			fread(&verstr,8,1,fvalidate);
			verstr[8] = '\0';
			
			// get the crc
			fseek(fvalidate,0x24,SEEK_SET);
			fread(&crc_expected,sizeof(crc_expected),1,fvalidate);
			
			//seek to the end to find size
			fseek(fbinary, 0L, SEEK_END);
			binlen = ftell(fbinary);
			
			// calc crc
			crc_calc = fileCRC(fbinary,0,binlen);
			
			fseek(fbinary,0L, SEEK_SET);
			
			if(crc_calc == crc_expected){
				printf("GoPro Firmware Version %s found with valid CRC of %08X\n",verstr,crc_calc);
				return EXIT_SUCCESS;
			}else{
				printf("GoPro Firmware Version %s found. INVALID CRC of %08X expected %08X\n",verstr, crc_calc, crc_expected);	
			}
				
		}
		
	}
    
	return EXIT_FAILURE;
}

int SaveNextSection(FILE *fbinary){
	uint16_t    volid,voltype;
    uint32_t	vol_unknown;
    uint32_t	magickey1,magickey2,volsize;
    char		fname[40];

	uint8_t 	*buffer;
	FILE 		*fout;
	size_t 		r;
    
	if (feof(fbinary)){
		printf("end of file reached\n");
		return EXIT_FAILURE;	
	}
		
    if(!fread(&magickey1,sizeof(magickey1),1,fbinary))
    	return EXIT_FAILURE;
    
    if(!fread(&magickey2,sizeof(magickey2),1,fbinary))
    	return EXIT_FAILURE;
    
    if(!fread(&voltype,sizeof(voltype),1,fbinary))
    	return EXIT_FAILURE;
    
    if(!fread(&volid,sizeof(volid),1,fbinary))
    	return EXIT_FAILURE;
    
    if(!fread(&volsize,sizeof(volsize),1,fbinary))
    	return EXIT_FAILURE;
    
    if(magickey1 != MAGIC_KEY1){
    	printf("magic key1 is not %x, read %x",MAGIC_KEY1, magickey1);	
    	return EXIT_FAILURE;
    }
   
    if(magickey2 != MAGIC_KEY2){
    	printf("magic key2 is not %x, read %x",MAGIC_KEY2, magickey2);	
    	return EXIT_FAILURE;
    } 	 
    
	// create the file name
	sprintf(fname,"%s\\sector%02d.bin",OUTPUT_DIR,volid);

    printf("%s id: %02d type %d of size %d\n",fname,volid, voltype, volsize);	

	// create a read buffer
	buffer = malloc(volsize);
	
	if(!buffer){
		printf("malloc of sector failed\n");
		return EXIT_FAILURE;	
	}
	
	//read in the sector
	if(fread(buffer,1,volsize,fbinary) != volsize){
		printf("Read size incorrect!\n");	
		return EXIT_FAILURE;	
	}
	
	if((fout = fopen(fname,"wb")) == NULL){
		printf("creating %s failed\n",fname);
		return EXIT_FAILURE;		
	}else{
		if(fwrite(buffer,1,volsize,fout) != volsize){
			printf("Write size incorrect!\n");	
			return EXIT_FAILURE;	
		}
	}

	// skip to the next
    //fseek(fbinary, volsize, SEEK_CUR);
    
	return EXIT_SUCCESS;
}

extern uint32_t crc32(uint32_t crc, const void *buf, size_t size);

/*

*/
uint32_t fileCRC(FILE *f,size_t offset,size_t size){
	char *buffer;
	size_t r;
	
	unsigned long crc = 0L;
	
	fseek(f,offset, SEEK_SET);

	buffer = malloc(size);
	if(!buffer){
		printf("malloc failed\n");
		return 0;	
	}
	
	if(fread(buffer,1,size,f) == size)
		crc= crc32(crc,buffer,size);
	else
		printf("sizes don't match\n");
	
	free(buffer);
		
	return crc;
}

/*
*/
void makefolder(char *filepath){
	struct stat st;
    char* 	pch;
    char path[200];
    char *f;
    char dir[200];
    char l;
     
    f = filepath;
    pch = strchr(f,'/');
    
    while(pch!=NULL){
    	l = pch-f;
    	memcpy(dir,f,l);
    	dir[l] = '\0';
    	
    	sprintf(path,"%s/%s/",OUTPUT_DIR,dir);
    	// just call it	
    	mkdir(path);
    	
    	f+=l+1;
    	pch = strchr(f,'/');
    }
}

/*
*/
int GetNextFile(FILE *fbinary){
	int i;
	uint32_t	l,len,crc,offset;
    char 		name[NAMELEN];
    char		path[200];
    fpos_t 		position;
    uint8_t		*buf;
    FILE		*fout;
    char* 		p;
	
	if((i = fread(&name,NAMELEN,1,fbinary)) <= 0)
    	return EXIT_FAILURE;
    
    if(i == NAMELEN)
    	name[NAMELEN-1] = '\0';

	if(!fread(&offset,sizeof(offset),1,fbinary))
		return 0;

    if(!fread(&len,sizeof(len),1,fbinary))
    	return 0;
	
	if(!fread(&crc,sizeof(crc),1,fbinary))
		return 0;
	
    // create the directory if we need to
    makefolder(name);
		
    sprintf(path,"%s/%s",OUTPUT_DIR,name);
    printf("%s (%d bytes) %08x\n",name, len, crc);	
    
    // create memory
    if((buf = malloc(len)) <= 0){
    	printf("malloc\n");
    	return 0;
	}
	
	// point to file in memory
	fgetpos (fbinary, &position);

	if(fseek(fbinary, (long int)offset, SEEK_SET)!=0)
		printf("seek to %x failed\n",offset);
	
	// read it
	if((l=fread(buf,1,len,fbinary)) != len){
		printf("fread buffer of %x failed, read %x\n",len,l);
		return 0;
	}
	
	//create file
	fout = fopen(path,"wb");
	
	if(fout <= 0){
		printf("fout failed to create!\n");
		return 0;
	}
	
	if((l = fwrite(buf,1,len,fout)) != len){
		printf("write failed write %x, expected %x\n",l,len);
		return 0;	
	}
	
	// write it
	fclose(fout);
	
	// free memory
	free(buf);
	
	// reset the  read pointer
	fsetpos (fbinary, &position);
	
	return 1;
	//return len;
}