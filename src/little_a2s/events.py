from dataclasses import dataclass
from enum import IntEnum


# ClientEventInfo types
class ServerType(IntEnum):
    DEDICATED = ord("d")
    LISTEN = ord("l")
    RELAY = ord("p")


class Environment(IntEnum):
    LINUX = ord("l")
    WINDOWS = ord("w")
    MACOS_M = ord("m")  # Ergh, can this be combined?
    MACOS_O = ord("o")


class Visibility(IntEnum):
    PUBLIC = 0
    PRIVATE = 1


class VAC(IntEnum):
    INSECURE = 0
    SECURE = 1


@dataclass(kw_only=True)
class ExtraInfo:
    """Extra data included with an A2S_INFO response."""

    port: int | None = None
    steam_id: int | None = None
    spectator_port: int | None = None
    spectator_name: str
    keywords: str
    game_id: int


# ClientEventGoldsourceInfo types
class GoldsourceServerType(IntEnum):
    DEDICATED = ord("D")
    LISTEN = ord("L")
    RELAY = ord("P")


class GoldsourceEnvironment(IntEnum):
    LINUX = ord("L")
    WINDOWS = ord("W")


class GoldsourceModType(IntEnum):
    SINGLE_AND_MULTIPLAYER = 0
    MULTIPLAYER_ONLY = 1


class GoldsourceModDLL(IntEnum):
    NATIVE = 0
    """This mod uses the Half-Life DLL."""

    EXTENSION = 1
    """This mod provides its own DLL."""


@dataclass(kw_only=True)
class GoldsourceMod:
    """Extra data included with an A2S_INFO response."""

    link: str
    download_link: str
    version: int
    size: int
    type: GoldsourceModType
    dll: GoldsourceModDLL


# ClientEventPlayer types
@dataclass
class Player:
    """A player returned in the A2S_PLAYER response."""

    index: int
    name: str
    score: int
    duration: float


# Event types
@dataclass(kw_only=True)
class Event:
    """The base class for all A2S protocol events."""


@dataclass(kw_only=True)
class ClientEvent(Event):
    """An A2S client protocol event."""


@dataclass(kw_only=True)
class ClientEventInfo(ClientEvent):
    """An A2S_INFO client protocol event.

    This follows the Source format. For the Goldsource equivalent,
    see :class:`ClientEventGoldsourceInfo`.

    """

    protocol: int
    name: str
    map: str
    folder: str
    game: str
    id: int
    players: int
    max_players: int
    bots: int
    type: ServerType
    environment: Environment
    visibility: Visibility
    vac: VAC
    version: str
    extra: ExtraInfo | None


@dataclass(kw_only=True)
class ClientEventGoldsourceInfo(ClientEvent):
    """An A2S_INFO Goldsource client protocol event."""

    address: str
    name: str
    map: str
    folder: str
    game: str
    players: int
    max_players: int
    protocol: int
    type: GoldsourceServerType
    environment: GoldsourceEnvironment
    visibility: Visibility
    mod: GoldsourceMod | None
    vac: VAC
    bots: int


@dataclass(kw_only=True)
class ClientEventPlayers(ClientEvent):
    """An A2S_PLAYER client protocol event."""

    players: list[Player]


@dataclass(kw_only=True)
class ClientEventRules(ClientEvent):
    """An A2S_RULES client protocol event."""

    # While documented to be strings, some games might provide binary data
    # *cough Arma* which may not decode correctly as UTF-8.
    rules: dict[bytes, bytes]

    def decode(self) -> dict[str, str]:
        """Return all rules decoded in UTF-8."""
        return {k.decode(): v.decode() for k, v in self.rules.items()}


@dataclass(kw_only=True)
class ClientEventChallenge(ClientEvent):
    """An S2C_CHALLENGE client protocol event."""
