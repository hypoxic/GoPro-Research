/* SPDX-License-Identifier: GPL-2.0 */
/* 
  Trunk/Hypoxic : getcpuid.c
  Compile: arm-linux-gnueabihf-gcc -Wall getcpuid.c -o getcpuid
  /mnt/c/Users/hypoxic/Documents/GitHub/GoPro-Research/tools/GP2/getprocessorinfo$ arm-linux-gnueabihf-gcc -Wall getcpuid.c -o getcpuid
  */

#define CONFIG_CPU_CP15 

#include <stdio.h>
#include <stdint.h>

#define u32 uint32_t

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


/* From linux master/arch/arm/kernel/setup.c */
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

int main(int argc, char *argv[]){
    uint32_t arch = __get_cpu_architecture();
    
    printf("Architecture= %d, read 0x%X\n", arch, (uint32_t)read_cpuid_id());
    unsigned int mmfr0 = read_cpuid_ext(CPUID_EXT_MMFR0);
    printf("CPUID Ext= 0x%x\n", mmfr0);
}