import codecs
from idautils import *
from idc import *
from idaapi import *
from decompress import decompress
from array import *
import binascii 
import re

#
# Finds all the Embedded Wizard Strings by using the xrefs to EwLoadString
# then writes them all the a file. Set's the string's comment and makes the name
#


FNC="EwLoadString"

minaddr=0x40080000
maxaddr=0x50000000


LOG=1       # write a file
OUTPUT=0    #Output to screen
COMMENT_IDA = 1 #Back fill into ida

# finds the end of the utf-16 string in the bytearray and returns it
def getstring(b,idx):
    start=2*sidx
    end = b.find("\0\0",start)+1
    
    # Fixes a unicode before null issue
    if (end % 2):
        end = end+1
    
    tbuff=pbuff[start:end]
    
    #fixes null string issue
    if (start+1 == end):
        return ""
        
    try:
        stringout=tbuff.decode('utf-16')
    except:    
        print("exception: idx %d %d-%d buff %s" % (sidx, start,end,l,str(binascii.hexlify(tbuff)) ))
        return "EXCEPTION"
    else:                              
        return stringout

def getADRPvalue(calledat):
    v=0
    func = idaapi.get_func(calledat)
    if not func:
        print("function at %x undef" % (calledat))
        return 0
            
    fstartea = func.startEA
    
    # ignore unified
    if (fstartea == 0xA1134B3C):
        #print("unified")
        return 0
    
    instructions=calledat-fstartea+4
    #print("\tInstructions %x %x-%x" % (instructions, calledat , fstartea))
    reg = 0x81
    for i in range(4, instructions, 4):
        m = idc.GetMnem(calledat-i)
        t = idc.GetOpType(calledat-i,0)
        o = idc.GetOperandValue(calledat-i,0)
        oo = idc.GetOperandValue(calledat-i,1)
        ooo = idc.GetOperandValue(calledat-i,2)
        
        #print("m=%s t=%d o=%x o=%x o=%x" % (m,t,o,oo,ooo) )
        
        if m.startswith('ADRP') and o == 0x81:
            t = idc.GetOpType(calledat-i,1)
            if (t == idc.o_imm and o == 0x81): 
                v |= oo
                #print("ADRP %d %x" % (i, v))  
                break
        elif m.startswith('ADD'):
            t = idc.GetOpType(calledat-i,2)
            if (t == idc.o_imm and o == 0x81): 
                v |= idc.GetOperandValue(calledat-i,2)    
                #print( "v 0x%x" % v)
            #else:
                #print( "[%d] mov type:%x value:%x %d" % (i,t,oo, idc.o_imm))                      
        #else:
            #print("[%d] %s" % (i,m))

    if(v >= minaddr and v < maxaddr):
        return v
    else:
        return 0

ea = BeginEA()

functionName=""
for segea in Segments():        
    minaddr=SegStart(segea)
    for funcea in Functions(SegStart(segea), SegEnd(segea)):
        functionName = GetFunctionName(funcea)
        if (functionName == FNC):
            break
    
    if (functionName == FNC):
        break 

if (functionName != FNC):       
    print("can't find %s, ensure case" % (FNC))
    idc.Exit
    
print("\nCreating strings from Embedded Wizard compressed files.\nNeed to run within IDA with %s found\n\tFound %s at %x" % (functionName,functionName,funcea))
xrefs = XrefsTo(funcea, 0)
#print(xrefs)
XStringRes = []

for x in xrefs:
    calledat = x.frm
    #print(hex(calledat))

    args = idaapi.get_arg_addrs(calledat)  
    #print(hex(calledat))
    
    if (args == None):
        res = getADRPvalue(calledat)
        if( res != 0 ):
            XStringRes.append(res)            
        #print("[%x] Nonresolved" % (calledat))
    else:   
        print("args " + args)
        XStringRes.append(get_operand_value(args[0], 1))

#print (XStringRes)

if (LOG):
    f = codecs.open('EWStringsConst_utf16.txt','w',encoding='utf-8')
    f.write("Hypoxic's GoPro Camera Embedded Wizard String Decompressor.\n")
    root_filename   = idaapi.get_root_filename()
    f.write("Extracted from %s\n" % root_filename)

lastblock=0
count=0

decodedstrs = []

for stringconst in XStringRes:
    # don't display list twice
    if stringconst not in decodedstrs:
        decodedstrs.append(stringconst)
        #print (hex(stringconst))
    
        # extract the block ptr and the offset within the decompressed file
        block = Qword(stringconst)
        sidx = Qword(stringconst+8)
        compsize = Dword(block)
        
        if (block > minaddr and block < maxaddr and compsize > 0x10 and compsize < 0x10000):       
            if(block != lastblock):
                print("Loading block %x %x" % (block, compsize))
                sc = idc.GetManyBytes(block+4, compsize+0x1000)
                pbuff=bytearray(decompress(sc,0,0))
                lastblock = block
            
            stringout=getstring(pbuff, sidx)
            if (len(stringout) > 0):
                count+=1
                
                sf = "[%08x] %s" % (stringconst, stringout)
                if(OUTPUT):
                    print(sf)
                
                if (LOG):
                    f.write("%s\n" % sf)
                
                if (COMMENT_IDA):
                    # might as well back feed this into ida
                    sascii=stringout.encode('ascii', 'replace').decode().encode("ascii")
                            
                    #set the comment
                    MakeComm(stringconst, sascii)
                    
                    #set the name, shorten and remove whitespace
                    sa_name = re.sub('[^0-9a-zA-Z]+', '_', sascii)[0:30]
                    if(sa_name[0].isdigit()):
                        sa_name = 'Z' + sa_name[1:]
                    idc.GetFunctionName(ea)            
                    
                    set_name(stringconst,sa_name, idc.SN_NOWARN)
                    #break

if (LOG):
    f.close()   

print("Finished. Found %d strings" % count)    
