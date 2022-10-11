PREFIX=arm-linux-gnueabihf-
#PREFIX=arm-linux-gnueabi-
CC=$(PREFIX)gcc
AS=$(PREFIX)as
LD=$(PREFIX)ld
OBJDUMP=$(PREFIX)objdump
NM=$(PREFIX)nm
STRIP=$(PREFIX)strip
FWDEST=output

SRC_DIR = src
HERO_TARGET_DRIVE=\\
OUTPUTDIR=output

TARGET_FW = gp1info
TARGET = ${TARGET_FW}
HERO_TARGET_DIR=$(HERO_TARGET_DRIVE)$(FWDEST)\\
TARGET_DEST_STRING=${HERO_TARGET_DIR}${TARGET}.bin

OBJS = tag.o crt.o gp1_info.o

CFLAGS = -Wall -g2 -Wa,-gstabs -D__ASSEMBLY__ -g -fno-strict-aliasing  \
	-fno-common -marm -ffixed-r8 \
	-fno-builtin -ffreestanding -pipe -fno-pic ${INCDIRS}
OBJCOPY=$(PREFIX)objcopy
LINKERFLAGS = -T ../linker/hero6_02.61.00.lds

LDFLAGS = ${LINKERFLAGS} -T ../linker/patch.lds 
LDLOADERFLAGS = ${LINKERFLAGS} -T ../linker/loader.lds

CLOADFLAGS = ${INCDIRS} $(CFLAGS) -DCOMP_LOADER
LOADOBJS = loader_c.o
TARGET_LOADER = loader

all: clean ${OUTPUTDIR}/$(TARGET).bin

${OUTPUTDIR}/$(TARGET).bin: $(OBJS)
	$(info ${\n}Making binary for: ${TARGET}${\n})
	$(LD) $(OBJS) $(LDFLAGS) -o $(TARGET).elf
	$(OBJCOPY) -O binary --gap-fill 0 $(TARGET).elf ${OUTPUTDIR}/$(TARGET).bin
	#$(OBJDUMP) -D $(TARGET).elf > b.txt	

.PHONY: clean
clean:
	$(info ${\n}Removing old files)
	@-rm -f $(OBJS) $(LOADOBJS) $(TARGET).elf $(TARGET_LOADER).bin $(TARGET_LOADER).elf
