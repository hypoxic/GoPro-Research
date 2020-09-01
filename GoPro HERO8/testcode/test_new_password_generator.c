/*

Based on HERO8 gpPlatform

*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h> 

#define PWLEN 16
unsigned char PW_CHAR_LIST[] = "0123456789@_-ABCDFGHJKLMNPQRSTVWXYZabcdfghjklmnpqrstvwxyz";

int main(void){  
    int i;
    unsigned char rstream[PWLEN+1];  //random stream  // don't need the last random, but they get it
    unsigned char pw[PWLEN+1];       // password out // +1 for null terminating
    size_t pw_char_list_len = sizeof(PW_CHAR_LIST)-1;  // 57
  
    printf("Creates a random password like the GoPro HERO8\n");
  
    memset(pw,0,sizeof(pw));

    // Create random buffer of 17 characters, actually only needs 16, but they get 17, so I do too  
    #ifdef __linux__
        // their implementation is something like this, I tested mine in windows
        FILE rfile = open64("/dev/urandom", O_RDONLY);
        read(rfile, &rstream, 0x11u);
    #else
        srand(time(0)); 
        for(i=0;i<sizeof(rstream);i++)
            rstream[i]  = rand();
    #endif

    // Now convert it via mod 57=pw_char_list_len
    for(i=0;i<PWLEN;i++)
        pw[i] = PW_CHAR_LIST[rstream[i] % pw_char_list_len];
     
    printf("Password: %s",pw);
}