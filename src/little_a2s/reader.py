import struct
from io import BytesIO
from typing import Protocol, runtime_checkable


@runtime_checkable
class Readable(Protocol):
    def read(self, n: int = -1, /) -> bytes: ...


class Reader:
    """A simple reader for parsing serialized data."""

    def __init__(self, data: bytes | Readable) -> None:
        if not isinstance(data, Readable):
            data = BytesIO(data)

        self._file = data

    def read(self, n: int = -1, /) -> bytes:
        data = self._file.read(n)
        if n >= 0 and len(data) < n:
            raise EOFError
        return data

    def read_byte(self) -> int:
        return self.read(1)[0]

    def read_char(self) -> str:
        return self.read(1).decode("ascii")

    def read_short(self) -> int:
        return int.from_bytes(self.read(2), "little", signed=True)

    def read_ushort(self) -> int:
        return int.from_bytes(self.read(2), "little")

    def read_long(self) -> int:
        return int.from_bytes(self.read(4), "little", signed=True)

    def read_ulong(self) -> int:
        return int.from_bytes(self.read(4), "little")

    def read_float(self) -> float:
        return struct.unpack("<f", self.read(4))[0]

    def read_uint64(self) -> int:
        return int.from_bytes(self.read(8), "little")

    def read_null_string(self) -> bytes:
        return self.read_until(b"\x00")[:-1]

    def read_until(self, sep: bytes) -> bytes:
        assert len(sep) == 1
        data = bytearray()

        # FIXME: is this hot loop slow?
        while (char := self.read(1)) != sep:
            data.append(char[0])

        data.append(char[0])  # include sep itself
        return bytes(data)

    def read_varchar1(self) -> bytes:
        length = self.read_byte()
        return self.read(length)

    def read_varchar2(self) -> bytes:
        length = self.read_ushort()
        return self.read(length)

    def read_varchar4(self) -> bytes:
        length = self.read_ulong()
        return self.read(length)

    def read_varchar8(self) -> bytes:
        length = self.read_uint64()
        return self.read(length)
