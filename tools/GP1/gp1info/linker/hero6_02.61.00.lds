PATCH_LINKER_VER = 0x0000001;

/* pwd console function overwritten location */
overwrite_loc = 0xA11767FC;  /* search  for pwd */

/* BOOTUP.WAV  */
//patch_dest =   0xA2EDB280;
patch_dest =   0xA2EDC000;
patch_dest_size = 0x1E7A0;

printk = ABSOLUTE(0xA0359830); 
memset = ABSOLUTE(0xA055FD68);  /* FJ_ClearMem_ */
memcpy = ABSOLUTE(0xA055F740); 

sleep = ABSOLUTE(0xA0D8F42C); /* rtos_task_sleep */

gp_fs_fopen = ABSOLUTE(0xA0BF6F98);
gp_fs_fwrite = ABSOLUTE(0xA0BF7200);
gp_fs_fclose = ABSOLUTE(0xA0BF70B8);
gp_fs_fsync = ABSOLUTE(0xA0BF7588);
gp_fs_fread = ABSOLUTE(0xA0BF7114);

MWEM_Set_AccessPartition = ABSOLUTE(0xA04E5240);
read_parameter_em = ABSOLUTE(0xA0349CC8);
MMC_SEND_CSD        = ABSOLUTE(0xA04EA3EC);
MMC_ALL_SEND_CID    = ABSOLUTE(0xA04E9C60);
Media_Custom_EM_Start_Clock = ABSOLUTE(0xA029ADB8);
Media_Custom_EM_Stop_Clock = ABSOLUTE(0xA029AE18);

/* For Loader */
linker_script_type_version = ABSOLUTE(PATCH_LINKER_VER);

