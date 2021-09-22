# GP2 IDA Scripts

* __hero10.sig__ Signature file for some functions expanded from various assert scripts and intuition
* __binldr64.py__ Loads RTOS binary image into IDA
* __highlight_arm_system_insn.py__ Script to expand aarch64 CPU calls
* __name__,__create_fnc_name__ Names functions based upon asserts. Note, no need to use this if you apply the signature.
* __ida_getstrings__, __ida_getstringvariants__ - Extracts most of the strings from the compressed Embedded Wizard blobs. Adds comments and names. Note: The script does not work hard at dermining the arguments so a few are dropped. Use IDA binldr64 to determine address of EwLoadString and EwLoadUnified
* __decompress.py__ - Used to decompress Embedded Wizard bmp and IDA strings 