import os
import struct
import sys
import binascii

MAGIC_HDR = "MILBEAUT"
BASE_ADDR = 0xA0000000
directory = "out"

# so we search for bootup_lcd string and the bootup LCD data as that does not change. We should be able to locate similar data in the hero8
IDENT="COMMON"
UPDATEFILENAME="DATA.bin"
UPDATECRCNAME="CAMFWV.bin"

COMMON_FILE_DATA=bytearray(b"0232.")

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
    def __init__(self, vtype, vid, vsize, buf, idx):
        self.vtype = vtype
        self.vid = vid
        self.size = vsize   
        self.buf = buf   
        self.idx = idx

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
        #print("size %x" % self.size)
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
            
            # set the idx after the header
            idx = f.tell()
            
            # Read the data
            b = f.read(volsize)
            
            return(volume(voltype, volid, volsize,b,idx))
        except Exception as e:
            #print("exception " + str(e))
            raise StopIteration

# -----------------------------------------------------------------------
class RomFile: 
    def __init__(self, s , idx): 
        data_idx=getLocInt(s,idx)
        size=getLocInt(s,idx+4)
        name_idx=getLocInt(s,idx+8)
        self.found=False
        
        # check returned values
        if (data_idx != 0 and data_idx > BASE_ADDR and size < 0x6000000):
            data_idx -= BASE_ADDR
            
            name_idx -= BASE_ADDR
            data_idx -= DATA_BIN_INIT_OFFSET
        
            r=bytearray(s[name_idx:name_idx+MAX_STR_LEN])
            r=r.split(b'\0',1)[0]
            
            name=r.decode()
            
            if (not name):
                return None
            
            self.size=size
            self.data_idx=data_idx                
            self.filename=name    
            self.b = s[data_idx:data_idx+size]
            self.found=True
        else:
            return None

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

def update_update_crc(crc):
    CRCOFFSET=0x24
    f = open(UPDATECRCNAME,"rb")
    flen = os.path.getsize(UPDATECRCNAME)
    b = bytearray(f.read(flen))
    f.close()
    
    crcdata=crc.to_bytes(4, byteorder='little')
    b[CRCOFFSET:CRCOFFSET+4]=crcdata
        
    #write    
    fnam= UPDATECRCNAME+".new"   
    fn = open(fnam,"wb")
    fn.write(b)
    fn.close()        
    

def replace_n_write(idx, newbuf, newbuflen):
    f = open(UPDATEFILENAME,"rb")
    flen = os.path.getsize(UPDATEFILENAME)
    b = bytearray(f.read(flen))
    f.close()
    
    #calculate crc32
    b4crc = binascii.crc32(b)
    
    #replace
    b[idx:idx+newbuflen]=newbuf
        
    #calculate crc32
    crc = binascii.crc32(b)
    
    print("crc before %x crc after %x" % (b4crc, crc))
    update_update_crc(crc)
        
    #write    
    fnam= UPDATEFILENAME+".new"   
    fn = open(fnam,"wb")
    fn.write(b)
    fn.close()

            
print("For replacing rom binaries in DATA.bin")

if len(sys.argv) != 3:
    print("USAGE: %s <ROM NAME> <replacement FILENAME>" % str(sys.argv[0]))
    exit()
    
romfilename = str(sys.argv[1])
rplcfilename = str(sys.argv[2])

fpatched = open(rplcfilename,"rb")
if (fpatched == -1):
    print("failed to open file %s" % rplcfilename)
    exit()
    
fpatchsize = os.path.getsize(rplcfilename)
bpatch = fpatched.read(fpatchsize)

print("Loaded patch file name %s of size 0x%x" % (rplcfilename,fpatchsize))
print("Loading Data.bin searching for %s" % (romfilename))

start = BASE_ADDR

li = open(UPDATEFILENAME,"rb")

for vol in parser(li):
    #only load section 4
    if(vol.vid == 4):
        buf = vol.buf
        size = vol.size
        vol_idx = vol.idx
        end = start + size
        print ("Found RTOS volume")

li.close()
#s=bytes(buf)
s=bytearray(buf)

# Now find the file 'COMMON's data
common_file_data_idx = s.find(COMMON_FILE_DATA)

if (common_file_data_idx == -1):
    print("COMMON_FILE_DATA not found")
    exit()

#print("found COMMON_FILE_DATA at %x" % (common_file_data_idx))

# Calculate the virtual address of that data chunk
ROM_DB_srch=common_file_data_idx+BASE_ADDR
rsrch=ROM_DB_srch.to_bytes(4, byteorder='little')

# With this we can find the pointer to the database
ROM_DB_IDX = s.find(rsrch)

if (ROM_DB_IDX == -1):
    print("Table of contents not found")
    exit()

#print("found DB at 0x%x offset" % (ROM_DB_IDX))

#now we find the offset of the database
d_idx=getLocInt(s,ROM_DB_IDX)-BASE_ADDR

if (d_idx > size):
    DATA_BIN_INIT_OFFSET=d_idx-common_file_data_idx
    print("d_idx is %x size is %x, offsetting by %x" % (d_idx, size, DATA_BIN_INIT_OFFSET))

while 1:
    rf = RomFile(s,ROM_DB_IDX)

    if (rf.found):
        if(romfilename == rf.filename):
            print("found %s, replacing..." % rf.filename)
            # Make sure size matches
            if (rf.size != fpatchsize):
                print("size mismatch")
                exit()        
                
            # patch volume 4
            s[rf.data_idx:rf.data_idx+rf.size]= bpatch  
            
            #now patch the file
            replace_n_write(vol_idx, s, size)
            break
            
        ROM_DB_IDX+= 0xC
        
    else:
        print("Passed destination file not found")
        exit() 

print("Done")