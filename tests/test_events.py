from little_a2s.events import (
    VAC,
    ClientEventChallenge,
    ClientEventGoldsourceInfo,
    ClientEventInfo,
    ClientEventPlayers,
    ClientEventRules,
    Environment,
    ExtraInfo,
    GoldsourceMod,
    GoldsourceModDLL,
    GoldsourceModType,
    Player,
    ServerType,
    Visibility,
)
from little_a2s.reader import Reader

from tests.constants import (
    A2S_INFO_COUNTERSTRIKE_SOURCE,
    A2S_INFO_GOLDSOURCE_COUNTERSTRIKE,
    A2S_INFO_PROJECT_ZOMBOID,
    A2S_INFO_SIN1_MP,
    A2S_PLAYER,
    A2S_RULES_PROJECT_ZOMBOID,
    S2C_CHALLENGE,
)


def test_a2s_info_counterstrike_source() -> None:
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


def test_a2s_info_sin1_mp() -> None:
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


def test_a2s_info_project_zomboid() -> None:
    info = ClientEventInfo.from_reader(Reader(A2S_INFO_PROJECT_ZOMBOID[5:]))
    assert info == ClientEventInfo(
        protocol=17,
        name="play.thegamecracks.xyz",
        map="Muldraugh, KY",
        folder="zomboid",
        game="Project Zomboid",
        id=0,
        players=0,
        max_players=8,
        bots=0,
        type=ServerType.DEDICATED,
        environment=Environment.LINUX,
        visibility=Visibility.PRIVATE,
        vac=VAC.SECURE,
        version="1.0.0.0",
        extra=ExtraInfo(
            port=16261,
            steam_id=90276363418906655,
            spectator_port=None,
            spectator_name=None,
            keywords="",
            game_id=108600,
        ),
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


def test_a2s_player() -> None:
    players = ClientEventPlayers.from_reader(Reader(A2S_PLAYER[5:]))
    assert players == ClientEventPlayers(
        players=[
            Player(
                index=1,
                name="[D]---->T.N.W<----",
                score=14,
                duration=514.370361328125,
            ),
            Player(
                index=2,
                name="Killer !!!",
                score=5,
                duration=434.2844543457031,
            ),
        ]
    )


def test_a2s_rules_project_zomboid() -> None:
    rules = ClientEventRules.from_reader(Reader(A2S_RULES_PROJECT_ZOMBOID[5:]))
    assert rules == ClientEventRules(
        rules={
            b"": b"modCount",
            b"304": b"mods",
            b"CasterPlus;TombBodyCompat;TombBody;TombBodyCustom;TombBodyTex;TombBodyTexDOLL;TombBodyTexNUDE;velkiel_fixed_cooking_recipes": b"open",
            b"0": b"public",
            b"1": b"version",
        }
    )


def test_s2c_challenge() -> None:
    challenge = ClientEventChallenge.from_reader(Reader(S2C_CHALLENGE[5:]))
    assert challenge == ClientEventChallenge(challenge=584425803)
