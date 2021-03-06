# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: WSDK_NotifyCAHStatus.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from wsdkCommands import WSDK_EnumDeviceMgrState_pb2 as wsdkCommands_dot_WSDK__EnumDeviceMgrState__pb2
from wsdkCommands import WSDK_EnumWOM_pb2 as wsdkCommands_dot_WSDK__EnumWOM__pb2
from wsdkCommands import WSDK_EnumCAHA_pb2 as wsdkCommands_dot_WSDK__EnumCAHA__pb2
from wsdkCommands import WSDK_EnumAuthState_pb2 as wsdkCommands_dot_WSDK__EnumAuthState__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='WSDK_NotifyCAHStatus.proto',
  package='wsdk_commands',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=b'\n\x1aWSDK_NotifyCAHStatus.proto\x12\rwsdk_commands\x1a*wsdkCommands/WSDK_EnumDeviceMgrState.proto\x1a\x1fwsdkCommands/WSDK_EnumWOM.proto\x1a wsdkCommands/WSDK_EnumCAHA.proto\x1a%wsdkCommands/WSDK_EnumAuthState.proto\"\xa7\x06\n\x14WSDK_NotifyCAHStatus\x12@\n\x10\x64\x65vice_mgr_state\x18\x01 \x01(\x0e\x32&.wsdk_commands.WSDK_EnumDeviceMgrState\x12<\n\x0e\x64\x65vice_mgr_cat\x18\x02 \x01(\x0e\x32$.wsdk_commands.WSDK_EnumDeviceMgrCat\x12<\n\x0e\x64\x65vice_mgr_sub\x18\x03 \x01(\x0e\x32$.wsdk_commands.WSDK_EnumDeviceMgrSub\x12<\n\x0e\x64\x65vice_mgr_err\x18\x04 \x01(\x0e\x32$.wsdk_commands.WSDK_EnumDeviceMgrErr\x12\x33\n\twom_state\x18\x05 \x01(\x0e\x32 .wsdk_commands.WSDK_EnumWOMState\x12/\n\x07wom_cat\x18\x06 \x01(\x0e\x32\x1e.wsdk_commands.WSDK_EnumWOMCat\x12/\n\x07wom_sub\x18\x07 \x01(\x0e\x32\x1e.wsdk_commands.WSDK_EnumWOMSub\x12/\n\x07wom_err\x18\x08 \x01(\x0e\x32\x1e.wsdk_commands.WSDK_EnumWOMErr\x12\x35\n\ncaha_state\x18\t \x01(\x0e\x32!.wsdk_commands.WSDK_EnumCAHAState\x12\x31\n\x08\x63\x61ha_cat\x18\n \x01(\x0e\x32\x1f.wsdk_commands.WSDK_EnumCAHACat\x12\x31\n\x08\x63\x61ha_sub\x18\x0b \x01(\x0e\x32\x1f.wsdk_commands.WSDK_EnumCAHASub\x12\x31\n\x08\x63\x61ha_err\x18\x0c \x01(\x0e\x32\x1f.wsdk_commands.WSDK_EnumCAHAErr\x12\x12\n\ncah_active\x18\r \x01(\x08\x12\x1a\n\x12\x63\x61h_feature_enable\x18\x0e \x01(\x08\x12\x39\n\x0e\x63\x61h_auth_state\x18\x0f \x01(\x0e\x32!.wsdk_commands.WSDK_EnumAuthState\x12\x10\n\x08\x63\x61h_busy\x18\x10 \x01(\x08'
  ,
  dependencies=[wsdkCommands_dot_WSDK__EnumDeviceMgrState__pb2.DESCRIPTOR,wsdkCommands_dot_WSDK__EnumWOM__pb2.DESCRIPTOR,wsdkCommands_dot_WSDK__EnumCAHA__pb2.DESCRIPTOR,wsdkCommands_dot_WSDK__EnumAuthState__pb2.DESCRIPTOR,])




_WSDK_NOTIFYCAHSTATUS = _descriptor.Descriptor(
  name='WSDK_NotifyCAHStatus',
  full_name='wsdk_commands.WSDK_NotifyCAHStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='device_mgr_state', full_name='wsdk_commands.WSDK_NotifyCAHStatus.device_mgr_state', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='device_mgr_cat', full_name='wsdk_commands.WSDK_NotifyCAHStatus.device_mgr_cat', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='device_mgr_sub', full_name='wsdk_commands.WSDK_NotifyCAHStatus.device_mgr_sub', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='device_mgr_err', full_name='wsdk_commands.WSDK_NotifyCAHStatus.device_mgr_err', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='wom_state', full_name='wsdk_commands.WSDK_NotifyCAHStatus.wom_state', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='wom_cat', full_name='wsdk_commands.WSDK_NotifyCAHStatus.wom_cat', index=5,
      number=6, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=127,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='wom_sub', full_name='wsdk_commands.WSDK_NotifyCAHStatus.wom_sub', index=6,
      number=7, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=127,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='wom_err', full_name='wsdk_commands.WSDK_NotifyCAHStatus.wom_err', index=7,
      number=8, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='caha_state', full_name='wsdk_commands.WSDK_NotifyCAHStatus.caha_state', index=8,
      number=9, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='caha_cat', full_name='wsdk_commands.WSDK_NotifyCAHStatus.caha_cat', index=9,
      number=10, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='caha_sub', full_name='wsdk_commands.WSDK_NotifyCAHStatus.caha_sub', index=10,
      number=11, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='caha_err', full_name='wsdk_commands.WSDK_NotifyCAHStatus.caha_err', index=11,
      number=12, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cah_active', full_name='wsdk_commands.WSDK_NotifyCAHStatus.cah_active', index=12,
      number=13, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cah_feature_enable', full_name='wsdk_commands.WSDK_NotifyCAHStatus.cah_feature_enable', index=13,
      number=14, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cah_auth_state', full_name='wsdk_commands.WSDK_NotifyCAHStatus.cah_auth_state', index=14,
      number=15, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cah_busy', full_name='wsdk_commands.WSDK_NotifyCAHStatus.cah_busy', index=15,
      number=16, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=196,
  serialized_end=1003,
)

_WSDK_NOTIFYCAHSTATUS.fields_by_name['device_mgr_state'].enum_type = wsdkCommands_dot_WSDK__EnumDeviceMgrState__pb2._WSDK_ENUMDEVICEMGRSTATE
_WSDK_NOTIFYCAHSTATUS.fields_by_name['device_mgr_cat'].enum_type = wsdkCommands_dot_WSDK__EnumDeviceMgrState__pb2._WSDK_ENUMDEVICEMGRCAT
_WSDK_NOTIFYCAHSTATUS.fields_by_name['device_mgr_sub'].enum_type = wsdkCommands_dot_WSDK__EnumDeviceMgrState__pb2._WSDK_ENUMDEVICEMGRSUB
_WSDK_NOTIFYCAHSTATUS.fields_by_name['device_mgr_err'].enum_type = wsdkCommands_dot_WSDK__EnumDeviceMgrState__pb2._WSDK_ENUMDEVICEMGRERR
_WSDK_NOTIFYCAHSTATUS.fields_by_name['wom_state'].enum_type = wsdkCommands_dot_WSDK__EnumWOM__pb2._WSDK_ENUMWOMSTATE
_WSDK_NOTIFYCAHSTATUS.fields_by_name['wom_cat'].enum_type = wsdkCommands_dot_WSDK__EnumWOM__pb2._WSDK_ENUMWOMCAT
_WSDK_NOTIFYCAHSTATUS.fields_by_name['wom_sub'].enum_type = wsdkCommands_dot_WSDK__EnumWOM__pb2._WSDK_ENUMWOMSUB
_WSDK_NOTIFYCAHSTATUS.fields_by_name['wom_err'].enum_type = wsdkCommands_dot_WSDK__EnumWOM__pb2._WSDK_ENUMWOMERR
_WSDK_NOTIFYCAHSTATUS.fields_by_name['caha_state'].enum_type = wsdkCommands_dot_WSDK__EnumCAHA__pb2._WSDK_ENUMCAHASTATE
_WSDK_NOTIFYCAHSTATUS.fields_by_name['caha_cat'].enum_type = wsdkCommands_dot_WSDK__EnumCAHA__pb2._WSDK_ENUMCAHACAT
_WSDK_NOTIFYCAHSTATUS.fields_by_name['caha_sub'].enum_type = wsdkCommands_dot_WSDK__EnumCAHA__pb2._WSDK_ENUMCAHASUB
_WSDK_NOTIFYCAHSTATUS.fields_by_name['caha_err'].enum_type = wsdkCommands_dot_WSDK__EnumCAHA__pb2._WSDK_ENUMCAHAERR
_WSDK_NOTIFYCAHSTATUS.fields_by_name['cah_auth_state'].enum_type = wsdkCommands_dot_WSDK__EnumAuthState__pb2._WSDK_ENUMAUTHSTATE
DESCRIPTOR.message_types_by_name['WSDK_NotifyCAHStatus'] = _WSDK_NOTIFYCAHSTATUS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

WSDK_NotifyCAHStatus = _reflection.GeneratedProtocolMessageType('WSDK_NotifyCAHStatus', (_message.Message,), {
  'DESCRIPTOR' : _WSDK_NOTIFYCAHSTATUS,
  '__module__' : 'WSDK_NotifyCAHStatus_pb2'
  # @@protoc_insertion_point(class_scope:wsdk_commands.WSDK_NotifyCAHStatus)
  })
_sym_db.RegisterMessage(WSDK_NotifyCAHStatus)


# @@protoc_insertion_point(module_scope)
