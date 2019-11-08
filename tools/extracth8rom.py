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
    
while 1:
    if(CreateNextFile(s,ROM_DB_IDX)):
        ROM_DB_IDX+= 0xC
    else:
        break

print("Done")