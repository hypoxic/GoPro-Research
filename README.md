# GoPro Research

This Repo has logs, utilities, and legally extracted assests for various GoPro Cameras. Older camera's assets are in their own unique repos within Hypoxic's Github.

## Camera Teardowns 
[GoPro HERO10 Teardown](https://gethypoxic.com/blogs/technical/gopro-hero10-teardown)   
[GoPro HERO9 Teardown](https://gethypoxic.com/blogs/technical/gopro-hero9-teardown)   
[GoPro HERO MAX Physical Teardown](https://gethypoxic.com/blogs/technical/gopro-max-teardown)  
[GoPro HERO8 Teardown](https://gethypoxic.com/blogs/technical/gopro-hero8-teardown)    
[GoPro HERO7 Silver & White Research](https://gethypoxic.com/blogs/technical/gopro-hero7-silver-gopro-hero7-white-research)  
[GoPro HERO7 Teardown](https://gethypoxic.com/blogs/technical/gopro-hero7-teardown) | [HERO7 Repo](https://github.com/hypoxic/gopro-HERO7)  
[GoPro HERO6 Teardown](https://gethypoxic.com/blogs/technical/gopro-hero6-teardown-preliminary)  
[GoPro HERO (2018 Research)](https://gethypoxic.com/blogs/technical/latest-gopro-hero-is-actually-a-gopro-hero5)  
[GoPro HERO5 Physical Teardown](https://gethypoxic.com/blogs/technical/gopro-hero5-tear-down-and-software-study) | [HERO5 Repo](https://github.com/hypoxic/hero5)

## Interfaces & Accessories
[Micronesia (Security Enclave) Research](https://gethypoxic.com/blogs/technical/a-practical-guide-for-cracking-aes-128-encrypted-firmware-updates)  
[GoPro Media Mod Teardown](https://gethypoxic.com/blogs/technical/gopro-media-mod-teardown)   
[Anti Cloning Technology on the GoPro HEROBUS(tm) 2.0](https://gethypoxic.com/blogs/technical/anti-cloning-technology-on-the-gopro-herobus-2-0?_pos=2&_sid=d65b56eb9&_ss=r)  
[GoPro HEROBus(tm) Research](https://gethypoxic.com/blogs/technical/gopro-herobus-for-gopro-hero5)  
[GoPro HERO\[5-9\] Interfaces](https://gethypoxic.com/blogs/technical/gopro-hero5-interfaces)  


## Tools 
Various tools to extract data from the firmware images. 

### GP2
GoPro HERO 10 and up.  
[Tools and scripts for GP2 based cameras](tools/GP2/readme.md)

### GP1
Works with GoPro HERO\[6-9\]
*   **unpackh6** - Breaks up the firmware into it's various binary blobs
*   **binldr.py** - IDA loader for RTOS straight from update file
*   **busybox** - Compiled busybox with all the components such as telnetd 
*   **decompress.py** - used to decompress Embedded Wizard content
*   **extract_read8.bin.py** - Extracts the various binaries from a read image. Useful for research with variables in memory. 
*   **extracth8dtb.py** - Extracts the Device tree from the image. Requires FdtBlobParse & glob
*   **extract8rom.py** - Extracts the rom files from the HERO8/MAX image
*   **extractXromfs.py** - Extracts the rom files from the HEROX image. Note, it's not precise as the memory size is now in code. A warning is given when the memory bounds do not match. 
*   **extracthbmpd** - Extracts the display's bitmaps from front and back
*   **gp1dropper** - rewrites memory in the rtos from linux for code execution in the the rtos
*   **memdump_h8** - linux based utility to read all of the RTOS memory space and dump it to a file. Useful for research with global data initialized. 
*   **readldr.py** - IDA loader for a read in binary. Use memdump_h8 within linux os, then use this loader on resulting binary.
*   **replace_rom_file.py** - Replaces a rom file with an external rom file and recalculates the crcs. Must be the same size. Replace the original files with the resulting files
*   **replace_section_file** - Replaces an extracted section with the one passed. Usefull for patching linux to add your own hook. 

## Logs
Various public dumps, logs, and musings from our research on these various cameras.   

[GoPro HERO 10](https://github.com/hypoxic/GoPro-Research/tree/master/GoPro%20HERO10)  
[GoPro HERO 9](https://github.com/hypoxic/GoPro-Research/tree/master/Gopro%20HERO9)  
[GoPro MAX](https://github.com/hypoxic/GoPro-Research/tree/master/GoPro_Max)   
[GoPro HERO 8](https://github.com/hypoxic/GoPro-Research/tree/master/GoPro%20HERO8)  
[GoPro HERO 8](https://github.com/hypoxic/gopro-HERO7)   
[GoPro HERO 5](https://github.com/hypoxic/hero5)   
[GoPro HERO 4 Session](https://github.com/hypoxic/hero4-session)  

