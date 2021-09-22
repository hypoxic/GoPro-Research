# rev 2
import os
import struct


MAGIC_HDR = "MILBEAUT"
BASE_ADDR = 0x40080000
directory = "sections"

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
            print("Vol: type %x id %x size 0x%x" % (voltype, volid, volsize))
            b = f.read(volsize)
            
            return(volume(voltype, volid, volsize, b))
        except Exception as e:
            #print("exception " + str(e))
            raise StopIteration

      
print("For extracting binaries from DATA.bin on GP2")

if not os.path.exists(directory):
    os.makedirs(directory)

start = BASE_ADDR

li = open("DATA.bin","rb")

for vol in parser(li):
    buf = vol.buf
    size = vol.size
    end = start + size
    
    fn = str("section_id%02d_type%02d.bin" % (vol.vid, vol.vtype))
    name = os.path.join(directory, fn)
    print(fn)
        
    # lets remove the gopro header        
    s=bytes(buf)[0x200:]
    with open(name,"wb") as fo:
        fo.write(s)
    
li.close()
    
print("Done")