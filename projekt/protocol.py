import struct, server, select
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def get_request_id(request) -> int:
    assert len(request) >= 4
    return struct.unpack(">i", request[0:4])[0]

def unpack_string(string):
    return string.split(b'\0', 1)[0].decode("utf_8")

def recv_all(conn):
    conn.setblocking(0)
    ready = select.select([conn], [], [], 1)
    if not ready[0]: return b""
    SIZE = 4096
    data = b""
    while True:
        part = conn.recv(SIZE)
        data += part
        if len(part) < SIZE: break
    return data

def send_request(connection, request, encrypt_with = None) -> (bool, bytes):
    bytes = request.pack()
    # if encrypt_with is not None:
    #     bytes = encrypt_with.encrypt(bytes, padding.PKCS1v15())
    #     print(bytes)
    connection.sendall(bytes)
    connection.setblocking(0)
    ready = select.select([connection], [], [], 1)
    if not ready[0]: return (False, b'')
    ok = connection.recv(3) == server.OK
    if ok:
        return (ok, recv_all(connection))
    else:
        return (ok, b"")

def strip_key(key: bytes) -> bytes:
    return key.split(b"END PUBLIC KEY-----\n", 1)[0]

def strip_nulls(key: bytes) -> bytes:
    return key.split(b"\0", 1)[0]

# Define endianness, and include the identifier at the beginning of each request.
PACK_START = ">i4096s"

# Decorator fo pack methods
def pack_request(fn):
    def wrapper(this):
        print(f"XXX {this.ident}")
        bytes = struct.pack(PACK_START, this.ID, this.ident)
        bytes += fn(this)
        return bytes
    return wrapper

def to_bytes(str):
    return bytes(str, "utf_8")

def stripr_nulls(bytes: bytes) -> bytes:
    while bytes[:-1] == '\0':
        bytes = bytes[:-1]
    return bytes

# A request to update the client with new messages.
class UpdateRequest:
    ID = 5
    def __init__(self, ident):
        self.ident = ident

    @pack_request
    def pack(self):
        return b""

    @staticmethod
    def unpack(bytes):
        (id, key) = struct.unpack(PACK_START + JoinRequest.PACK_PATTERN, bytes)
        return (unpack_string(channel), strip_nulls(key))

# A request to join a chat channel.
# An "/" string is the default chat channel.
# A chat channel's name can have up to 32 characters.
class JoinRequest:
    ID = 3
    PACK_PATTERN = "32s"

    def __init__(self, ident, channel: str):
        self.ident = ident
        self.channel = channel

    @pack_request
    def pack(self):
        return struct.pack(self.PACK_PATTERN, to_bytes(self.channel))

    @staticmethod
    def unpack(bytes):
        bytes = stripr_nulls(bytes)
        (id, key, channel) = struct.unpack(PACK_START + JoinRequest.PACK_PATTERN, bytes)
        return (unpack_string(channel), strip_nulls(key))

class MessageRequest:
    ID = 2
    # 1024 character limit per message, 4096 is token
    PACK_PATTERN = "1024s"

    def __init__(self, identifier: str, message: str):
        self.ident = identifier
        self.message = message

    @pack_request
    def pack(self):
        return struct.pack(self.PACK_PATTERN, bytes(self.message, "utf_8"))

    @staticmethod
    def unpack(bytes):
        bytes = stripr_nulls(bytes)
        (id, key, message) = struct.unpack(PACK_START + MessageRequest.PACK_PATTERN, bytes)
        return (unpack_string(message), strip_nulls(key))

class LoginRequest:
    ID = 1
    PACK_PATTERN = ">i64s64s4096s"

    def __init__(self, name: str, password: str, key: bytes):
        self.name = name
        self.password = password
        self.key = key

    def pack(self):
        return struct.pack(self.PACK_PATTERN, self.ID, to_bytes(self.name), to_bytes(self.password), self.key)

    @staticmethod
    def unpack(bytes):
        (id, name, password, key) = struct.unpack(LoginRequest.PACK_PATTERN, bytes)
        return (unpack_string(name), unpack_string(password), strip_key(key))

class RegisterRequest:
    ID = 11
    PACK_PATTERN = ">i64s64s"

    def __init__(self, name: str, password: str):
        self.name = name
        self.password = password

    def pack(self):
        return struct.pack(self.PACK_PATTERN, self.ID, to_bytes(self.name), to_bytes(self.password))

    @staticmethod
    def unpack(bytes):
        (id, name, password) = struct.unpack(RegisterRequest.PACK_PATTERN, bytes)
        return (unpack_string(name), unpack_string(password))

