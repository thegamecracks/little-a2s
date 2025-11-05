from dataclasses import dataclass, field


@dataclass(kw_only=True)
class Packet:
    """The base class of all A2S packets."""


@dataclass(kw_only=True)
class ClientPacket(Packet):
    """An A2S packet sent by the client."""

    header: bytes
    payload: bytes
    challenge: bytes

    def __bytes__(self) -> bytes:
        return b"".join((self.header, self.payload, self.challenge))


@dataclass(kw_only=True)
class ClientPacketInfo(ClientPacket):
    """An A2S_INFO packet sent by the client."""

    header: bytes = field(default=b"\xFF\xFF\xFF\xFF\x54", init=False)
    payload: bytes = field(default=b"Source Engine Query\x00", init=False)
    challenge: bytes = field(default=b"\xFF\xFF\xFF\xFF")


@dataclass(kw_only=True)
class ClientPacketPlayers(ClientPacket):
    """An A2S_PLAYER packet sent by the client."""

    header: bytes = field(default=b"\xFF\xFF\xFF\xFF\x55", init=False)
    payload: bytes = field(default=b"", init=False)
    challenge: bytes = field(default=b"\xFF\xFF\xFF\xFF")


@dataclass(kw_only=True)
class ClientPacketRules(ClientPacket):
    """An A2S_RULES packet sent by the client."""

    header: bytes = field(default=b"\xFF\xFF\xFF\xFF\x56", init=False)
    payload: bytes = field(default=b"", init=False)
    challenge: bytes = field(default=b"\xFF\xFF\xFF\xFF")
