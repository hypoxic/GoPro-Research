/*
  * HYPOXIC - 
  * Trunk / 2022

 */
#include <ctype.h>
#include <dirent.h>
#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <mntent.h>
#include <netdb.h>
#include <setjmp.h>
#include <signal.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdarg.h>
#include <stddef.h>
#include <string.h>
#include <strings.h>
#include <sys/ioctl.h>
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
#include <time.h>
#include <signal.h>
#include "../common/mutex.h"


#define PHYMASK				0xFFFFFFFF
#define BASE                0xA0000000		

#define TIMEOUT			10

typedef struct rtos_mem_t_{
    uint32_t        mem_loc;
    uint32_t        size;    
    uint32_t        init;				// Address of our test command
    uint32_t        patch_caller;       // location where the test function is in memory, ie. pwd
}rtos_mem_t;

// prototypes
int devmem(off_t target, unsigned width, uint64_t *read_result, uint64_t *writeval);
int memmapPtrOpen(int *fd, off_t target, size_t target_size, void **virt_addr, void **map_base, size_t *mapped_size);	
int memmapPtrClose(int fd, void *map_base, size_t mapped_size);

int PrepareBinary(FILE *fbin,rtos_mem_t*);
int loadRtosCode(FILE *fd, uint8_t *cPtr,rtos_mem_t *rmem);

// Main
int main(int argc, char **argv)
{
    FILE        *fd=0;
    rtos_mem_t  rtos_mem;
    
    int 		fd_buff;
    void 		*map_base_buff;
    size_t		mapped_size_buff;
    uint8_t 	*cPtr;
	int 		i;
	    
    if(argc>1){
        printf("Opening up %s\n",argv[1]);
        fd=fopen(argv[1], "rb");
    }
    else
    {
        printf("provide file name!\n");    
    }
    
    printf("HYPOXIC HERO6 Patch Loader\n");
    printf("All rights reserved. Built " __DATE__ " " __TIME__ "\n");
        
    if(PrepareBinary(fd,&rtos_mem) < 0){
    	// close the bin file
	    fclose(fd);
        printf("Prepare Binary Failed\n");
        return EXIT_FAILURE;
    }else
    	printf("successfully loaded %s\n",argv[1]);
    
    // perform the memory map       
    if(memmapPtrOpen(&fd_buff, rtos_mem.mem_loc, rtos_mem.size, (void **)&cPtr, &map_base_buff, &mapped_size_buff) == EXIT_SUCCESS){
		
		printf("Successfully mapped rtos memory\n");
		
		// load the code into memory
		if((i=loadRtosCode(fd, cPtr, &rtos_mem))<0){
			return i;
		}
	
		// Memory is written with the program, close it up
		printf("freeing program mmap\n");
        memmapPtrClose(fd_buff, map_base_buff, mapped_size_buff);   
        cPtr = 0;map_base_buff=0;mapped_size_buff=0;
    
    }else{
        printf("MMAP Failed\n");
        return EXIT_FAILURE;
    }
        
    return EXIT_SUCCESS;
}



/*
 loadRtosCode

*/
int loadRtosCode(FILE *fd, uint8_t *cPtr,rtos_mem_t *rmem){
	int readlen;
	uint64_t  writeval;
	size_t fsize;

	//figure out the files size
	fseek(fd, 0, SEEK_END);
	fsize=ftell(fd);
	fseek(fd, 0, SEEK_SET);
	
	printf("---starting write----\n");

	// read the code into ram into the RTOS space
	readlen = fread(cPtr,fsize,1,fd);

	fclose(fd);

	if(readlen>0){
		printf("Successfully read input file\n");
	
		// now overwrite the test vector type "false" in the rtos.
		writeval = rmem->init;
		printf("test vector overwrite: (0x%08X) 0x%08X\n", rmem->patch_caller, rmem->init);
		
		if(devmem(rmem->patch_caller,32,NULL, &writeval) < 0){
			printf("test vector overwite failed. 0x%08llX", writeval);
			return -10;
		}
				
		// now do an instruction barrier
		//iflush();
		//printf("iflush barrier completed\n");		
	}
	else{
		printf("read failed (%d)\n",readlen);
		return -13;
	}
	
	return 0;
}

#define IDENTITY    "HYPOXIC"
/*

*/
int PrepareBinary(FILE *fbin,rtos_mem_t *rmem){
    char        ident[8];
    int			l;
    
    if(fread(ident,sizeof(char),sizeof(ident),fbin) != sizeof(ident)){
        printf("indentifer failed\n");
        return -1;
        }
    
    if(strncmp(ident,IDENTITY,sizeof(ident) != 0)){
        printf("indentifer mismatch\n");
        return -2;
    }
       
    l = fread(rmem,sizeof(rtos_mem_t),1,fbin);    
    if(l != 1){
        printf("rtos_mem descriptor failed (%d)\n",l);
        return -1;
    }
    
    printf("mem_loc 0x%08x\nsize 0x%08x\ninit 0x%08x\nOverwrite location 0x%08x\n",rmem->mem_loc,rmem->size,rmem->init, rmem->patch_caller); 
    
    //rewind
    fseek(fbin,0,SEEK_SET);
    
    return 0;
}


/*


*/
int memmapPtrOpen(int *fd, off_t target, size_t target_size, void **virt_addr, void **map_base, size_t *mapped_size){
    int filebits;
	unsigned page_size, offset_in_page;
	
	filebits = (O_RDWR | O_SYNC);
	
	target &= PHYMASK;
//	target-=BASE;
	
	*fd = open("/dev/mem", filebits);
	*mapped_size = page_size = getpagesize();
	offset_in_page = (unsigned)(target) & (page_size - 1);
	
	if (offset_in_page + target_size > page_size) {
		/* This access spans pages. */        
		*mapped_size = page_size*((target_size+page_size-1)/page_size);
		printf("mapped_size spans page_size=0x%08x target_size=%08x mapped_size=%08x\n", page_size, target_size, *mapped_size);
	}
	
	printf("memmapPtrOpen 0x%08X size %08X\n", target, *mapped_size);
	
	filebits = (PROT_READ|PROT_WRITE|PROT_EXEC|MAP_SHARED);
	
	*map_base = mmap(NULL,
			*mapped_size,
			filebits,
			MAP_SHARED,
			*fd,
			target & ~(off_t)(page_size - 1));
			
	if (*map_base == MAP_FAILED){
		printf("Failed: OpenPrintfPointers");
		return EXIT_FAILURE;
	}

	*virt_addr = (char*)*map_base + offset_in_page;

	printf("Memory mapped at address 0x%p. 0x%p\n", *map_base,*virt_addr);
	fflush(stdout);
	
	return EXIT_SUCCESS;
}
	

int memmapPtrClose(int fd, void *map_base, size_t mapped_size){
	if (munmap(map_base, mapped_size) == -1){
		printf("munmap");
		return EXIT_FAILURE;
	}
	close(fd);

	return EXIT_SUCCESS;
}



// width is in number of bits, if read_result = NULL then its a write
int devmem(off_t target, unsigned width, uint64_t *read_result, uint64_t *writeval)
{
	void *map_base, *virt_addr;
    int filebits;
	unsigned page_size, mapped_size, offset_in_page;
	int fd;
	
	target &= PHYMASK;
//	target-=BASE;
	
	filebits = ((read_result == NULL) ? (O_RDWR | O_SYNC) : (O_RDONLY | O_SYNC));
	
	fd = open("/dev/mem", filebits);
	mapped_size = page_size = getpagesize();
	offset_in_page = (unsigned)target & (page_size - 1);
	if (offset_in_page + 4 > page_size) {
		/* This access spans pages.
		 * Must map two pages to make it possible: */
		mapped_size *= 2;
	}
	
	filebits = ((read_result == NULL) ? (PROT_READ | PROT_WRITE) : PROT_READ);
	
	map_base = mmap(NULL,
			mapped_size,
			filebits,
			MAP_SHARED,
			fd,
			target & ~(off_t)(page_size - 1));
	if (map_base == MAP_FAILED){
		printf("mmap");
		return EXIT_FAILURE;
	}

	//printf("Memory mapped at address %p.\n", map_base);

	virt_addr = (char*)map_base + offset_in_page;

	if (read_result != NULL) {
		switch (width) {
		case 8:
			*read_result = *(volatile uint8_t*)virt_addr;
			break;
		case 16:
			*read_result = *(volatile uint16_t*)virt_addr;
			break;
		case 32:
			*read_result = *(volatile uint32_t*)virt_addr;
			break;
		case 64:
			*read_result = *(volatile uint64_t*)virt_addr;
			break;
		default:
			printf("bad width");
			
		}
//		printf("Value at address 0x%"OFF_FMT"X (%p): 0x%llX\n",
//			target, virt_addr,
//			(unsigned long long)read_result);
		/* Zero-padded output shows the width of access just done */
		//printf("0x%0*llX\n", (width >> 2), (unsigned long long)*read_result);
	} else {
		switch (width) {
		case 8:
			*(volatile uint8_t*)virt_addr = *writeval;
//			read_result = *(volatile uint8_t*)virt_addr;
			break;
		case 16:
			*(volatile uint16_t*)virt_addr = *writeval;
//			read_result = *(volatile uint16_t*)virt_addr;
			break;
		case 32:
			*(volatile uint32_t*)virt_addr = *writeval;
//			read_result = *(volatile uint32_t*)virt_addr;
			break;
		case 64:
			*(volatile uint64_t*)virt_addr = *writeval;
//			read_result = *(volatile uint64_t*)virt_addr;
			break;
		default:
			printf("bad width");
		}
//		printf("Written 0x%llX; readback 0x%llX\n",
//				(unsigned long long)writeval,
//				(unsigned long long)read_result);
	}

	if (munmap(map_base, mapped_size) == -1)
		printf("munmap");
	close(fd);

	return EXIT_SUCCESS;
}
