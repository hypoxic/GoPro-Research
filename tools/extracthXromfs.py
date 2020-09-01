# rev 2
import os
import struct


MAGIC_HDR = "MILBEAUT"
BASE_ADDR = 0xA0000000
directory = "romfs"

# so we search for bootup_lcd string and the bootup LCD data as that does not change. We should be able to locate similar data in the hero8
IDENT="COMMON"
#LCD_DATA=bytearray(b'\x81\x82\x86\xff')
LCD_DATA=bytearray(b"0240.")

DATA_BIN_INIT_OFFSET = 0
MAX_STR_LEN=20

# the Latest now populates this table with op codes, kinda a pain if it changes, look for NVD_
# used uEMU and then extracted it with the below script
"""import os
import struct

with open("test.bin", "rb") as f:
    #b = bytearray(f.read())
    s=""
    while True:
        b = f.read(4)
        if not b:
            break
        v = struct.unpack('i', b)[0]
        s += hex(v)+", "
        
    print (s)        
"""

"""
item_lens = [0x2E, 0x14B7C, 0x14B7C, 0x14AB4, 0x14AB4, 0x14AB4, 0x1613C, 0x14AB4, 
0x1613C, 0x14AB4, 0x14AB4, 0x14AB4, 0x14AB4, 0x14AB4, 0x14AB4, 0x14AB4, 
0x14AB4, 0x14AB4, 0x14AB4, 0x14AB4, 0x14AB4, 0x14AB4, 0x14AB4, 0x1374, 
0x502C, 0xA02C, 0xEC2C, 0x202C, 0x1782C, 0x302C, 0x802C, 0x1402C, 
0x3402C, 0x7C2C, 0x13690, 0x4030, 0x57BB, 0x57BE, 0x571B, 0x55EE86, 
0xC9B0, 0x7DE, 0x33666, 0xF8E1, 0x1ECD]                                                                          
"""
item_lens = [0x2e, 0x14b7c, 0x14b7c, 0x13bac, 0x13f0c, 0x13ae4, 0x14b7c, 0x13bac, 
0x14b7c, 0x13bac, 0x13bac, 0x13bac, 0x13bac, 0x13bac, 0x13bac, 0x13bac, 0x13bac, 
0x13bac, 0x13bac, 0x13bac, 0x13bac, 0x13bac, 0x13bac, 0x1374, 0x502c, 0xa02c, 
0xec2c, 0x202c, 0x1782c, 0x302c, 0x802c, 0x1402c, 0x3402c, 0x7c2c, 0x10510, 
0x4030, 0x57bb, 0x57be, 0x571b, 0xd60, 0x7ea0, 0x7ea0, 0x7ea0, 0x55ee86, 
0xc9b0, 0x7de, 0x38400, 0x38400, 0x33666, 0xfa6f, 0x1f11]

# -----------------------------------------------------------------------
class volume(object):
    """
    @param vtype: volume type as read from the header
    @param vid: volume id 
    @param vsize: volume size minus header
    #param buf: The volume's data 
    """
    def __init__(self, vtype, vid, vsize, buf):
        self.vtype = vtype
        self.vid = vid
        self.size = vsize   
        self.buf = buf   

# -----------------------------------------------------------------------
class parser:
    """
    Parse the Socionext Data.bin file

    @param li: a file-like object which can be used to access the input data
    @return: volume
    """
    def __init__(self,li):
        li.seek(0, os.SEEK_END)
        self.size =  li.tell()
        li.seek(0)
        print("size %x" % self.size)
        self.f = li
        
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            f = self.f
            # Read the header
            (magic,voltype, volid, volsize) = struct.unpack("<8sHHI", f.read(16))
            
            if magic != MAGIC_HDR:
                StopIteration
            
            # Read the data
            b = f.read(volsize)
            
            return(volume(voltype, volid, volsize,b))
        except Exception as e:
            #print("exception " + str(e))
            raise StopIteration

def getLocInt(s, idx):
    v=int.from_bytes(s[idx:idx+4], byteorder='little')
    return v

def CreateNextFile(s, idx, item):
    data_idx=getLocInt(s,idx)
    size=getLocInt(s,idx+4)
    name_idx=getLocInt(s,idx+8)
    data_idx_next=getLocInt(s,idx+0xC)
    estsize=data_idx_next-data_idx
    
    size = item_lens[item]
    
        
    if (data_idx != 0 and data_idx > BASE_ADDR and size < 0x6000000):
        data_idx -= BASE_ADDR
        name_idx -= BASE_ADDR
        
        data_idx -= DATA_BIN_INIT_OFFSET
        
        r=bytearray(s[name_idx:name_idx+MAX_STR_LEN])
        r=r.split(b'\0',1)[0]
        name=r.decode()
        
        if (not name):
            return False
            
        if(name == "MCU_APP_CHP1"):
            size = estsize    
                
        if(name == "BT_SETTINGS"):
            size = estsize           
                
        if(size == estsize):    
            print("Creating %s of size %x from data at %x" % (name, size, data_idx))
        else:
            print("[Non Continuous] Creating %s of size 0x%x != 0x%x from data at %x" % (name, size, estsize, data_idx))                        
        
        name= directory + "\\" + name
        
        data=s[data_idx:data_idx+size]
        with open(name,"wb") as fw:
            fw.write(data)
        fw.close()
        return True
    else:
        return False
            
print("For extracting binaries from DATA.bin")

if not os.path.exists(directory):
    os.makedirs(directory)

start = BASE_ADDR

li = open("DATA.bin","rb")

for vol in parser(li):
    #only load section 4
    if(vol.vid == 4):
        buf = vol.buf
        size = vol.size
        end = start + size
        print ("Found RTOS size %x" % size)

li.close()
s=bytes(buf)

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

i=0    
while i < len(item_lens):
    if(CreateNextFile(s,ROM_DB_IDX,i)):
        ROM_DB_IDX+= 0xC
        i+=1
    else:
        break

print("Done")