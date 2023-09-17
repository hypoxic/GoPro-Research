#!/usr/bin/env python

"""
Dumps out the information from a GoPro Crash Log. 
Author Trunk/Hypoxic
"""

import binascii
import re
import string
import csv
import sys
from datetime import datetime

def getLocU16(s, idx):
    v=int.from_bytes(s[idx:idx+2], byteorder='little')
    return v  
  
def getLocInt(s, idx):
    v=int.from_bytes(s[idx:idx+4], byteorder='little')
    return v    

def getDword(s, idx):
    return s[idx:idx+4]

def getLocInt64(s, idx):
    v=int.from_bytes(s[idx:idx+8], byteorder='little')
    return v    
    
def getFdrName(s, idx):
    try:
        ba = bytearray(s[idx:idx+4]) 
        #print("fdr: %s" % binascii.hexlify(ba) )
        n = ba.decode("utf-8")     
        #print(n)
        return n    
    except:
        print ("getFdrName failed")
        
def getLine(s,ptr,textlen):
    try:
        text = s[ptr:ptr+textlen]          
        text = text.decode("utf-8")      
        #print(text)
        return text
    except:
        pass
        #print("---BAD DECODE---")              

def escape_ansi(line):
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

class header:
    def __init__(self,b,idx,expected):
        self.name = b[idx:idx+17].decode("utf-8") 
        self.offset = self.size = 0
        if(self.name != expected):
            self.offset = getLocInt(b,idx+17)
            self.size = getLocInt(b,idx+21)

        self.idx = idx+21+4
        
    def print(self):
        print("%s offset 0x%x len 0x%x" % (self.name, self.offset, self.size))

#
def print_log(mem, ptr):    
    for i in range(0,4096):
        #print(binascii.hexlify(mem[ptr:ptr+0x40]))
        hdr_val1 = getLocInt(mem, ptr)    
        ptr += 4
        if(hdr_val1 == 0):
            print("---Done---")
            return
            
        hdr_val2 = getLocInt(mem, ptr)    
        ptr += 4
        hdr_val3 = getLocInt(mem, ptr)    
        ptr += 4
        hdr_val4 = getLocInt(mem, ptr)    
        ptr += 4
        hdr_val5 = getLocInt(mem, ptr)    
        ptr += 4
        hdr_val6 = getLocInt(mem, ptr)    
        ptr += 4
        hdr1_fdr = getFdrName(mem,ptr)
        ptr +=4    

        ptr += 0x1C

        hdr2_addr1 = getLocInt64(mem, ptr)    
        ptr += 8
        hdr2_fdr = getFdrName(mem,ptr)
        ptr +=4 

        ptr += 0x1C

        p_filename = getLocInt64(mem, ptr)
        ptr+=8    
        p_functionname = getLocInt64(mem, ptr)
        ptr+=8    
        len1 = getLocInt(mem, ptr)    
        ptr +=4    
        T = getLocInt(mem, ptr)    
        ptr +=4    
        textlen = getLocU16(mem, ptr)    
        ptr +=2
        flag = getLocU16(mem, ptr)    
        ptr +=2

        text = getLine(mem,ptr,textlen)
        text = escape_ansi(text)
        ptr+=textlen
        
        ptr = int((ptr+4-1)/4)*4 # probably a nice alignment in python
        
        if(not text):
        #if(1):
            print("p_filename=0x%x p_functionname=0x%x" % (p_filename,p_functionname))
            print("\t%s: %08x %08x %08x %08x %08x %08x" % (hdr1_fdr, hdr_val1,hdr_val2,hdr_val3,hdr_val4,hdr_val5,hdr_val6))
            print("\t%x %08x %08x" % (hdr2_addr1, len1, T))
        
        smsgtype = "I"
        
        if(T == 0xFFFFFFFF):
            sT = "->I<-"
        else:
            sT = str(" %4d"%T)        
        print("[%08d][%s] %s [T:%s] %s" % (hdr_val6,smsgtype,hdr1_fdr,sT,text))

#
def get_log_idx(mem, size):
    # Now find the base by root:root 
    root=bytearray(b'root')
    root_idx=0
    while(root_idx >= 0 and root_idx < size):
        root_idx = mem.find(root,root_idx)
        #print(hex(root_idx+0x600))
        if(root_idx < 0):
            break
        if(getDword(mem,root_idx+0x28) == root):
            break
        else:   
            root_idx+=4

    if(root_idx > 0x18):
        root_idx -= 0x18
    else:
        root_idx = -1        
        
    return root_idx
    
#     
def get_registers(rmem,size):
    # get the registers    
    pointer = 0
    regs = []
    regslen = 35

    for i in range(0,regslen):
        regs.append(getLocInt64(rmem, pointer));
        pointer += 8    

    for i in range(0,regslen):
        if(i == 31):
            name = "sp"
        elif(i == 32):
            name = "ELR_EL1"
        elif(i == 33):
            name = "SPSR_EL1"    
        elif(i == 34):
            name = "ESR_EL1"    
        else:
            name = str("x%d" % i)                    
        print("%s = 0x%016x" % (name,regs[i]))
        
    name = "Crash Location"  
    print("\n%s = 0x%08x" % (name,regs[32]))  
    
def print_caminfo(mem,size):
    caminfo_idx = 0xF
    version = getLine(mem,caminfo_idx,0x10)
    caminfo_idx += 0x10
    print(version)
    caminfo_idx += 0x10
    git = getLine(mem,caminfo_idx,0x10)
    caminfo_idx += 0x20
    print(git)
    addr1 = getLocInt64(mem, caminfo_idx)
    caminfo_idx += 0x10
    print("GITVER pointer: 0x%x" % addr1)

def main():
    if len(sys.argv) < 2:
        print("Missing arguments: %s <input>")
        return
        
    inf= sys.argv[1]    

    lined = []	
    with open(inf, "rb") as f:
        b = f.read()
        
    if not b:
        print("file read error")
        return
        
    idx = 0    
    hdr = b[idx:idx+8]    
    if(hdr != b'GpCrAsH!'):
        print("%s not dump header" % binascii.hexlify(hdr))    
        return

    idx+=0x8
    print("Crash version %d.%d.%d" % (b[idx],b[idx+1],b[idx+2]))

    idx+=3
    ci_hdr = header(b,idx,"CAMINFO")  
    CAMINFO = b[ci_hdr.offset:ci_hdr.offset+ci_hdr.size]
    idx = ci_hdr.idx
    print_caminfo(CAMINFO, ci_hdr.size)

    regs_hdr = header(b,idx,"REGS")  
    #regs_hdr.print()   
    REGS = b[regs_hdr.offset:regs_hdr.offset+regs_hdr.size]    
    idx = regs_hdr.idx    

    mem_hdr = header(b,idx,"MEMORY")  
    #mem_hdr.print()   
    #RTOS_DATA Globals Sink Cinit
    MEM = b[mem_hdr.offset:mem_hdr.offset+mem_hdr.size]    
    idx = mem_hdr.idx    

    get_registers(REGS,regs_hdr.size)

    ptr = get_log_idx(MEM,mem_hdr.size)
    if(ptr >= 0):
        print("\nFound start of log via FDR prefix root:root at %x" % (ptr+mem_hdr.offset))
        print_log(MEM,ptr)
    else:
        print("Can not find log via root:root, maybe its been running too long, or my algorithm sucks.")
        return

if __name__ == "__main__":
    main()
    
