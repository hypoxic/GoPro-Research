#ifndef GP1_INFO_H
#define GP1_INFO_H

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

        #define gpFILE void*
		extern int printk(char * c, ...);
		extern gpFILE gp_fs_fopen(const char * filename, const char * mode);
		extern int gp_fs_fread(void * ptr, size_t size, size_t count, gpFILE fp);// returns length
        extern int gp_fs_fwrite(void * ptr, size_t size, size_t count, gpFILE fp); // returns length
		extern int gp_fs_fclose(gpFILE fp);  /* returns 0 if passes */
		
		/* emmc debug */
		extern int MWEM_Set_AccessPartition(int x); 
		extern int read_parameter_em(void);
		extern int MMC_SEND_CSD(void*, void*);
		extern int Media_Custom_EM_Start_Clock(void);
		extern int Media_Custom_EM_Stop_Clock(void);

		extern void sleep(int ms); 

	#else

	#endif
#endif
