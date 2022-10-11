#PREFIX=arm-linux-gnueabihf-
PREFIX=arm-linux-gnueabi-
CC=$(PREFIX)gcc
AS=$(PREFIX)as
LD=$(PREFIX)ld
OBJDUMP=$(PREFIX)objdump
NM=$(PREFIX)nm
STRIP=$(PREFIX)strip
FWDEST=output

SRC_DIR = src
OUTPUTDIR=output

TARGET_FW = patchldr
TARGET = ${TARGET_FW}
HERO_TARGET_DIR=$(HERO_TARGET_DRIVE)$(FWDEST)\\
TARGET_DEST_STRING=${HERO_TARGET_DIR}${TARGET}

#CFLAGS +=  -march=armv7-a -Wl,--dynamic-linker=/lib/ld-linux.so.3 -marm  ${INCDIRS} 
CFLAGS +=  -march=armv7-a -Wall -marm  ${INCDIRS} 
#LFLAGS += -static
LFLAGS += -no-pie

FILES = patchloader.c
OBJS = patchloader.o 

all: clean ${OUTPUTDIR}/$(TARGET)

${OUTPUTDIR}/$(TARGET): $(OBJS)
	$(info ${\n}Making binary for: ${TARGET}${\n})
	$(CC) $(CFLAGS) -o $@ $(FILES) $(LFLAGS)
	
.PHONY: clean
clean:
	$(info ${\n}Removing old files)
	@-rm -f $(OBJS) $(LOADOBJS) $(TARGET).elf ${OUTPUTDIR}/$(TARGET)
		
