from little_a2s.events import VAC, ClientEventInfo, Environment, ServerType, Visibility
from little_a2s.reader import Reader

from .constants import (
    A2S_INFO_COUNTERSTRIKE_SOURCE,
    A2S_INFO_SIN1_MP,
)


def test_a2s_info() -> None:
    info = ClientEventInfo.from_reader(Reader(A2S_INFO_COUNTERSTRIKE_SOURCE[5:]))
    assert info == ClientEventInfo(
        protocol=2,
        name="game2xs.com Counter-Strike Source #1",
        map="de_dust",
        folder="cstrike",
        game="Counter-Strike: Source",
        id=240,
        players=5,
        max_players=16,
        bots=4,
        type=ServerType.DEDICATED,
        environment=Environment.LINUX,
        visibility=Visibility.PUBLIC,
        vac=VAC.INSECURE,
        version="1.0.0.22",
        extra=None,
    )

    info = ClientEventInfo.from_reader(Reader(A2S_INFO_SIN1_MP[5:]))
    assert info == ClientEventInfo(
        protocol=47,
        name="Sensemann SiN DM",
        map="paradox",
        folder="SiN 1",
        game="SiN 1",
        id=1309,
        players=0,
        max_players=16,
        bots=0,
        type=ServerType.LISTEN,
        environment=Environment.WINDOWS,
        visibility=Visibility.PUBLIC,
        vac=VAC.INSECURE,
        version="1.0.0.0",
        extra=None,
    )
