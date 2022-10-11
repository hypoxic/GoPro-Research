#ifndef READSEC_H
#define READSEC_H

	#define BUFFER_SIZE		0x400   

	#ifndef __ASSEMBLY__
		
		#include <stdio.h>
		#include <stdint.h>
		#include <stdbool.h>
		#include <stdlib.h>

		#include <string.h>

		#include <sys/msg.h>
		#include <sys/types.h>
		#include <sys/stat.h>
		#include <fcntl.h>

		#include "types.h"

		#define DEBUG

		#ifdef DEBUG
			#define DBG_PRINT printk
		#else
			#define DBG_PRINT(...)
		#endif

		extern int printk(char * c, ...);
		extern void * ff_open(const char * filename, const char * mode);
		extern void * ff_fread(void * ptr, size_t size, size_t count, FILE * stream);
		extern void * ff_close(void *fp);

		extern int hijacked_putc(void *x, char *c, int t);
		extern int hijacked_getc(void *x, char *c, int t);

		extern void * memset ( void * ptr, int value, size_t num );
		//extern void * memcpy(void *dest, const void *src, size_t n);

		extern int luexec(const char * str, unsigned int nothing, unsigned int *ret);

		extern void sleep(int ms); 

		extern int mcu_atmsamd21_reg_read(uint8_t addr, uint8_t *val, int size);
		extern int mcu_atmsamd21_reg_write(uint8_t addr, uint8_t val);
		extern int mcu_atmsamg55_shmem_read(uint8_t *val);
	
		extern int mcu_bld_boot(void);
		extern int mcu_transfer_fifo_reset(void);
		extern int mcu_transfer_ready_wait(void);
		extern int mcu_transfer_fifo_write(uint8_t *data_to_write, uint8_t size);
		extern int mcu_flash_write(int first);

		extern void mcu_atmsamd21_i2c_lock(void);
		extern void mcu_atmsamd21_i2c_unlock(void);

		AMBA_FS_FILE * AmbaFS_fopen(const char *pFileName, const char *pMode);
		uint32_t  AmbaFS_fwrite(const void *pBuf, size_t Size, size_t Count, AMBA_FS_FILE *pFile);
		int  AmbaFS_fclose(AMBA_FS_FILE *pFile);

	#else

	#endif
#endif
