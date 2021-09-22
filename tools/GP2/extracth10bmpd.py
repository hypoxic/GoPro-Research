import os
import struct
import numpy as np
from collections import namedtuple
from decompress import decompress
from PIL import Image

MAGIC_HDR = "MILBEAUT"
H10HDRSIZE = 0x200

BASE_ADDR = 0x40080000
MAX_ADDR  = 0x44000000
MAX_COMPRESEDSIZE = 0x100000
fdir = "front"
bdir = "back"

EW_DRIVER_VARIANT_RGBA8888 = 1
EW_DRIVER_VARIANT_RGBA4444 = 2
EW_DRIVER_VARIANT_RGB565A8 = 3
EW_DRIVER_VARIANT_RGB555A8 = 4
EW_DRIVER_VARIANT_YUVA8888 = 5
EW_DRIVER_VARIANT_LUMA44   = 6
EW_DRIVER_VARIANT_RGB565   = 7
EW_DRIVER_VARIANT_RGB888   = 8
EW_DRIVER_VARIANT_INDEX8   = 11
EW_DRIVER_VARIANT_ALPHA8   = 12

# so we search for bootup_lcd string and the bootup LCD data as that does not change. We should be able to locate similar data in the hero8
BMP_MAGIC=bytes(b'\x64\x70\x6d\x62')  # 0x626D7064
bmp_magic_int= 0xd00dfeed

DATA_BIN_INIT_OFFSET = 0
MAX_STR_LEN=20

def validateAddress(f):
    if (f > BASE_ADDR and f < MAX_ADDR):
        return True
    else:
        return False

"""
typedef struct {
	uint32_t MagicNo;
	int32_t Format;
	int32_t FrameWidth;
	int32_t FrameHeight;
	int32_t FrameDelay;
	int32_t NoOfFrames;
	const XBmpFrameRes *Frames;
	const void *Pixel;
}XBmpRes;
"""
class XBmpRes():
    def __init__(self, s, i):
        MagicNo,Format,FrameWidth,FrameHeight,FrameDelay,NoOfFrames,Frames,Pixel =struct.unpack_from('<IiiiiiQQ', s, i)
        
        if(validateAddress(Frames) and validateAddress(Pixel)):
            self.MagicNo = MagicNo.to_bytes(4, byteorder='little')
            self.Format = Format
            self.FrameWidth = FrameWidth
            self.FrameHeight = FrameHeight
            self.FrameDelay = FrameDelay
            self.NoOfFrames = NoOfFrames
            self.Frames = Frames
            self.Pixel =Pixel
            print("XBmpRes Type:%x Size:%dx%d Delay:%dms NoOfFrames:%d FramePtr:%x PixelPtr:%x" % (Format,FrameWidth,FrameHeight,FrameDelay,NoOfFrames,Frames,Pixel))
        else:
            print("not valid address")
            return None

"""
typedef struct {
	int32_t OpqX;
	int32_t OpqY;
	int32_t OpqWidth;
	int32_t OpqHeight;
	uint32_t Pixel1;
	int32_t Pixel2;
}XBmpFrameRes;
"""
XBMPFRAMERESSIZE=6*4
class XBmpFrameRes():
    def __init__(self, s, i):    
        OpqX,OpqY,OpqWidth,OpqHeight,Pixel1,Pixel2=struct.unpack_from('<iiiiIi', s, i)
        self.OpqX =         OpqX            
        self.OpqY =         OpqY     
        self.OpqWidth =     OpqWidth 
        self.OpqHeight =    OpqHeight
        self.Pixel1 =      	Pixel1   
        self.Pixel2 =       Pixel2   
        #print("XBmpFrameRes Opq: (%d,%d) Opq %d x %d Pixel1 %d Pixel2 %d" % (OpqX, OpqY, OpqWidth, OpqHeight, Pixel1, Pixel2))

    	
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
                
            # Skip the new header 
            f.read(H10HDRSIZE)       
            
            volsize -= H10HDRSIZE # Read the data
            
            # Read the data
            b = f.read(volsize)
            
            return(volume(voltype, volid, volsize,b))
        except Exception as e:
            #print("exception " + str(e))
            raise StopIteration

def addr2offset(a):
    return a-BASE_ADDR

def getLocInt(s, idx):
    v=int.from_bytes(s[idx:idx+4], byteorder='little')
    return v

def getLocIntBig(s, idx):
    v=int.from_bytes(s[idx:idx+4], byteorder='big')
    return v

def RGB565_to_8888(  buf  ):
    nlist = np.asarray(buf, dtype='<B')
    nlist = nlist.view(np.uint16)
    
    s = len(nlist) *4 
       
    arr = np.empty(shape=[s], dtype=np.uint8)
    i = 0
    
    for n in nlist:
        # alpha
        arr[i] = 0xFF
        i+=1
        
        arr[i] = n & 0x1F
        i+=1
        
        arr[i] = (n >> 5) & 0x3F
        i+=1
        
        arr[i] = (n >> 11) & 0x1F
        i+=1
    
    return arr           
                 

#
bmpcount=0

def CreateNextFile(s, idx):
    global bmpcount
    global fdir,bdir
    bmp = XBmpRes(s, idx)
        
    if(bmp and bmp.MagicNo != BMP_MAGIC):
        print("invalid magic %x" % bmp.MagicNo)
        return 0
    else:   
        frame_ofs=addr2offset(bmp.Frames)
        pixel_ofs=addr2offset(bmp.Pixel)
        
        if(bmp.Format == EW_DRIVER_VARIANT_ALPHA8):            
            RGB8888 = decompress(s[pixel_ofs:],0,0)
                
            print("\EW_DRIVER_VARIANT_ALPHA8 frameset (%d x %dpx)" % (bmp.FrameWidth, bmp.FrameHeight))
            #pass                
            for f in range(0,bmp.NoOfFrames):
                frame = XBmpFrameRes(s, frame_ofs+(f*XBMPFRAMERESSIZE))
                
                #print("\t[%04d]Opq: (%d,%d) Opq %d x %d Pixel1 %d Pixel2 %d" % (f, frame.OpqX, frame.OpqY, frame.OpqWidth, frame.OpqHeight, frame.Pixel1, frame.Pixel2))
                fn=str("fimg_%04d_%02dof%02d.png" % ( bmpcount, f,bmp.NoOfFrames))
                sz=bmp.FrameWidth* bmp.FrameHeight
                frame = XBmpFrameRes(s, frame_ofs)
                framebuf=RGB8888[frame.Pixel1:frame.Pixel1+sz]
                aBGR = np.array(framebuf, dtype=np.uint8)    
                img=Image.frombuffer('L', (bmp.FrameWidth, bmp.FrameHeight), aBGR, 'raw', 'L', 0, 1)
                
                if(img):
                   fname = os.path.join(fdir, fn)
                   img.save(fname)
                   print("\t\tCreated: %s (%d x %dpx)" % ( fn, bmp.FrameWidth, bmp.FrameHeight))
                else:
                    print("error creating img")
            bmpcount+=1    
        elif(bmp.Format == EW_DRIVER_VARIANT_RGBA8888):    
            frame = XBmpFrameRes(s, frame_ofs)
           
            print("\EW_DRIVER_VARIANT_RGBA8888 frameset (%d x %dpx)" % (bmp.FrameWidth, bmp.FrameHeight))
           
            if(bmp.FrameWidth):
                
                RGB8888 = decompress(s[pixel_ofs:],0,0)
                
                fn=str("bimg_%04d.png" % ( bmpcount ))
                                
                aBGR = np.array(RGB8888, dtype=np.uint8)
                
                try:
                    img=Image.frombuffer('RGBA', (bmp.FrameWidth, bmp.FrameHeight), aBGR, 'raw', 'RGBA', 0, 1)
                    
                    if(img):
                       fname = os.path.join(fdir, fn)
                       img.save(fname)
                       print("\t\tCreated[%d]: %s (%d x %dpx)" % (bmp.Format, fn, bmp.FrameWidth, bmp.FrameHeight))

                    bmpcount+=1
                except Exception:
                    print("Failed to create %s of width %d height %d and format: %d" % (fn, bmp.FrameWidth, bmp.FrameHeight, bmp.Format) )
        elif(bmp.Format == EW_DRIVER_VARIANT_RGB565):
            print("EW_DRIVER_VARIANT_RGB565 format: %d of width %d height %d" % (bmp.Format, bmp.FrameWidth, bmp.FrameHeight ) )       
            
            RGB565 = decompress(s[pixel_ofs:],0,0)
                
            print("\nextract frameset (%d x %dpx)" % (bmp.FrameWidth, bmp.FrameHeight))
                            
            for f in range(0,bmp.NoOfFrames):
                frame = XBmpFrameRes(s, frame_ofs+(f*XBMPFRAMERESSIZE))
                
                #print("\t[%04d]Opq: (%d,%d) Opq %d x %d Pixel1 %d Pixel2 %d" % (f, frame.OpqX, frame.OpqY, frame.OpqWidth, frame.OpqHeight, frame.Pixel1, frame.Pixel2))
                fn=str("f565img_%04d_%02dof%02d.png" % ( bmpcount, f,bmp.NoOfFrames))
                sz=bmp.FrameWidth* bmp.FrameHeight
                frame = XBmpFrameRes(s, frame_ofs)
                framebuf=RGB565[frame.Pixel1:frame.Pixel1+sz]
                
                aBGR = RGB565_to_8888(  framebuf  )
                    
                img=Image.frombuffer('L', (bmp.FrameWidth, bmp.FrameHeight), aBGR, 'raw', 'L', 0, 1)
                
                if(img):
                    fname = os.path.join(fdir, fn)
                    ppyt(fname)
                    print("\t\tCreated: %s (%d x %dpx)" % ( fn, bmp.FrameWidth, bmp.FrameHeight))
                else:
                    print("error creating img")
            bmpcount+=1                                         
        else:
            print("Don't know how to handle format: %d of width %d height %d" % (bmp.Format, bmp.FrameWidth, bmp.FrameHeight ) )                                            
        return 1

# EwCreateIndex8Surface aHeight * aWidth + 1040   // size + 1024
## Buffer size Size 4 * width * height + 12  // size 4 * width * height

            
print("Extracting bitmaps from DATA.bin")

start = BASE_ADDR

li = open("DATA.bin","rb")

for vol in parser(li):
    #only load section 4
    if(vol.vid == 4):
        buf = vol.buf
        size = vol.size
        end = start + size
        print ("Found RTOS size %x" % size)

print("Extracting GOPRO's Camera's bitmaps")
li.close()
s=bytes(buf)
bmp_idx=0

if not os.path.exists(bdir):
    os.makedirs(bdir)

if not os.path.exists(fdir):
    os.makedirs(fdir)

while 1:
    # Now find the Magic key for the first bmp
    bmp_idx = s.find(BMP_MAGIC,bmp_idx)
    
    print("found magic at  %x" % (bmp_idx+BASE_ADDR))

    if (bmp_idx == -1):
        print("No more bitmaps")
        exit()

    l=CreateNextFile(s,bmp_idx)        
    if l == 0:
        break
    
    bmp_idx+=4

print("Done")