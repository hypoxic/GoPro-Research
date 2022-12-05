/*
 * Modified from busybox devmem to read RTOS into a binary. 
 *
 * Compile: aarch64-linux-gnu-gcc memdisplay64.c  -o memdisplay64 -static
 * or for GP1   arm-linux-gnueabihf-gcc -Wall memdisplay64.c -o memdisplay -static
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

void DumpHex(const void* data, size_t size, uint32_t addr) {
	char ascii[17];
	size_t i, j;
	ascii[16] = '\0';
	for (i = 0; i < size; ++i) {
	    // print the address
	    if(!i || i%16 == 0)
	    {
	        printf("[%08x] ", addr);	        
	        addr += 16;
	    }
		printf("%02X ", ((unsigned char*)data)[i]);
		if (((unsigned char*)data)[i] >= ' ' && ((unsigned char*)data)[i] <= '~') {
			ascii[i % 16] = ((unsigned char*)data)[i];
		} else {
			ascii[i % 16] = '.';
		}
		if ((i+1) % 8 == 0 || i+1 == size) {
			printf(" ");
			if ((i+1) % 16 == 0) {
				printf("|  %s \n", ascii);
			} else if (i+1 == size) {
				ascii[(i+1) % 16] = '\0';
				if ((i+1) % 16 <= 8) {
					printf(" ");
				}
				for (j = (i+1) % 16; j < 16; ++j) {
					printf("   ");
				}
				printf("|  %s \n", ascii);
			}
		}
	}
}
	
int main(int argc, char **argv)
{
	memread_t *rbuf,*rbuf_base;
	int i;
	
	void *map_base, *virt_addr;
	uint64_t read_result=0;
	uint64_t writeval = writeval; /* for compiler */
	unsigned page_size, mapped_size, offset_in_page,read_len;
	int fd;
	unsigned width = 8 * sizeof(int);
	uint64_t start, size, addr;
	
		
	if(argc != 3)
	{
	    printf("[ERROR] %s <start_address> <size>\n", argv[0]);
	    return -1;
	}
	    
	start = strtoull(argv[1], NULL, 16);
	size = strtoull(argv[2], NULL, 16);
	printf("Running %s [0x%" PRIx64  "] size:0x%" PRIx64  "\n", argv[0], start, size);
	
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
		
	rbuf = (memread_t *)malloc(READ_ELEMENT_SIZE*nBUFF_ELEMENTS);
	if(rbuf == NULL){
		printf("malloc failed");
		return EXIT_FAILURE;
	}
	rbuf_base = rbuf;
	
	printf("Reading [0x%" PRIx64  "]-[0x%" PRIx64  "] = %d blocks, 0x%08x bytes\n",start, start + size, read_len, mapped_size);
	addr=start;
	while(read_len--){
		for(i=0;i<nBUFF_ELEMENTS;i++){
			*rbuf = *(volatile uint32_t*)virt_addr;
			rbuf++;
			virt_addr+=4;
		}
		rbuf = rbuf_base;
			
		DumpHex(rbuf,READ_ELEMENT_SIZE*nBUFF_ELEMENTS,(uint32_t)addr);
		addr+=READ_ELEMENT_SIZE*nBUFF_ELEMENTS;
	}
	
	free(rbuf);
	rbuf=0;
	printf("done\n");

	close(fd);

	return EXIT_SUCCESS;
}


