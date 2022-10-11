import idaapi
import idc
import idautils
import ida_offset
import ida_auto, ida_kernwin, ida_diskio
import re

# "fj_print_host_info", "fj_print_host_warn", "fj_print_host_error", "fj_print_host_debug"
#functionnames=["fj_print_2", "fj_print_3", "fj_print_4", "fj_print_error", "fj_print_6", "fj_print_7", "fj_print_8", "fj_print_9"]
#functionnames=[ "fj_print_7", "fj_print_8", "fj_print_9"]
functionnames=[ "Ddim_Assertion"]

minaddr=0x40080000
maxaddr=0x50000000

#Based on Evil Wombats's Analyzer
def urlify(s):

     # Remove all non-word characters (everything except numbers and letters)
     s = re.sub(r"[^\w\s]", '', s)

     # Replace all runs of whitespace with a single dash
     s = re.sub(r"\s+", '_', s)

     return s

def get_function_start(ea):
	n = idc.GetFunctionName(ea)
	for f in idautils.Functions():
		if idc.GetFunctionName(f) == n:
			return f
	print "huh?"
	return 0
	
def function_exists(n):
    ret = False
    ea = idaapi.get_name_ea(idaapi.NT_NONE, n)
    if ea != idc.BADADDR:
        ret = True			

    return ret

def process_name(ea, new_name):
    old_name = idc.GetFunctionName(ea)
    
    #fix naming convention
    new_name = urlify(new_name)
    
    # Make sure we are not already named as we want and we 
    if not old_name == new_name:
        if "sub_" in old_name and not function_exists(new_name):
            start = get_function_start(ea)

            print "Renaming " + old_name + " to " + new_name
            idc.MakeName(start, new_name)
            
def getADRPvalue(calledat):
    v=0
    func = idaapi.get_func(calledat)
    if not func:
        print("function at %x undef" % (calledat))
        return 0
            
    fstartea = func.startEA
        
    instructions=calledat-fstartea+4
    #print("\n\tInstructions %x %x-%x" % (instructions, calledat , fstartea))
    reg = 0x82
    sreg = -1
    
    for i in range(4, instructions, 4):
        m = idc.GetMnem(calledat-i) 
        t0 = idc.GetOpType(calledat-i,0)
        t1 = idc.GetOpType(calledat-i,1)
        o = idc.GetOperandValue(calledat-i,0)
        oo = idc.GetOperandValue(calledat-i,1)
        ooo = idc.GetOperandValue(calledat-i,2)
        
        #print("[%x] m=%s t0=%d t1=%d o=%x oo=%x oo=%x" % (calledat-i, m,t0,t1,o,oo,ooo) )
        
        if m.startswith('LDR') and o == reg and t1 == o_displ:
            paddr = calledat-i-4
            
            m2 = idc.GetMnem(paddr)
            t21 = idc.GetOpType(paddr,1)
            
            #print("[%x] LDR tree m2=%s t21=%d o=%x oo=%x oo=%x" % (paddr, m2,t21,o,oo,ooo) )
            
            if m2.startswith('ADD') and idc.GetOpType(paddr,2) == o_imm:
                #print("[%x] t21=%x ooo= %x" % (paddr, idc.GetOpType(paddr,2), idc.GetOperandValue(paddr,2) ) )
                v = idc.GetOperandValue(paddr,2)
                
                # step back one
                paddr = paddr-4
                m2 = idc.GetMnem(paddr)
                t21 = idc.GetOpType(paddr,1)
                o = idc.GetOperandValue(paddr,0)
                oo = idc.GetOperandValue(paddr,1)
                ooo = idc.GetOperandValue(paddr,2)
                #print("[%x] backstep m2=%s t21=%d o=%x oo=%x oo=%x" % (paddr, m2,t21,o,oo,ooo) )
                
                ##if m2.startswith('ADRP') and t21 == o_imm and o == 0x81:        
                ##    print("%x ADRP found 0x%x\n" % (calledat, v))
                ##    break
            
            if m2.startswith('ADRP') and t21 == o_imm and o == 0x81:
                v |= idc.GetOperandValue(paddr,1)
                #print("%x ADRP found 0x%x" % (calledat, v))
                break
            elif m2.startswith('ADRP') and t21 == o_imm and o == 0x82:
                v = oo | idc.GetOperandValue(paddr,1)
                #print("%x ADRP found 0x%x" % (calledat, v))
                break                
            else:
                print("can't handle this calling convention\n[%x] m2=%s t21=%d o=%x oo=%x oo=%x" % (calledat, m2,t21,o,oo,ooo) )
                break
                
        elif m.startswith('MOV') and t1 == o_reg  and o == reg: 
            #print(m)      
            sreg = oo
            print("%x ignoring" % calledat)
            break
        
    if(v >= minaddr and v < maxaddr):
        return v
    else:
        return 0

            
def get_assert_offset(xref_ea):
    xref_ea -= 0x20
    low_ea = high_ea = off = -1
    
    for ea in range(xref_ea, xref_ea+0x44, 0x4):
        mnem = idc.GetMnem(ea)   
        s0 = idc.get_operand_value(ea, 0) 
        s1 = idc.get_operand_value(ea, 1) 
        s2 = idc.get_operand_value(ea, 2) 
    
        if(s0 == 0x88):
            #print("%s\n%s %x %x %x" % (idc.GetDisasm(ea), mnem, s0, s1, s2))
            
            if(mnem == "ADRP"):
                high_ea = s1
            elif(mnem == "ADD"):
                low_ea = s2
            elif(mnem == "MOV"):
                low_ea = s2          
                
            if(high_ea != -1 and low_ea != -1):
                off = high_ea | low_ea
                break
    
    if (off == -1):
        print("not found at = 0x%x" % (xref_ea+0x20))

    return (off)
    
def process_ref(ea):
    # Collects the function name from the MOV #lit, R3 and then renames the function
    off = get_assert_offset(ea)
    
    if( off == -1 ):
        return

    #print("off2=%x" % off)
        
    str_val = idc.GetString(off)
    
    #check if the name is already taken
    process_name(ea, str_val)
        
def process_assert_xrefs(ea):
    # create a list of references to this assert string const
	r = idautils.DataRefsTo(ea)
	
	# go through each xref and rename the function accordingly
	for i in r:
		process_ref(i)
	
def name_funcs():
    #if s is already created, don't recreate
    idc.GetMnem(0x48000000)
            
    try:
       strl     
    except:
        print "Building Strings list...."
        strl = idautils.Strings();
        strl.setup(strtypes=[0])
        #strl.setup(strtypes=[ASCSTR_C])
        #strl.setup(Strings.STR_C);

    print "Iterating through strings"
    for x in strl:
        if "**************** ERROR: Assertion" in str(x):
            process_assert_xrefs(x.ea)
    
def find_n_name_function(fnc):
    functionName=""
    for segea in Segments():        
        minaddr=SegStart(segea)
        for funcea in Functions(SegStart(segea), SegEnd(segea)):
            functionName = GetFunctionName(funcea)
            if (functionName == fnc):
                break
        
        if (functionName == fnc):
            break 

    if (functionName != fnc):       
        print("can't find %s, ensure case" % (fnc))
        idc.Exit
        
    print("\nCreating functions from %s calls\n\tFound %s at %x" % (functionName, functionName,funcea))

    xrefs = XrefsTo(funcea, 0)   
    count = 0

    for x in xrefs:
        ea = x.frm
        
        args = idaapi.get_arg_addrs(ea)  

        if (args == None):
            off = getADRPvalue(ea)
            if(not off):
                continue
                
            # ptr to ptr            
            stroff = idc.Qword(off)
            str_val = idc.GetString(stroff)
            
            print("%x %s" % (ea, str_val))
            #check if the name is already taken
            process_name(ea, str_val)
            count += 1
            
    return count            
            
    
count = 0            
for fnc in functionnames:
    count += find_n_name_function(fnc)          
    
print ("replaced %d function names " %count    )
    