# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: wsdkCommands/WSDK_EnumLiveStreamError.proto

from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='wsdkCommands/WSDK_EnumLiveStreamError.proto',
  package='wsdk_commands',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=b'\n+wsdkCommands/WSDK_EnumLiveStreamError.proto\x12\rwsdk_commands*\xf9\x03\n\x18WSDK_EnumLiveStreamError\x12\x1f\n\x1bWSDK_LIVE_STREAM_ERROR_NONE\x10\x00\x12\"\n\x1eWSDK_LIVE_STREAM_ERROR_NETWORK\x10\x01\x12\'\n#WSDK_LIVE_STREAM_ERROR_CREATESTREAM\x10\x02\x12&\n\"WSDK_LIVE_STREAM_ERROR_OUTOFMEMORY\x10\x03\x12&\n\"WSDK_LIVE_STREAM_ERROR_INPUTSTREAM\x10\x04\x12#\n\x1fWSDK_LIVE_STREAM_ERROR_INTERNET\x10\x05\x12$\n WSDK_LIVE_STREAM_ERROR_OSNETWORK\x10\x06\x12\x31\n-WSDK_LIVE_STREAM_ERROR_SELECTEDNETWORKTIMEOUT\x10\x07\x12(\n$WSDK_LIVE_STREAM_ERROR_SSL_HANDSHAKE\x10\x08\x12\"\n\x1eWSDK_LIVE_STREAM_ERROR_UNKNOWN\x10\t\x12\'\n#WSDK_LIVE_STREAM_ERROR_SD_CARD_FULL\x10(\x12*\n&WSDK_LIVE_STREAM_ERROR_SD_CARD_REMOVED\x10)'
)

_WSDK_ENUMLIVESTREAMERROR = _descriptor.EnumDescriptor(
  name='WSDK_EnumLiveStreamError',
  full_name='wsdk_commands.WSDK_EnumLiveStreamError',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='WSDK_LIVE_STREAM_ERROR_NONE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WSDK_LIVE_STREAM_ERROR_NETWORK', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WSDK_LIVE_STREAM_ERROR_CREATESTREAM', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WSDK_LIVE_STREAM_ERROR_OUTOFMEMORY', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WSDK_LIVE_STREAM_ERROR_INPUTSTREAM', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WSDK_LIVE_STREAM_ERROR_INTERNET', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WSDK_LIVE_STREAM_ERROR_OSNETWORK', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WSDK_LIVE_STREAM_ERROR_SELECTEDNETWORKTIMEOUT', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WSDK_LIVE_STREAM_ERROR_SSL_HANDSHAKE', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WSDK_LIVE_STREAM_ERROR_UNKNOWN', index=9, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WSDK_LIVE_STREAM_ERROR_SD_CARD_FULL', index=10, number=40,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WSDK_LIVE_STREAM_ERROR_SD_CARD_REMOVED', index=11, number=41,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=63,
  serialized_end=568,
)
_sym_db.RegisterEnumDescriptor(_WSDK_ENUMLIVESTREAMERROR)

WSDK_EnumLiveStreamError = enum_type_wrapper.EnumTypeWrapper(_WSDK_ENUMLIVESTREAMERROR)
WSDK_LIVE_STREAM_ERROR_NONE = 0
WSDK_LIVE_STREAM_ERROR_NETWORK = 1
WSDK_LIVE_STREAM_ERROR_CREATESTREAM = 2
WSDK_LIVE_STREAM_ERROR_OUTOFMEMORY = 3
WSDK_LIVE_STREAM_ERROR_INPUTSTREAM = 4
WSDK_LIVE_STREAM_ERROR_INTERNET = 5
WSDK_LIVE_STREAM_ERROR_OSNETWORK = 6
WSDK_LIVE_STREAM_ERROR_SELECTEDNETWORKTIMEOUT = 7
WSDK_LIVE_STREAM_ERROR_SSL_HANDSHAKE = 8
WSDK_LIVE_STREAM_ERROR_UNKNOWN = 9
WSDK_LIVE_STREAM_ERROR_SD_CARD_FULL = 40
WSDK_LIVE_STREAM_ERROR_SD_CARD_REMOVED = 41


DESCRIPTOR.enum_types_by_name['WSDK_EnumLiveStreamError'] = _WSDK_ENUMLIVESTREAMERROR
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


# @@protoc_insertion_point(module_scope)
