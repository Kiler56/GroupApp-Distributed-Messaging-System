
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    31,
    1,
    '',
    'auth.proto'
)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nauth.proto\x12\x04\x61uth\"&\n\x15GetUserByEmailRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\"C\n\x0cUserResponse\x12\x12\n\nid_usuario\x18\x01 \x01(\x05\x12\x10\n\x08username\x18\x02 \x01(\t\x12\r\n\x05\x65mail\x18\x03 \x01(\t2P\n\x0b\x41uthService\x12\x41\n\x0eGetUserByEmail\x12\x1b.auth.GetUserByEmailRequest\x1a\x12.auth.UserResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'auth_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_GETUSERBYEMAILREQUEST']._serialized_start=20
  _globals['_GETUSERBYEMAILREQUEST']._serialized_end=58
  _globals['_USERRESPONSE']._serialized_start=60
  _globals['_USERRESPONSE']._serialized_end=127
  _globals['_AUTHSERVICE']._serialized_start=129
  _globals['_AUTHSERVICE']._serialized_end=209

