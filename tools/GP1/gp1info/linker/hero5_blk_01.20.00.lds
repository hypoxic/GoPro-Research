PATCH_LINKER_VER = 0x0000001;

/* false console function overwritten location */
overwrite_loc = 0xA63346CC;

/* Test hor & ver warp table  */
patch_dest = 0xA76C4810;
patch_dest_size = 0x2000;

/* patch_ram_dest = 0xA0100000; */
/* Sharing with AmbaLink_Mutex cache line */
patch_ram_dest = 0xA0515100;
/* patch_ram_dest = 0xDFF00100;  noncached */
patch_ram_size = LAST_RAM - patch_ram_dest;

mutex 			= ABSOLUTE(patch_ram_dest);
out_buffer  	= ABSOLUTE(mutex + 4);
idx_out_rtos	= ABSOLUTE(out_buffer + 0x1000);
idx_out_linux	= ABSOLUTE(idx_out_rtos + 4);
out_ready 		= ABSOLUTE(idx_out_linux + 4);
in_buffer		= ABSOLUTE(out_ready + 4);
idx_in_rtos		= ABSOLUTE(in_buffer + 0x1000);
idx_in_linux	= ABSOLUTE(idx_in_rtos + 4);
in_ready		= ABSOLUTE(idx_in_linux + 4);
LAST_RAM		= in_ready;

printk = ABSOLUTE(0xA411EE20); /* See above */
/*memset = ABSOLUTE(0xA4E2DC9C); */ /* See above */
memset = ABSOLUTE(0xA4E2DC9D);  /* Thumb!!@#@! */

/* These values are for pass through testing */
hijacked_putc = ABSOLUTE(0xA482EFD4);
hijacked_getc = ABSOLUTE(0xA482F17C);

/* here are the locations we hijack */
ambash_puts = ABSOLUTE(0xA70C2240); 
ambash_gets = ABSOLUTE(0xA70C2244);

sleep = ABSOLUTE(0xA4B6D198); /* sleep */
ff_open = ABSOLUTE(0xA4B75824);
ff_close = ABSOLUTE(0xA4B75870);
ff_fread = ABSOLUTE(0xA4B75830);
fflush = ABSOLUTE(0xA4E2C968);

luexec = ABSOLUTE(0xA4E2DC9C);

mcu_atmsamd21_reg_write = ABSOLUTE(0xA477B2D8);
mcu_atmsamd21_reg_read	= ABSOLUTE(0xA477B320);
AmbaFS_fopen = ABSOLUTE(0xA4B75824);
AmbaFS_fwrite = ABSOLUTE(0xA4B75834);
AmbaFS_fclose = ABSOLUTE(0xA4B7582C);

mcu_atmsamd21_i2c_unlock  = ABSOLUTE(0xA477B05C);
mcu_atmsamd21_i2c_lock = ABSOLUTE(0xA477AFE8);

mcu_transfer_fifo_reset = ABSOLUTE(0xA47787B4);
mcu_transfer_fifo_write = ABSOLUTE(0xA4778800);
mcu_flash_erase = ABSOLUTE(0xA477870C);
mcu_transfer_ready_wait = ABSOLUTE(0xA4778DC8);
mcu_flash_write = ABSOLUTE(0xA4778758) ;
mcu_bld_boot = ABSOLUTE(0xA47784C4 );

 

/* For Loader */
linker_script_type_version = ABSOLUTE(PATCH_LINKER_VER);

