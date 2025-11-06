# https://community.bistudio.com/wiki/Arma_3:_ServerBrowserProtocol3
from __future__ import annotations

from dataclasses import dataclass
from enum import IntFlag
from typing import Self

from little_a2s.events import ClientEventRules
from little_a2s.reader import Reader


@dataclass(kw_only=True)
class Arma3Rules:
    version: int
    overflow: int
    dlc: Arma3DLC
    difficulty: Arma3Difficulty
    dlc_hashes: list[int]
    mods: list[Arma3Mod]
    signatures: list[str]

    @classmethod
    def from_rules(cls, rules: dict[bytes, bytes] | ClientEventRules) -> Self:
        if isinstance(rules, ClientEventRules):
            rules = rules.rules

        data = cls._assemble_rules(rules)
        data = cls._translate_escapes(data)
        reader = Reader(data)

        version = reader.read_byte()
        overflow = reader.read_byte()
        dlc = Arma3DLC(reader.read_ushort())
        difficulty = Arma3Difficulty.from_int(reader.read_ushort())
        dlc_hashes = [reader.read_ulong() for _ in range(dlc.bit_count())]

        n_mods = reader.read_byte()
        mods = [Arma3Mod.from_reader(reader) for _ in range(n_mods)]

        n_signatures = reader.read_byte()
        signatures = [reader.read_varchar1().decode() for _ in range(n_signatures)]

        return cls(
            version=version,
            overflow=overflow,
            dlc=dlc,
            difficulty=difficulty,
            dlc_hashes=dlc_hashes,
            mods=mods,
            signatures=signatures,
        )

    @staticmethod
    def _assemble_rules(rules: dict[bytes, bytes]) -> bytes:
        # Real Virtuality stores the payload in chunks of 125 bytes,
        # ordered and enumerated.
        data = bytearray()

        last_current = None
        last_total = None

        for k, v in rules.items():
            if len(k) != 2:
                continue

            current, total = k
            if last_total is not None and total != last_total:
                # This could be a legitimate two character key
                raise ValueError(f"Expected total {last_total}, got {total}")
            if last_current is not None and current != last_current + 1:
                raise ValueError(f"Expected index {last_current + 1}, got {current}")
            last_current, last_total = current, total

            data.extend(v)

            # We're making an assumption that the rules are encoded in order,
            # so last key should end with the same index.
            if current == total:
                break

        return bytes(data)

    @staticmethod
    def _translate_escapes(data: bytes) -> bytes:
        # FIXME: does this need to be optimized?
        data = data.replace(b"\x01\x03", b"\xff")
        data = data.replace(b"\x01\x02", b"\x00")
        data = data.replace(b"\x01\x01", b"\x01")
        return data


class Arma3DLC(IntFlag):
    KART = 0x1
    MARKSMEN = 0x2
    HELI = 0x4
    CURATOR = 0x8
    EXPANSION = 0x10
    JETS = 0x20
    ORANGE = 0x40  # Laws of War
    ARGO = 0x80
    TACOPS = 0x100
    TANKS = 0x200
    CONTACT = 0x400  # Contact platform
    ENOCH = 0x800  # Contact DLC


@dataclass(kw_only=True)
class Arma3Difficulty:
    difficulty: int
    skill: int
    advanced_flight_model: bool
    third_person_view: bool
    weapon_crosshair: bool

    @classmethod
    def from_int(cls, n: int) -> Self:
        assert 0 <= n < 0xFFFF
        return cls(
            difficulty=n & 0b111,
            skill=n >> 3 & 0b111,
            advanced_flight_model=bool(n >> 6 & 0b1),
            third_person_view=bool(n >> 7 & 0b1),
            weapon_crosshair=bool(n >> 8 & 0b1),
        )


@dataclass(kw_only=True)
class Arma3Mod:
    hash: int
    dlc: bool
    steam_id: int
    name: str

    @classmethod
    def from_reader(cls, reader: Reader) -> Self:
        hash = reader.read_ulong()

        length = reader.read_byte()
        dlc = bool(length >> 4 & 1)
        length = length & 0x0F
        steam_id = int.from_bytes(reader.read(length), "little")
        name = reader.read_varchar1().decode()

        return cls(
            hash=hash,
            dlc=dlc,
            steam_id=steam_id,
            name=name,
        )
