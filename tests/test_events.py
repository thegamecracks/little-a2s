from little_a2s.events import (
    VAC,
    ClientEventGoldsourceInfo,
    ClientEventInfo,
    Environment,
    GoldsourceMod,
    GoldsourceModDLL,
    GoldsourceModType,
    ServerType,
    Visibility,
)
from little_a2s.reader import Reader

from .constants import (
    A2S_INFO_COUNTERSTRIKE_SOURCE,
    A2S_INFO_GOLDSOURCE_COUNTERSTRIKE,
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


def test_a2s_info_goldsource() -> None:
    info = ClientEventGoldsourceInfo.from_reader(
        Reader(A2S_INFO_GOLDSOURCE_COUNTERSTRIKE[5:])
    )
    assert info == ClientEventGoldsourceInfo(
        address="77.111.194.110:27015",
        name="FR - VeryGames.net - Deatmatch - only surf_ski - ngR",
        map="surf_ski",
        folder="cstrike",
        game="Counter-Strike",
        players=12,
        max_players=18,
        protocol=47,
        type=ServerType.DEDICATED,
        environment=Environment.LINUX,
        visibility=Visibility.PUBLIC,
        mod=GoldsourceMod(
            link="www.counter-strike.net",
            download_link="",
            version=1,
            size=184000000,
            type=GoldsourceModType.SINGLE_AND_MULTIPLAYER,
            dll=GoldsourceModDLL.EXTENSION,
        ),
        vac=VAC.SECURE,
        bots=0,
    )
