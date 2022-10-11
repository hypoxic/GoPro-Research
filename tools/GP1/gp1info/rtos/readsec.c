/* Rtos side of our rtos tunnel */
#undef __ASSEMBLY__
#include "readsec.h"

//int main(int argc, char* argv[]){
int false_cmd(int ArgCount, uint8_t **pArgVector, void (*PrintFunc)(void *)){
	uint8_t			seckey[0x800];
	uint8_t			fake[0x90];
	const char		filename[] = "c:\\fullsec.bin";
	AMBA_FS_FILE*	p_file;
	int				i;
	uint8_t			j;
	uint8_t			*p;

	printk("Testing readsec");	

	memset(seckey,0,sizeof(seckey));
	memset(fake,0xAA,sizeof(fake));

	p = seckey;
	mcu_atmsamd21_i2c_lock();
	mcu_bld_boot();

	mcu_transfer_fifo_reset();
	mcu_transfer_ready_wait();

	mcu_transfer_fifo_write(fake,0x90);
	mcu_transfer_ready_wait();

	mcu_flash_write(1);
	
	mcu_atmsamd21_reg_write(0x21, 0xF0);
	mcu_atmsamd21_reg_read(0x23, p, 0x800);

/*
	mcu_atmsamd21_reg_write(0x21, 0xF0);
	mcu_atmsamd21_reg_read(0x23, p, 0x800);


	mcu_atmsamd21_reg_write(0x21, 0xF1);
	mcu_atmsamd21_reg_read(0x23, seckey+0x80, 0x80);


	mcu_atmsamd21_reg_read(0xB3, p, 1);
	mcu_atmsamd21_reg_read(0xB4, p+1, 0x800);
	*/
	mcu_atmsamd21_i2c_unlock();

	p_file = AmbaFS_fopen(filename, "wb");
	AmbaFS_fwrite(seckey,1,sizeof(seckey),p_file);
	AmbaFS_fclose(p_file);

	printk("End of test");
	
	return 0;
}


