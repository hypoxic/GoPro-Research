# Hypoxic 2019 
#  Gopro BLE WSDK functions protobuf extracted pyhton example. 
#
# You'll need protobuf installed 'pip install protobuf'

# Since we are  running one level down, you need to add `wsdk` to your module search path
import binascii
import sys

# needed to run in subdirectory
sys.path.append('./wsdk/')

from wsdk.WSDK_RequestSetBandSelect_pb2 import WSDK_RequestSetBandSelect
from wsdk.wsdkCommands.WSDK_EnumBandSelect_pb2 import WSDK_EnumBandSelect

def WSDK_SetBandSelect(v = 2):
    RequestSetBandSelect = WSDK_RequestSetBandSelect()
    
    if v == 2:
        RequestSetBandSelect.band_select = WSDK_EnumBandSelect.WSDK_BAND_SELECT_2_4GHZ
    if v == 5:            
        RequestSetBandSelect.band_select = WSDK_EnumBandSelect.BAND_SELECT_5GHZ
        
    print(binascii.hexlify(RequestSetBandSelect.SerializeToString()))

WSDK_SetBandSelect(5)