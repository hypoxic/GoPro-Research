import os
import struct
import array

LZW_STACKSIZE=4096
lValues = [0] * (LZW_STACKSIZE - 258)
#lValues = [0] * (LZW_STACKSIZE)
rValues = [0] * (LZW_STACKSIZE - 258)
#rValues = [0] * (LZW_STACKSIZE)
stack = [0] * LZW_STACKSIZE

def decompress(b,Width,Pitch):
    tmp = int(0)
    mask = 0x01FF
    i = 0
    depth=9
    l=32
    nextCode = 258
    oldCode = 0xFFFF
    ofs = int(0)
    aDest = []
    
    a = struct.unpack_from('<I', b, i)
    i+=4
    acc = a[0]
    
    curCode = acc & mask
    acc = acc >> 9
    l -= depth
    
    while ( curCode != 257 ):
        tmp = curCode
        #print("code: %04x" %curCode)
        
        if (curCode == 256):
            #print("[clear code]")
            depth = 9
            mask = 0x01FF
            nextCode = 258
            curCode = 0xFFFF
            #print("nextcode: %x new depth %x mask %x" % (nextCode, depth, mask))
        else:
            #print("curCode %x nextCode %x" % (curCode, nextCode))
            if (curCode == nextCode):
                tmp = oldCode
                ofs += 1
                
            while (tmp > 257):
                tmp -= 258
                if(ofs >= LZW_STACKSIZE or tmp >= LZW_STACKSIZE or ofs < 0 or tmp < 0):
                    print("decompression FaTAL ofs:%x tmp:%x" % (ofs,tmp))
                    return []
                    
                stack[ofs] = rValues[tmp]
                ofs += 1
                tmp = lValues[tmp]
                #print("r:%x", rValues[tmp], end =" ")
                #print("l:%x", lValues[tmp], end =" ")
            
            # The last code word is equal the uncompressed byte 
            stack[ofs] = tmp
            ofs += 1

            # Continue with the special case: repeat the first character from the last sequenz 
            if (curCode == nextCode):
                stack[0] = stack[ofs - 1]

            # Append new entry to the table 
            if (oldCode != 0xFFFF):
                #print("old code %04x" % oldCode)
                lValues[nextCode - 258] = oldCode
                rValues[nextCode - 258] = stack[ofs - 1]

                # Calculate the code word depth 
                if (((nextCode ^ (nextCode + 1)) > nextCode) and (depth < 12)):
                    depth+=1
                    mask = (mask << 1) | 1
                nextCode+=1
                #print("nextcode: %x new depth %x mask %x" % (nextCode, depth, mask))

            # from HERO code
            if (Width and Pitch):
                print("Width & pitch untested")
                while (ofs):
                    ofs -= 1
                    aDest.append(stack[ofs])
                    for x in range (0, Width):
                        for y in range (0, (Pitch - Width)):
                            aDest.append(0)
            else:
               # Write the content of the stack in revers order to the aDest memory 
               #print("Stackdump[%x] " % ofs, end =" ")

               while (ofs):
                   ofs -= 1
                   aDest.append(stack[ofs])
                   #print("%02x " % stack[ofs], end =" ")
                   
        if (l <= 16):
            hword = struct.unpack_from('<H', b, i)[0]
            acc |= hword << l;
            i+=2
            l += 16;  
            #print("ACC: %04x" % acc)
        
        oldCode = curCode;
        curCode = acc & mask;
        acc = acc >> depth;
        l -= depth;

    return aDest
