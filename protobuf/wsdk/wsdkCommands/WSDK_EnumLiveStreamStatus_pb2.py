# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: wsdkCommands/WSDK_EnumLiveStreamStatus.proto

from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='wsdkCommands/WSDK_EnumLiveStreamStatus.proto',
  package='wsdk_commands',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=b'\n,wsdkCommands/WSDK_EnumLiveStreamStatus.proto\x12\rwsdk_commands*\xff\x01\n\x19WSDK_EnumLiveStreamStatus\x12\x1f\n\x1bWSDK_LIVE_STREAM_STATE_IDLE\x10\x00\x12!\n\x1dWSDK_LIVE_STREAM_STATE_CONFIG\x10\x01\x12 \n\x1cWSDK_LIVE_STREAM_STATE_READY\x10\x02\x12$\n WSDK_LIVE_STREAM_STATE_STREAMING\x10\x03\x12+\n\'WSDK_LIVE_STREAM_STATE_COMPLETE_STAY_ON\x10\x04\x12)\n%WSDK_LIVE_STREAM_STATE_FAILED_STAY_ON\x10\x05'
)

_WSDK_ENUMLIVESTREAMSTATUS = _descriptor.EnumDescriptor(
  name='WSDK_EnumLiveStreamStatus',
  full_name='wsdk_commands.WSDK_EnumLiveStreamStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='WSDK_LIVE_STREAM_STATE_IDLE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WSDK_LIVE_STREAM_STATE_CONFIG', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WSDK_LIVE_STREAM_STATE_READY', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WSDK_LIVE_STREAM_STATE_STREAMING', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WSDK_LIVE_STREAM_STATE_COMPLETE_STAY_ON', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WSDK_LIVE_STREAM_STATE_FAILED_STAY_ON', index=5, number=5,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=64,
  serialized_end=319,
)
_sym_db.RegisterEnumDescriptor(_WSDK_ENUMLIVESTREAMSTATUS)

WSDK_EnumLiveStreamStatus = enum_type_wrapper.EnumTypeWrapper(_WSDK_ENUMLIVESTREAMSTATUS)
WSDK_LIVE_STREAM_STATE_IDLE = 0
WSDK_LIVE_STREAM_STATE_CONFIG = 1
WSDK_LIVE_STREAM_STATE_READY = 2
WSDK_LIVE_STREAM_STATE_STREAMING = 3
WSDK_LIVE_STREAM_STATE_COMPLETE_STAY_ON = 4
WSDK_LIVE_STREAM_STATE_FAILED_STAY_ON = 5


DESCRIPTOR.enum_types_by_name['WSDK_EnumLiveStreamStatus'] = _WSDK_ENUMLIVESTREAMSTATUS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


# @@protoc_insertion_point(module_scope)
