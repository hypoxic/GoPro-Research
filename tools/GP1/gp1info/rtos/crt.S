.global _start
.func _start
.extern __bss_start
.extern __bss_end__
.extern main

        .text
        #ifndef COMP_LOADER
#if 1
	# NO BSS
_start:
	B       pwd_cmd
#else
_start:
        MOV     r0, #0                     @ get a zero
        LDR     r1,=__bss_start           @ -> bss start
        LDR     r2,=__bss_end__           @ -> bss end
loop:   CMP     r1,r2                     @ check if data to clear
        STRLO   r0,[r1],#4                @ clear 4 bytes
        BLO     loop                        @    loop until done
        B       pwd_cmd
        #endif
#endif
        .end
+
