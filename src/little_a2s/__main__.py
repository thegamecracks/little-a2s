"""Query a server at the given host and port.

Examples:
    python -m little_a2s 127.0.0.1:27015
    python -m little_a2s ::1:27015
    python -m little_a2s example.com:27015

"""

import argparse
import datetime
import json
import logging
from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import assert_never

from little_a2s import (
    A2S,
    A2SGoldsource,
    ClientEventGoldsourceInfo,
    ClientEventInfo,
    ClientEventPlayers,
    ClientEventRules,
    Error,
)
from little_a2s.client.constants import DEFAULT_TIMEOUT

Address = tuple[str, int]

log = logging.getLogger(__name__)


def main() -> None:
    formats = [e.value for e in OutputFormat]
    formats_str = ", ".join(formats)
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-f",
        "--format",
        default="text",
        choices=formats,
        help=f"The output format to use ({formats_str}) (default: %(default)s)",
        type=OutputFormat,
    )
    # FIXME: this flag will become obsolete once A2SGoldsource is merged into A2S
    parser.add_argument(
        "--goldsource",
        action="store_true",
        help="[EXPERIMENTAL] Parse Goldsource A2S_INFO responses instead of Source",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        default=DEFAULT_TIMEOUT,
        help="The timeout between responses (default: %(default)s)",
        type=float,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase logging verbosity",
    )
    parser.add_argument(
        "addr",
        help="The query host and port in format host:port (IPv4, IPv6, DNS name)",
        type=parse_address,
    )

    args = parser.parse_args()
    addr: Address = args.addr
    format: OutputFormat = args.format
    goldsource: bool = args.goldsource
    timeout: float = args.timeout
    verbose: int = args.verbose

    setup_logging(verbose=verbose)

    try:
        results = query_addr(addr, goldsource=goldsource, timeout=timeout)
    except (Error, TimeoutError) as e:
        return log.error("Failed to query server: %s", e)

    print_query_results(results, format=format)


class OutputFormat(StrEnum):
    JSON = "json"
    NONE = "none"
    TEXT = "text"


def parse_address(addr: str) -> Address:
    host, _, port = addr.rpartition(":")
    # host = ip_address(host)  # IPv4 / IPv6 / DNS name validation?
    port = int(port)
    return host, port


def setup_logging(*, verbose: int) -> None:
    if verbose > 1:
        format = "%(levelname)-7s: %(name)-30s: %(message)s"
        root_level = logging.DEBUG
    elif verbose > 0:
        format = "%(levelname)s: %(message)s"
        root_level = logging.INFO
    else:
        format = "%(levelname)s: %(message)s"
        root_level = logging.WARNING

    logging.basicConfig(format=format, level=root_level)


@dataclass(kw_only=True)
class QueryResults:
    info: ClientEventInfo | ClientEventGoldsourceInfo
    players: ClientEventPlayers
    rules: ClientEventRules


def query_addr(addr: Address, *, goldsource: bool, timeout: float) -> QueryResults:
    host, port = addr
    host = str(host)

    if goldsource:
        with A2SGoldsource.from_addr(host, port, timeout=timeout) as a2s:
            log.info("Querying A2S_INFO...")
            info = a2s.info()
            log.info("Querying A2S_PLAYERS...")
            players = a2s.players()
            log.info("Querying A2S_RULES...")
            rules = a2s.rules()
    else:
        with A2S.from_addr(host, port, timeout=timeout) as a2s:
            log.info("Querying A2S_INFO...")
            info = a2s.info()
            log.info("Querying A2S_PLAYERS...")
            players = a2s.players()
            log.info("Querying A2S_RULES...")
            rules = a2s.rules()

    return QueryResults(info=info, players=players, rules=rules)


def print_query_results(results: QueryResults, *, format: OutputFormat) -> None:
    if format == OutputFormat.JSON:
        info = asdict(results.info)
        players = results.players.players
        try:
            rules = results.rules.decode()
        except UnicodeDecodeError:
            rules = {
                stringify_bytes(k): stringify_bytes(v) for k, v in results.rules.items()
            }

        data = {"info": info, "players": players, "rules": rules}
        print(json.dumps(data, indent=4))
    elif format == OutputFormat.NONE:
        pass  # useful for checking that a server is online without output
    elif format == OutputFormat.TEXT:
        print("A2S_INFO:")
        info = asdict(results.info)
        for k, v in info.items():
            print(f"  {k} = {v}")

        print()
        print("A2S_PLAYER:")
        for i, player in enumerate(results.players, start=1):
            duration = datetime.timedelta(seconds=int(player.duration))
            print(
                f"  {i: 3d}. {player.name!r:32s} (score: {player.score}, duration: {duration})"
            )

        print()
        print("A2S_RULES:")
        try:
            for k, v in results.rules.decode().items():
                v = truncate_rule_value(v)
                print(f"  {k}: {v}")
        except UnicodeDecodeError:
            for k, v in results.rules.items():
                v = truncate_rule_value(v)
                print(f"  {k}: {v}")
    else:
        assert_never(format)


def stringify_bytes(b: bytes) -> str:
    return "".join(c if (c := chr(n)).isprintable() else f"\\x{n:02x}" for n in b)


def truncate_rule_value(v: bytes | str) -> str:
    length = 80
    v = str(v)
    return v if len(v) <= length else str(v[:length]) + " [...]"


if __name__ == "__main__":
    main()
