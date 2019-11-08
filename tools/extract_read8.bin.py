import os
import struct

MAGIC_HDR = "MILBEAUT"
BASE_ADDR = 0xA0000000
directory = "out"

# so we search for bootup_lcd string and the bootup LCD data as that does not change. We should be able to locate similar data in the hero8
IDENT="COMMON"
#LCD_DATA=bytearray(b'\x81\x82\x86\xff')
LCD_DATA=bytearray(b"0232.")

DATA_BIN_INIT_OFFSET = 0
MAX_STR_LEN=20

def getLocInt(s, idx):
    v=int.from_bytes(s[idx:idx+4], byteorder='little')
    return v

def CreateNextFile(s, idx):
    data_idx=getLocInt(s,idx)
    size=getLocInt(s,idx+4)
    name_idx=getLocInt(s,idx+8)
        
    if (data_idx != 0 and data_idx > BASE_ADDR and size < 0x6000000):
        data_idx -= BASE_ADDR
        name_idx -= BASE_ADDR
        
        data_idx -= DATA_BIN_INIT_OFFSET
        
        r=bytearray(s[name_idx:name_idx+MAX_STR_LEN])
        r=r.split(b'\0',1)[0]
        name=r.decode()
        
        if (not name):
            return False
        print("Creating %s of size %x from data at %x" % (name, size, data_idx))
        
        name= directory + "\\" + name
        
        data=s[data_idx:data_idx+size]
        with open(name,"wb") as fw:
            fw.write(data)
        fw.close()
        return True
    else:
        return False
            
print("For extracting binaries from read.bin")

with open("read.bin","rb") as f:
    f.seek(0, os.SEEK_END)
    size =  f.tell()
    f.seek(0)
    print("size %x" % size)
    s=bytes(f.read())
f.close()

# Now find the LCD data
lcddata_idx = s.find(LCD_DATA)

if (lcddata_idx == -1):
    print("LCD_DATA not found")
    exit()

print("found LCD_DATA at %x" % (lcddata_idx))

ROM_DB_srch=lcddata_idx+BASE_ADDR
rsrch=ROM_DB_srch.to_bytes(4, byteorder='little')
ROM_DB_IDX = s.find(rsrch)

if (ROM_DB_IDX == -1):
    print("Table of contents not found")
    exit()

print("found DB at 0x%x offset" % (ROM_DB_IDX))

d_idx=getLocInt(s,ROM_DB_IDX)-BASE_ADDR
if (d_idx > size):
    DATA_BIN_INIT_OFFSET=d_idx-lcddata_idx
    print("d_idx is %x size is %x, offsetting by %x" % (d_idx, size, DATA_BIN_INIT_OFFSET))
else:
    print("no offset")    

while 1:
    if(CreateNextFile(s,ROM_DB_IDX)):
        ROM_DB_IDX+= 0xC
    else:
        break

print("Done")
