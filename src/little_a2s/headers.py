# https://developer.valvesoftware.com/wiki/Server_queries
from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum


class HeaderType(IntEnum):
    SIMPLE = -1
    MULTI = -2


@dataclass(kw_only=True)
class Header:
    """An A2S response header."""

    type: HeaderType


@dataclass(kw_only=True)
class MultiGoldsourceHeader(Header):
    """A multi-packet response header for Goldsource games."""

    type: HeaderType = field(default=HeaderType.SIMPLE)
    id: int
    current: int
    total: int


@dataclass(kw_only=True)
class MultiSourceHeader(Header):
    """A multi-packet response header for Source games."""

    type: HeaderType = field(default=HeaderType.SIMPLE)
    id: int
    current: int
    total: int
    size: int  # Some games omit this field!
    compressed: CompressionHeader | None


@dataclass(kw_only=True)
class CompressionHeader:
    """The compression header for Source games. Mostly present in ~2006-era engines."""

    size: int
    checksum: int
