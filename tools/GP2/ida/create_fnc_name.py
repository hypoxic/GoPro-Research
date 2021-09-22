import idaapi
import idc
import idautils
import ida_offset
import ida_auto, ida_kernwin, ida_diskio
import re

BADADDR=0xffffffffffffffff

#Based on Evil Wombats's Analyzer. Updated to GP2
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
    if ea != BADADDR:
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
    