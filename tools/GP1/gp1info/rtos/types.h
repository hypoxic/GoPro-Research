/* Types for ARM processor */
#ifndef TYPES_H
#define TYPES_H

#include <stdint.h> 
#include <stdbool.h>

//typedef int     size_t;

typedef uint8_t  BYTE;
typedef uint16_t WORD;
typedef uint32_t DWORD;

typedef int      lFILE;

#define LOBYTE(var)      (((unsigned char*)&var)[0])
#define HIBYTE(var)      (((unsigned char*)&var)[1])
#define UPBYTE(var)      (((unsigned char*)&var)[2])
#define HUPBYTE(var)      (((unsigned char*)&var)[3])

#define OFFSETOF(TYPE, ELEMENT) ((size_t)&(((TYPE *)0)->ELEMENT))

typedef int AMBA_FS_FILE;



#endif
