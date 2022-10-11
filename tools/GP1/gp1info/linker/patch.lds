OUTPUT_FORMAT("elf32-littlearm", "elf32-littlearm", "elf32-littlearm")
OUTPUT_ARCH(arm)

desc = patch_dest;
entry = desc + 0xF0;

SECTIONS
{
    . desc : { tag.o(.text) }
    
	. = entry; 
	. = ALIGN(4);
	.text      :
	{   	
	  crt.o(.text);
	  *(.text)
	}

	. = ALIGN(4);
	.rodata : { *(.rodata) }

	. = ALIGN(4);
	.data : { *(.data) }

	. = ALIGN(4);
	.got : { *(.got) }

    . = ALIGN(4);
    .persist :
       {
         _persist_begin = .;
         *(.persist .persist.*)
         _persist_end = .;
       } 

	. = ALIGN(4);
	__bss_start = .;
	.bss : { *(.bss) }
	__bss_end__ = .;

	_end = .;

}

