/* SPDX-License-Identifier: GPL-2.0 */
/* 
  Trunk/Hypoxic : getcpuid.c
  Compile: arm-linux-gnueabihf-gcc -Wall getcpuid.c -o getcpuid
  /mnt/c/Users/hypoxic/Documents/GitHub/GoPro-Research/tools/GP2/getprocessorinfo$ arm-linux-gnueabihf-gcc -Wall getcpuid.c -o getcpuid
  
  Then call from linux:
    /tmp/fuse_d/patchldr /tmp/fuse_d/gp1info.bin
  Then involk from rtos
    pwd
    
    Hypoxic GP1 Sniff
    Architecture= 9, read 0x410fc075
  */

#define CONFIG_CPU_CP15 

#include <stdio.h>
#include <stdint.h>

#define u32 uint32_t

#undef __ASSEMBLY__
#include "gp1_info.h"
#include "stringify.h"   
#include "cputype.h"

/* system_info.h */
#define CPU_ARCH_UNKNOWN	0
#define CPU_ARCH_ARMv3		1
#define CPU_ARCH_ARMv4		2
#define CPU_ARCH_ARMv4T		3
#define CPU_ARCH_ARMv5		4
#define CPU_ARCH_ARMv5T		5
#define CPU_ARCH_ARMv5TE	6
#define CPU_ARCH_ARMv5TEJ	7
#define CPU_ARCH_ARMv6		8
#define CPU_ARCH_ARMv7		9
#define CPU_ARCH_ARMv7M		10

unsigned int processor_id;

#define UNUSED(...) (void)(__VA_ARGS__)
#define read32(addr)         (*((uint32_t *)addr))
#define write32(addr, data)  (*((uint32_t *)addr)=data)

// from https://gist.github.com/ccbrown/9722406
void DumpHex(const void* data, size_t size) {
	char ascii[17];
	size_t i, j;
	ascii[16] = '\0';
	for (i = 0; i < size; ++i) {
		printk("%02X ", ((unsigned char*)data)[i]);
		if (((unsigned char*)data)[i] >= ' ' && ((unsigned char*)data)[i] <= '~') {
			ascii[i % 16] = ((unsigned char*)data)[i];
		} else {
			ascii[i % 16] = '.';
		}
		if ((i+1) % 8 == 0 || i+1 == size) {
			printk(" ");
			if ((i+1) % 16 == 0) {
				printk("|  %s \n", ascii);
			} else if (i+1 == size) {
				ascii[(i+1) % 16] = '\0';
				if ((i+1) % 16 <= 8) {
					printk(" ");
				}
				for (j = (i+1) % 16; j < 16; ++j) {
					printk("   ");
				}
				printk("|  %s \n", ascii);
			}
		}
	}
}

/* From master/arch/arm/kernel/setup.c */
static int __get_cpu_architecture(void)
{
	int cpu_arch;

	if ((read_cpuid_id() & 0x0008f000) == 0) {
		cpu_arch = CPU_ARCH_UNKNOWN;
	} else if ((read_cpuid_id() & 0x0008f000) == 0x00007000) {
		cpu_arch = (read_cpuid_id() & (1 << 23)) ? CPU_ARCH_ARMv4T : CPU_ARCH_ARMv3;
	} else if ((read_cpuid_id() & 0x00080000) == 0x00000000) {
		cpu_arch = (read_cpuid_id() >> 16) & 7;
		if (cpu_arch)
			cpu_arch += CPU_ARCH_ARMv3;
	} else if ((read_cpuid_id() & 0x000f0000) == 0x000f0000) {
		/* Revised CPUID format. Read the Memory Model Feature
		 * Register 0 and check for VMSAv7 or PMSAv7 */
		unsigned int mmfr0 = read_cpuid_ext(CPUID_EXT_MMFR0);
		if ((mmfr0 & 0x0000000f) >= 0x00000003 ||
		    (mmfr0 & 0x000000f0) >= 0x00000030)
			cpu_arch = CPU_ARCH_ARMv7;
		else if ((mmfr0 & 0x0000000f) == 0x00000002 ||
			 (mmfr0 & 0x000000f0) == 0x00000020)
			cpu_arch = CPU_ARCH_ARMv6;
		else
			cpu_arch = CPU_ARCH_UNKNOWN;
	} else
		cpu_arch = CPU_ARCH_UNKNOWN;

	return cpu_arch;
}

/* doesn't work :( */
void get_csd(void)
{
    int result;
    uint32_t buffer[4]; /* It only grabs 4 bytes */
    //void *card = (void*)0xA5629D80;
    /*
    0xA5629D80 + 0x414 = 0xA562A194 == 0xA562A1B0
    */
    //void *card = (void*)0xA562A1B0;
    void *card = (void*)0xA562A194;
    void *emmc_struct = (void*)0xA562A194; // ->0xA562A1B0-> 0xA5629D80
    UNUSED(emmc_struct);
    
    // Dump structures
    printk("0xA5629D80: ctx:\n");
    DumpHex((uint8_t *)0xA5629D80, 0x200);
    
    printk("0xA5629D80+414:\n");
    DumpHex((uint8_t *)0xA562A194, 0x200);
    
    printk("emmc_struct *(0xA5629D80+414) = 0xA562A1B0\n");
    DumpHex((uint8_t *)0xA562A1B0, 0x200);
        
    /*
        emmc_struct 
        0x449 - initialized?
    
    */
    
    printk("---Starting eMMC Inspection---\n");
    /* Start up the eMMC Clock */
    result = Media_Custom_EM_Start_Clock();
    if(result)
    {
        printk("Media_Custom_EM_Start_Clock failed, res=%d\n", result);           
    }
    else
    {
        /* Let's get the CSD */
        memset(buffer, 0xCC, sizeof(buffer));
        MMC_SEND_CSD(card , &buffer);
        // 0xA5629D80 + 0x105 = 0xA5629E85 + 0x10
        /* 0xA562A194 */
        if(result)
            printk("MMC_SEND_CSD failed! result = %d\n", result);   
        else
        {
            printk("CSD:\n");   
            DumpHex(buffer, sizeof(buffer));        
        }   
        
        result = Media_Custom_EM_Stop_Clock();
        if(result)
            printk("Media_Custom_EM_Stop_Clock failed, res=%d\n", result);           
    }
    printk("---Ending eMMC Inspection---\n");
}

void debug_boot_sector(void)
{
    int Err;
    
    printk("--debug_boot_sector---\n");  
    Err = MWEM_Set_AccessPartition(1);
    if(Err)
        printk("Err Set_AccessPartition(EM_ACCCESS_BOOT_1) ret=%d\n",Err);
    
    Err = read_parameter_em();
    if(Err)
        printk("Err read_parameter_em() ret=%d\n",Err);

    // from read_parameter_em     
    printk("start_sector1 [0xA4570DC0]\n");
    DumpHex((uint8_t *)0xA4570DC0, 2);   
    
    printk("sr_offset [0xA4570A00]\n");
    DumpHex((uint8_t *)0xA4570A00, 4);
    
    printk("dg_offset [0xA4570A04]\n");
    DumpHex((uint8_t *)0xA4570A04, 0x20);
    
    printk("Who Knows [0xA45795CC]\n");
    DumpHex((uint8_t *)0xA45795CC, 0x220);
    
    uint32_t boot_image_addr = read32( 0xA4570DD0 );
    uint32_t boot_image_size = read32( 0xA4570DCC );
    printk("boot_image_addr= %x, boot_image_size = 0x%X\n", boot_image_addr, boot_image_size);
    printk("Now loaded into 0x45700000\n");
       
       /*
         This reads the boot sector and writes it to the card
         This a binary 1:1 of the sector_00.bin
         */
       
       gpFILE fp;
       fp = gp_fs_fopen("C:\\boot_sector_0.bin", "wb");
       int wrote = gp_fs_fwrite((uint8_t *)0x45700000, 1, boot_image_size, fp);
       printk("wrote %d bytes\n", wrote);
       gp_fs_fclose(fp);
       */ 
    
    get_csd();   
    
    Err = MWEM_Set_AccessPartition(0);
    if(Err)
        printk("Err Set_AccessPartition(EM_ACCCESS_BOOT_NONE) ret=%d\n", Err);             
}

/*
  main()
*/
int pwd_cmd(void)
{
    uint32_t read;	
	uint32_t arch = __get_cpu_architecture();
 
    printk("Hypoxic GP1 Information\nSocionext JEDEC ID is Bank 9 0x57");	   
    printk("Architecture= %d, read 0x%x\n", arch, (uint32_t)read_cpuid_id());
    
    read = read_cpuid_ext(CPUID_EXT_PFR0);
    printk("CPUID_EXT_PFR0 = 0x%x\n", read);
    read = read_cpuid_ext(CPUID_EXT_PFR1);
    printk("CPUID_EXT_PFR1 = 0x%x\n", read);
    read = read_cpuid_ext(CPUID_EXT_DFR0);
    printk("CPUID_EXT_DFR0 = 0x%x\n", read);
    read = read_cpuid_ext(CPUID_EXT_AFR0);
    printk("CPUID_EXT_AFR0 = 0x%x\n", read);
    
    read = read_cpuid_ext(CPUID_EXT_MMFR0);
    printk("CPUID_EXT_MMFR0 = 0x%x\n", read);
    read = read_cpuid_ext(CPUID_EXT_MMFR1);
    printk("CPUID_EXT_MMFR1 = 0x%x\n", read);
    read = read_cpuid_ext(CPUID_EXT_MMFR2);
    printk("CPUID_EXT_MMFR2 = 0x%x\n", read);
    read = read_cpuid_ext(CPUID_EXT_MMFR3);
    printk("CPUID_EXT_MMFR3 = 0x%x\n", read);

    read = read_cpuid_ext(CPUID_EXT_ISAR0);
    printk("CPUID_EXT_ISAR0 = 0x%x\n", read);
    read = read_cpuid_ext(CPUID_EXT_ISAR1);
    printk("CPUID_EXT_ISAR1 = 0x%x\n", read);
    read = read_cpuid_ext(CPUID_EXT_ISAR2);
    printk("CPUID_EXT_ISAR2 = 0x%x\n", read);
    read = read_cpuid_ext(CPUID_EXT_ISAR3);
    printk("CPUID_EXT_ISAR3 = 0x%x\n", read);
    read = read_cpuid_ext(CPUID_EXT_ISAR4);
    printk("CPUID_EXT_ISAR4 = 0x%x\n", read);
    read = read_cpuid_ext(CPUID_EXT_ISAR5);
    printk("CPUID_EXT_ISAR5 = 0x%x\n", read);
    
    uint32_t    DebugVer;
    uint64_t    rombase,offset;
    uint32_t dbgid, dbgdevid,dbgdevid1,dbgdevid2, mpidr32;
	{
		uint32_t midr;
		__asm__("mrc p15,0,%0,c0,c0,0":"=r"(midr));
		printk("midr = 0x%x\n", midr);
	}
    
    __asm__("mrc p15,0,%0,c0,c0,5":"=r"(mpidr32));
    printk("mpidr32 = 0x%x\n", mpidr32);
    
    __asm__("mrc p14,0,%0,c0,c0,0":"=r"(dbgid));
    DebugVer = (dbgid >> 16) & 0xf;
    printk("  DBGDIDR           = 0x%08x\n", dbgid);
    printk("  DebugVer          = 0x%08x\n", DebugVer);
    
    __asm__("mrc p14,0,%0,c7,c2,7":"=r"(dbgdevid));
    printk("  DBGDEVID          = 0x%08x\n", dbgdevid);
    
    __asm__("mrc p14,0,%0,c7,c1,7":"=r"(dbgdevid1));
    printk("  DBGDEVID1         = 0x%08x\n", dbgdevid1);
	
	__asm__("mrc p14,0,%0,c7,c0,7":"=r"(dbgdevid2));
    printk("  DBGDEVID2         = 0x%08x\n", dbgdevid2);
	
    uint32_t hi, lo;
    __asm__("mrrc p14,0,%0,%1,c1":"=r"(lo),"=r"(hi));
            rombase = ((uint64_t)hi << 32) | lo;
    printk("rombase(DBGDRAR) = 0x%llX\n", rombase);

    hi = lo = 0;
    __asm__("mrrc p14,0,%0,%1,c2":"=r"(lo),"=r"(hi));
            offset = ((uint64_t)hi << 32) | lo;
    printk("offset(DBGDSAR) = 0x%llX\n", offset);
    
    uint32_t cache_size;
    __asm__("mrc p15,1,%0,c0,c0,0":"=r"(cache_size));
    printk("cache_size(CCSIDR) = 0x%x\n", cache_size);
    
    uint32_t cache_level;
    __asm__("mrc p15,1,%0,c0,c0,1":"=r"(cache_level));
    printk("cache_level(CLIDR) = 0x%x\n", cache_level);

    printk("---Done---\n");
    
    debug_boot_sector();
    
	return 0;
}
