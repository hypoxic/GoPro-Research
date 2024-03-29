"""
A script that extracts GoPro Binary
 
The script uses very basic shellcode extraction algorithm

Copyright (c) 2018 Hypoxic
ALL RIGHTS RESERVED.

Revision history
=========================
v1.0 - initial version

"""

import re
import zlib
import struct

try:
    import idaapi
    from idc import *
    ida = True
except:
    ida = False

MAGIC_HDR = "MILBEAUT"
BASE_ADDR = 0x40080000
#DATA_ADDR = 0x41732800
DATA_ADDR = 0x40FB2F90  # search for 0xA9BF73FBA9BF7BFD

END_ADDR  = 0x50000000
H10HDRSIZE = 0x200


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
        self.size =  li.size()
        li.seek(0)
        self.f = li
        
    def __iter__(self):
        return self

#    def __next__(self):
    def next(self):
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
        except:
            raise StopIteration
  
# -----------------------------------------------------------------------
def accept_file(li, filename):
    """
    Check if the file is of supported format
    @param li: a file-like object which can be used to access the input data
    @param filename : filename
    @return: 0 - no more supported formats
             string "name" - format name to display in the chooser dialog
             dictionary { 'format': "name", 'options': integer }
               options: should be 1, possibly ORed with ACCEPT_FIRST (0x8000)
               to
    """   
    retval = ""
        
    for vol in parser(li):
        if(vol.vid == 4):
            retval = "GP2 Update Loader Section %d of size %d bytes" % (vol.vid, vol.size)

    return retval


def add_xrefs(addr, end=idc.BADADDR):
    """
        https://github.com/xyzz/vita-ida-physdump/blob/master/vita_phys_dump.py
        Searches for MOV / MOVT pair, probably separated by few instructions,
        and adds xrefs to things that look like addresses
    """    
    while addr < end and addr != BADADDR:
        addr = idc.NextHead(addr)
        if idc.GetMnem(addr) in ["MOV", "MOVW"]:
            reg = idc.GetOpnd(addr, 0)
            if idc.GetOpnd(addr, 1)[0] != "#":
                continue
            val = idc.GetOperandValue(addr, 1)
            found = False
            next_addr = addr
            for x in range(16):
                next_addr = idc.NextHead(next_addr)
                if idc.GetMnem(next_addr) in ["B", "BX"]:
                    break
                # TODO: we could handle a lot more situations if we follow branches, but it's getting complicated
                # if there's a function call and our register is scratch, it will probably get corrupted, bail out
                if idc.GetMnem(next_addr) in ["BL", "BLX"] and reg in ["R0", "R1", "R2", "R3"]:
                    break
                # if we see a MOVT, do the match!
                if idc.GetMnem(next_addr) in ["MOVT", "MOVT.W"] and idc.GetOpnd(next_addr, 0) == reg:
                    if idc.GetOpnd(next_addr, 1)[0] == "#":
                        found = True
                        val += idc.GetOperandValue(next_addr, 1) * (2 ** 16)
                    break
                # if we see something other than MOVT doing something to the register, bail out
                if idc.GetOpnd(next_addr, 0) == reg or idc.GetOpnd(next_addr, 1) == reg:
                    break
            if val & 0xFFFF0000 == 0:
                continue
            if found:
                # pair of MOV/MOVT
                try:
                    idc.OpOffEx(addr, 1, idc.REF_LOW16, val, 0, 0)
                    idc.OpOffEx(next_addr, 1, idc.REF_HIGH16, val, 0, 0)
                except:
                    print "Failed xref @ %x next_addr %x val %x" % (addr, next_addr, val)
            else:
                # a single MOV instruction
                try:
                    idc.OpOff(addr, 1, 0)
                except:
                    print "Failed xref at addr %x" % (addr)
                    

def MakeUnknownCode(start,end):   
    """
        Makes code in the data section that is not made yet
        @param start Start address
        @param start End address

    """
    addr = start
    
    while addr < end and addr != BADADDR:			
        addr = find_unknown(addr, idaapi.SEARCH_DOWN)
        if(addr % 4):
        	addr = (addr & 0xFFFFFFFC)+4
        	        
        if isUnknown(GetFlags(addr)) and idc.Qword(addr) != 0:
            #print "C 0x%08x" % addr
            MakeCode(addr)
    
def MakeUnknownFncs(start, end):
    """
        Makes code that is not yet a function a function
        @param start Start address
        @param start End address

    """
    addr = start

    while addr < end and addr != BADADDR:
        if idc.Qword(addr) != 0 and isCode(GetFlags(addr)) and (idc.GetMnem(addr) != "NOP") and not (idaapi.get_func(addr)):
            #print "N 0x%08x" % addr
            idc.MakeFunction(addr, idaapi.BADADDR)        
        addr = NextHead(addr, BADADDR)

def findEW():
    # find EwDecompress
    addr = FindBinary(0, SEARCH_DOWN, "FD 7B BA A9 FD 03 00 91 F5 5B 02 A9 75 B1 02 B0 A7 96 46 F9 F3 53 01 A9  F4 03 00 AA 13 00 40 B9");

    EwDecompress = GetFunctionAttr(addr-0x8, FUNCATTR_START)
    print("EwDecompress at 0x%x" % EwDecompress) 
    idc.MakeName(EwDecompress, "EwDecompress")

    i = 0
    for xref in XrefsTo(EwDecompress):
        print(xref.frm)
        if i == 0:
            EwLoadString = GetFunctionAttr(xref.frm, FUNCATTR_START)
            idc.MakeName(EwLoadString, "EwLoadString")
            print("EwLoadString %x" % EwLoadString)
        elif i == 1:        
            EwLoadUnified = GetFunctionAttr(xref.frm, FUNCATTR_START)
            idc.MakeName(EwLoadUnified, "EwLoadUnified")
            print("EwLoadUnified %x" % EwLoadUnified)
        i += 1
                       
    print("now run getstringvariants")

# -----------------------------------------------------------------------
def load_file(li, neflags, format):

    """
    Load the file into database

    @param li: a file-like object which can be used to access the input data
    @param neflags: options selected by the user, see loader.hpp
    @return: 0-failure, 1-ok
    """

    # Select the PC processor module
    idaapi.set_processor_type("ARM:ARMv8", SETPROC_ALL|SETPROC_FATAL)
    inf = idaapi.get_inf_structure()
    inf.af &= ~idc.AF_MARKCODE  # this is so that IDA does not find functions inside .data segments
    inf.af2 &= ~idc.AF2_FTAIL  # don't create function tails
    inf.af2 |= idc.AF2_PURDAT  # control flow to data segment is ignored 

    start = BASE_ADDR

    for vol in parser(li):
        #only load section 4
        if(vol.vid == 4):
            print "Found RTOS"
            buf = vol.buf
            size = vol.size
            end = start + size
            
            # find the data location
            faddr = buf.find(b'\xFD\x7B\xBF\xA9\xFB\x73\xBF\xA9\xF9\x6B\xBF\xA9\xF7\x63\xBF\xA9\xF5\x5B\xBF\xA9\xF3\x53\xBF\xA9\xFD\x7B\xBF\xA9\xFB\x73\xBF\xA9\xF9\x6B\xBF\xA9\xF7\x63\xBF\xA9\xF5\x5B\xBF\xA9\xF3\x53\xBF\xA9');
            if (faddr == -1):
                print("Data End signature not found, %x" % faddr)
                exit()
                
            print("found code end at 0x%x" % faddr)                
            DATA_ADDR = faddr + BASE_ADDR

            #Code Segment
            print "1) Creating Code Section"
            seg = idaapi.segment_t()
            seg.start_ea = start
            seg.end_ea   = DATA_ADDR
            seg.bitness  = 2 # 64-bit
            idaapi.add_segm_ex(seg, "RTOS", "CODE", 0)
            
            #Data Segment
            print "2) Creating Data Section"
            segdata = idaapi.segment_t()
            segdata.start_ea = DATA_ADDR
            segdata.end_ea   = END_ADDR
            segdata.bitness =  2 # 64-bit  
            idaapi.add_segm_ex(segdata, "RTOS", "DATA", 1)
                        
            # now load the memory
            print "3) Loading Memory"
            idaapi.mem2base(buf, start, end)
            
            # Mark for analysis
            print "4) First Pass Analalzying Code"
            idaapi.add_entry(start, start, "start", 1)
            plan_and_wait( seg.start_ea,seg.end_ea,True)
            auto_wait()
            
            idc.Wait()
            
            print "5) Making unknown Code"
            MakeUnknownCode(seg.start_ea,seg.end_ea)  

            print "6) Making Functions"
            MakeUnknownFncs(seg.start_ea,seg.end_ea)

            print "7) Analyzing system instructions"
            from highlight_arm_system_insn import run_script
            run_script()
            
            print "9) Find EWStrings"
            findEW()
            
            print "10) Analyze Data Section"
            plan_and_wait( segdata.start_ea, segdata.end_ea, True)
            
            
            print "11) !!!!!!!!!!!!!!!!!!BE SURE TO load hero10.sig!!!!!!!!!!!!!!"            
            auto_wait()
            
            break

    return 1

# -----------------------------------------------------------------------
def main():
    return 1

if not ida:
    main()
