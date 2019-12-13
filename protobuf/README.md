# GoPro HERO8 WSDK Protobuf extraction
## For public GoPro HERO8 information

* GoPro's BLE WSDK protobuf extracted via [protod](https://github.com/hypoxic/Protod). Used by BLE on newer cameras. Extracted from gpBLESDK binary and modified to compile correctly. 
Learn more about [Google Protobuf](https://developers.google.com/protocol-buffers/docs/overview)    

To compile for pyhton
````../protoc/protoc -I=./ --python_out=../wdskout/ *.proto````
Use the protoc compiler from google, scroll down and used precompiled [protoc](https://developers.google.com/protocol-buffers/docs/downloads.html)

BLE Commands   
most are not tested
````

class CCCD_MODE:
    OFF = 0
    NOTIFY = 1
    INDICATE = 2

# Standard BLE Cmds
class BLECOMMAND:
    eBleCommandShutter                    =1 
    eBleCommandMode                       =2 
    eBleCommandModeSubMode                =3 
    eBleCommandPower                      =4 
    eBleCommandSleep                      =5 
    eBleCommandCancelWifiRemotePair       =8 
    eBleCommandVideoProtuneReset          =10 
    eBleCommandMultiShotProtuneRes        =11 
    eBleCommandPhotoProtuneReset          =12 
    eBleCommandSetDateAndTime             =13
    eBleCommandGetDateAndTime             =14 
    eBleCommandLocate                     =22 
    eBleCommandAPControl                  =23 
    eBleCommandTagMoment                  =24 
    eBleCommandRemotePair                 =25 
    eBleCommandVoiceEditMyStory           =26 
    eBleCommandVoicePhotoTake             =32 
    eBleCommandVoiceVideoStart            =33 
    eBleCommandVoiceVideoStop             =34 
    eBleCommandVoiceTimelapseStart        =35 
    eBleCommandVoiceTimelapseStop         =36 
    eBleCommandVoiceBurstTake             =37 
    eBleCommandVoiceTag                   =38 
    eBleCommandVoiceDeleteLast            =39 
    eBleCommandSettingsJSONVersion        =58 
    eBleCommandSettingsJSON               =59 
    eBleCommandCameraInfo                 =60 
    eBleCommandBLEControl                 =61  
    eBleCommandSetMode                    =62 
    eBleCommandProtuneReset               =63 
    eBleCommandSetPreset                  =64 
    eBleCommandProtobufCmdLow             =240  # execute pb={%02x %02x %02x %02x %02x}  
    eBleCommandProtobufCmdHigh            =241

# eBleCommandProtobufCmdLow->WSDK
class WSDK:  
    WSDK_CMD_ID_REQUEST_PRESET_REMOVE = 110
    WSDK_CMD_ID_REQUEST_SHORTCUTS_RESET = 111
    WSDK_CMD_ID_REQUEST_SET_TIMEWARP1X = 113
    WSDK_CMD_ID_REQUEST_SET_PRESET_EDIT_START = 114
    WSDK_CMD_ID_REQUEST_SET_PRESET_EDIT_CANCEL = 115
    WSDK_CMD_ID_REQUEST_SET_PRESET_EDIT_STORE = 116
    WSDK_CMD_ID_REQUEST_SET_PRESET_FACTORY_RESET = 117
    WSDK_CMD_ID_REQUEST_PRESET_CREATE = 118
    WSDK_CMD_ID_REQUEST_PRESET_SET_ORDER = 119
    WSDK_CMD_ID_REQUEST_RELEASE_NETWORK = 120
    WSDK_CMD_ID_REQUEST_SET_LIVE_STREAM = 121
    WSDK_CMD_ID_REQUEST_SET_OTA_CMD = 122
    WSDK_CMD_ID_REQUEST_SET_BAND_SELECT = 123
    WSDK_CMD_ID_REQUEST_CLEAR_MOBILE_OFFLOAD_NEW_MEDIA_FLAG = 124
    WSDK_CMD_ID_REQUEST_SET_SYSTEM_NOTIFY_EVENT = 125
    WSDK_CMD_ID_REQUEST_SET_CLIENT_INFO = 126
    WSDK_CMD_ID_REQUEST_SET_CAH_SETUP_MODE = 127
    
    

# Extract_ProtoBuff_from_CMSPkt 
WSDK_COMMAND = {
    'SN_CMD' : 1,  # SNIPER COMMAND
    'NETWORK_MANAGEMENT' : 2, # NETWORK_MANAGEMENT 'PN'
    'WIRELESS_MANAGEMENT' : 3  # WIRELESS_MANAGEMENT_COMMAND 'PB'
}
    
WIRELESS_MANAGEMENT_COMMAND = {
    'PING' : 0,
    'PAIRING_FINISH' : 1,
    'SET_SUSPEND_SEQUENCE' : 2,
    'SET_RESUME_SEQUENCE' : 3,
    'SET_COLDBOOT_SEQUENCE' : 4,
    'PAIR_BTC' : 5,
    'EVENT_NOTIF_PAIR_BTC' : 6,
    'CONNECT_BTC' : 7 ,
    'EVENT_NOTIF_CONNECT_BTC': 8,
}

NETWORK_MANAGEMENT_COMMAND = {
    'PING' : 0,
    'GET_CAPABILITIES' : 1,
    'START_SCAN' : 2,
    'GET_AP_ENTRIES' : 3,
    'CONNECT' : 4,
    'CONNECT_NEW' : 5,
    'DELETE_SINGLE' : 6,
    'DELETE_ALL' : 7,
    'TAKE_OWNERSHIP' : 8,
    'RELINQUISH_OWNERSHIP' : 9,
    'STOP_NETWORK_FEATURES' : 10,
    'EVENT_NOTIF_START_SCAN' : 11,
    'EVENT_NOTIF_PROVIS_STATE' : 12,
    'CONNECT_MFU' : 13,
}
     

````