from little_a2s.client import A2SClientProtocol

from little_a2s.events import (
    ClientEventChallenge,
    ClientEventGoldsourceInfo,
    ClientEventInfo,
    ClientEventPlayers,
)
from tests.constants import (
    A2S_INFO_COUNTERSTRIKE_SOURCE,
    A2S_INFO_GOLDSOURCE_COUNTERSTRIKE,
    A2S_INFO_SIN1_MP,
    A2S_PLAYER,
    S2C_CHALLENGE,
)


def test_single_packets() -> None:
    source = A2SClientProtocol()
    source.receive_datagram(S2C_CHALLENGE)
    source.receive_datagram(A2S_INFO_COUNTERSTRIKE_SOURCE)
    source.receive_datagram(A2S_INFO_GOLDSOURCE_COUNTERSTRIKE)
    source.receive_datagram(A2S_INFO_SIN1_MP)
    source.receive_datagram(A2S_PLAYER)

    events = source.events_received()
    assert isinstance(events[0], ClientEventChallenge)
    assert isinstance(events[1], ClientEventInfo)
    assert isinstance(events[2], ClientEventGoldsourceInfo)
    assert isinstance(events[3], ClientEventInfo)
    assert isinstance(events[4], ClientEventPlayers)
    assert len(events) == 5

    assert source.events_received() == []
    assert source.packets_to_send() == []
