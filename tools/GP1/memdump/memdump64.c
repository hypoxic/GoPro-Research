/*
 * Modified from busybox devmem to read RTOS into a binary. 
 *
 * Compile: aarch64-linux-gnu-gcc memdump64.c  -o memdump64 -static
 * Note: busybox devmem 0x40200208 to determine end of RODATA
 * 
*/


/*
 * Licensed under GPLv2 or later, see file LICENSE in this source tree.
 *  Copyright (C) 2000, Jan-Derk Bakker (J.D.Bakker@its.tudelft.nl)
 *  Copyright (C) 2008, BusyBox Team. -solar 4/26/08
 */

//usage:#define devmem_trivial_usage
//usage:	"ADDRESS [WIDTH [VALUE]]"
//usage:#define devmem_full_usage "\n\n"
//usage:       "Read/write from physical address\n"
//usage:     "\n	ADDRESS	Address to act upon"
//usage:     "\n	WIDTH	Width (8/16/...)"
//usage:     "\n	VALUE	Data to be written"

#include <ctype.h>
#include <dirent.h>
#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
//#include <mntent.h>
//#include <netdb.h>
#include <setjmp.h>
#include <signal.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdarg.h>
#include <stddef.h>
#include <string.h>
#include <strings.h>
//#include <sys/ioctl.h>
#include <sys/mman.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/statfs.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <termios.h>
#include <time.h>
#include <unistd.h>
#include <utime.h>
#include <inttypes.h>

#define memread_t			unsigned int
#define READ_ELEMENT_SIZE 	sizeof(memread_t)
#define nBUFF_ELEMENTS		0x200
	
//int devmem(off_t target, unsigned width, uint64_t *read_result, uint64_t *writeval);	
	
int main(int argc, char **argv)
{
	FILE *fw;
	memread_t *rbuf,*rbuf_base;
	int i;
	
	void *map_base, *virt_addr;
	uint64_t read_result=0;
	uint64_t writeval = writeval; /* for compiler */
	unsigned page_size, mapped_size, offset_in_page,read_len;
	int fd;
	unsigned width = 8 * sizeof(int);
	uint64_t start, size;
	
	char filename[] = "/tmp/fuse_d/read.bin";
	
	printf("%s <start_address> <size>\n", argv[0]);
	printf("HERO11: Run devmem 0x40200208 for find out end of RODATA\n");
	
	if(argc != 3)
	{
	    printf("[ERROR] %s <start_address> <size>\n", argv[0]);
	    return -1;
	}
	    
	start = strtoull(argv[1], NULL, 16);
	size = strtoull(argv[2], NULL, 16);
	printf("Running %s [0x%" PRIx64  "] size:0x%" PRIx64  " with output to %s\n", argv[0], start, size, filename);
	
	mapped_size = size;
	read_len = (mapped_size+(READ_ELEMENT_SIZE*nBUFF_ELEMENTS-1))/(READ_ELEMENT_SIZE*nBUFF_ELEMENTS);

	fd = open("/dev/mem", (O_RDONLY | O_SYNC));
    
    #if 0	            
	mapped_size = page_size = getpagesize();
	
	if (offset_in_page + width > page_size) {
		/* This access spans pages.
		 * Must map two pages to make it possible: */
		mapped_size *= 2;
	}
	#endif
	
	page_size = getpagesize();
	offset_in_page = (unsigned)start & (page_size - 1);
	
	map_base = mmap(NULL,
			mapped_size,
			PROT_READ,
			MAP_SHARED,
			fd,
			start & ~(off_t)(page_size - 1));
	if (map_base == MAP_FAILED){
		printf("mmap failed");
		return EXIT_FAILURE;
	}

	virt_addr = (char*)map_base + offset_in_page;
	
	fw=fopen(filename, "wb");
	
	rbuf = (memread_t *)malloc(READ_ELEMENT_SIZE*nBUFF_ELEMENTS);
	if(rbuf == NULL){
		printf("malloc failed");
		return EXIT_FAILURE;
	}
	rbuf_base = rbuf;
	
	printf("Reading [0x%" PRIx64  "]-[0x%" PRIx64  "] = %d blocks, 0x%08x bytes\n",start, start + size, read_len, mapped_size);
	while(read_len--){
		for(i=0;i<nBUFF_ELEMENTS;i++){
			*rbuf = *(volatile uint32_t*)virt_addr;
			rbuf++;
			virt_addr+=4;
		}
		rbuf = rbuf_base;
			
		fwrite(rbuf,READ_ELEMENT_SIZE,nBUFF_ELEMENTS,fw);
	}
	
	printf("done\n");


	close(fd);
	fclose(fw);

	return EXIT_SUCCESS;
}


