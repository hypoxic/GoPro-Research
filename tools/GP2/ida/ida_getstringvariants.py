import time
import codecs
from idautils import *
from idc import *
from idaapi import *
idaapi.require("decompress")
from decompress import decompress
from array import *
import binascii 
import re

#
# Finds all the Embedded Wizard Strings by using the xrefs to EwLoadString
# then writes them all the a file. Set's the string's comment and makes the name
#

#FNC="EwLoadString"  #"[0m[%08lu] Can not create a string. Out of memory. 3 entry"
FNC="EwLoadUnified"  #"[0m[%08lu] Can not create a string. Out of memory. 4 entry" 

minaddr=0x40080000
maxaddr=0x50000000
MAX_LANGS=11

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
        elif m.startswith('MOV'):                                 
            if (o == 0x81): 
                print( "can't handle indirects at the moment")
                return 0
        #else:
            #print("[%d] %s" % (i,m))

    if(v >= minaddr and v < maxaddr):
        return v
    else:
        return 0
        
###
def printstrs(l,style):
    sl = l[style]
    
    for t in sl:
        print(t)
    
###### START
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

# create strings handle
strs = [[] for y in range(MAX_LANGS+1)] 

xrefs = XrefsTo(funcea, 0)
#print(xrefs)
XStringRes = []

for x in xrefs:
    calledat = x.frm
    #print(hex(calledat))

    args = idaapi.get_arg_addrs(calledat)  
    #print("\n" + hex(calledat))
    if (args == None):
        res = getADRPvalue(calledat)
        if( res != 0 ):
            #if (res == 0xa3f70000):
                #print("Bad MOV came from %x" %(calledat))
                #exit()
            print("%x %x" % (calledat, res))                
            XStringRes.append(res)            
        #else:
            #print("[%x] Nonresolved" % (calledat))
            
    else:   
        #print(args)
        res = get_operand_value(args[0], 1)
        #if (res == 0xa3f70000):
            #print("Bad came from %x" %(calledat))
      
        #XStringRes.append(res)
        print("args at %x" % calledat)
    #break


print("found xrefs, now parse them all")

lastblock=0
count=0
decodedstrs = []

# create multi dimension list for string storage
#strs = [[0 for x in range(1)] for y in range(12)] 
strs = [[u''] for y in range(12)] 

for descript in XStringRes:
    # extract the stringvariant's descriptor
    stringconst = Qword(descript)
    langcount = Qword(descript+8)
    
    #print("stringconst %x langcount %x" % (stringconst, langcount))
    
    if (stringconst < minaddr or stringconst > maxaddr or langcount > 15):
        print("SKIPPING: bad ptr descript: %x, stringconst = 0x%x, langcount = %x" % (descript, stringconst, langcount))
        continue
    
    # don't display list twice
    if stringconst not in decodedstrs:
        decodedstrs.append(stringconst)
    
        for ofs in range(0, langcount*0xC, 0xC):
            #Now extract the x string
            curstringconst = stringconst+ofs*2
            
            style = Qword(curstringconst)
            
            #print("curstringconst %x style %x " % (curstringconst, style))
            
            if (style > MAX_LANGS):
                print("bad style:%x str+ofs:%x descript:0x%x ofs:%x langcount: %x" % (style, stringconst+ofs, descript, ofs, langcount))
                print("skipping block")
            else:    
                block = Qword(curstringconst+8)
                sidx  = Qword(curstringconst+0x10)
                
                #look ahead and get the uncompresed size
                compsize = Dword(block)
                
                if (block > minaddr and block < maxaddr and compsize > 0x10 and compsize < 0x10000):       
                    if(block != lastblock):
                        sc = idc.GetManyBytes(block+4, compsize+0x1000)  # at a bit more as we only know the uncompressed size
                        pbuff=bytearray(decompress(sc,0,0))
                        lastblock = block
                    
                    stringout=getstring(pbuff, sidx)
                    count+=1
                    
                    #sf = "\t[%02d::%08x:%04d] %s" % (style, block, sidx, stringout)
                    sf = u"[%08x] %s\n" % (curstringconst, stringout)
                    #print(sf)
                    
                    # append it to a list
                    strs[style].append(sf)

                    # if english, comment it
                    if (style == 0):    
                        #print(descript)
                        # might as well back feed this into ida
                        sascii=stringout.encode('ascii', 'replace').decode().encode("ascii")
                        sascii="EW_" + sascii                                
                        #set the comment
                        ###### TRUNK TEST MakeComm(descript, sascii)
                        
                        #set the name, shorten and remove whitespace
                        sa_name = re.sub('[^0-9a-zA-Z]+', '_', sascii)[0:30]
                        #if(sa_name[0].isdigit()):
                        #    sa_name = 'Z' + sa_name[1:]
                        
                        ###### TRUNK TEST set_name(descript,sa_name, idc.SN_NOWARN)
                        #print(hex(descript))
    ###break

for i in range(MAX_LANGS):
    fn=str("EWStringsVariants_%02d_utf16.txt" % i)
    f = codecs.open(fn,'w',encoding='utf-8')
    f.write("Hypoxic's GoPro Camera Embedded Wizard String Variants Decompressor.\n")
    root_filename   = idaapi.get_root_filename()
    f.write("Extracted from %s\n" % root_filename)

    sl = strs[i]

    print("creating file for style %02d of len %d name: %s" % (i, len(sl), fn))
    for t in sl:
        f.write(t)    

    f.close()   

print("Finished. Found %d strings" % (count))    