import os
import io
from pyfdt.pyfdt import FdtBlobParse
import glob
import struct


MAGIC_HDR = "MILBEAUT"
BASE_ADDR = 0xA0000000
directory = "dts"

# so we search for bootup_lcd string and the bootup LCD data as that does not change. We should be able to locate similar data in the hero8
IDENT="COMMON"
DTS_MAGIC=bytearray(b'\xd0\x0d\xfe\xed')
dts_magic_int= 0xd00dfeed

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

def getLocIntBig(s, idx):
    v=int.from_bytes(s[idx:idx+4], byteorder='big')
    return v

def CreateNextFile(s, idx):
    magic=getLocIntBig(s,idx)
    
    if(magic != dts_magic_int):
        return 0
    else:    
        dts_size=getLocIntBig(s,idx+4)
        name_idx=idx+0x5C
        r=bytearray(s[name_idx:name_idx+MAX_STR_LEN])
        r=r.split(b'\0',1)[0]
        name=r.decode()
        name=name+".dts"
                
        if (not name):
            print("Name Not Found")
            return 0
            exit()

        print("Creating \"%s\" of size %x from data at %x" % (name, dts_size, idx))
                
        name= directory + "\\" + name

        data=s[idx:idx+dts_size]
        f = io.BytesIO(data)
        dtb = FdtBlobParse(f)
        fos = dtb.to_fdt().to_dts()
        
        with open(name, "w") as outfile:
            outfile.write(fos)                    
            
        return dts_size
            
print("Extracting DTS DATA.bin")

if not os.path.exists(directory):
    os.makedirs(directory)

start = BASE_ADDR

li = open("DATA.bin","rb")

for vol in parser(li):
    buf = vol.buf
    size = vol.size
    end = start + size
    
    s=bytes(buf)
    
    # Now find the Magic key for DTS
    dts_idx = s.find(DTS_MAGIC)

    if (dts_idx == -1):
        continue

    print("found DTS_MAGIC at %x in volume %d" % (dts_idx, vol.vid))
    while 1:
        l=CreateNextFile(s,dts_idx)        
        if l == 0:
            break
        dts_idx+=l    

li.close()




print("Done")