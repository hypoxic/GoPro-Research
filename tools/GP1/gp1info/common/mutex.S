.equ locked,1
.equ unlocked,0

@ lock_mutex
@ Declare for use from C as extern void lock_mutex(void * mutex);
    .global lock_mutex
lock_mutex:
    LDR     r1, =locked
1:  LDREX   r2, [r0]
    CMP     r2, r1        @ Test if mutex is locked or unlocked
    BEQ     2f            @ If locked - wait for it to be released, from 2
    STREXNE r2, r1, [r0]  @ Not locked, attempt to lock it
    CMPNE   r2, #1        @ Check if Store-Exclusive failed
    BEQ     1b            @ Failed - retry from 1
    # Lock acquired
    DMB                   @ Required before accessing protected resource
    BX      lr

2:  @ Take appropriate action while waiting for mutex to become unlocked
    @ WAIT_FOR_UPDATE
    B       1b            @ Retry from 1


@ unlock_mutex
@ Declare for use from C as extern void unlock_mutex(void * mutex);
    .global unlock_mutex
unlock_mutex:
    LDR     r1, =unlocked
    DMB                   @ Required before releasing protected resource
    STR     r1, [r0]      @ Unlock mutex
    @ SIGNAL_UPDATE   
    BX      lr
    
	.global syncronize
synchronize:	
	DMB  
	DSB
	BX      lr
	
	
	.global iflush
iflush:
	DSB
	ISB
	BX		lr
