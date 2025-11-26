"""This uses the Sans-IO protocol to implement an asyncio A2S query client.

Example output (see host and port):
    Sent packet: ClientPacketInfo
    Parsed event: ClientEventChallenge
    Sent packet: ClientPacketInfo
    Parsed event: ClientEventInfo
    Sent packet: ClientPacketPlayers
    Parsed event: ClientEventPlayers
    Sent packet: ClientPacketRules
    Parsed event: ClientEventRules
    ClientEventInfo(protocol=17, name="The Northmen's Deer Isle | US | Vanilla+", ...)
    ClientEventPlayers(players=[Player(index=0, name='', score=0, duration=1948.5), ...])
    ClientEventRules(rules={b'allowedBuild': b'0', b'clientPort': b'0', ...})
"""

import asyncio
from typing import Callable

from little_a2s import (
    # This is the class that handles parsing datagrams into events.
    A2SClientProtocol,
    # The classes below are some return values of the protocol.
    ClientEvent,
    ClientEventChallenge,
    ClientEventInfo,
    ClientEventPlayers,
    ClientEventRules,
    ClientPacket,
    PayloadError,
)

host = "127.0.0.1"
port = 27015


async def main():
    loop = asyncio.get_running_loop()

    transport, protocol = await loop.create_datagram_endpoint(
        MyA2SProtocol,
        remote_addr=(host, port),
    )

    async with protocol, asyncio.timeout(1):
        info = await protocol.info()
        players = await protocol.players()
        rules = await protocol.rules()

    print(info)
    print(players)
    print(rules)


class MyA2SProtocol(asyncio.DatagramProtocol):
    _send_fut: asyncio.Future[list[ClientEvent]] | None

    def __init__(self):
        self._proto = A2SClientProtocol()

        # For this example, we won't try to support concurrent usage,
        # so we're lock sending and receiving to one task at a time.
        self._send_lock = asyncio.Lock()
        self._send_fut = None

        # A future to help us wait for the protocol's closure.
        self._close_fut = asyncio.get_running_loop().create_future()

    # Datagram protocol methods

    def connection_made(self, transport: asyncio.DatagramTransport):
        self.transport = transport

    def connection_lost(self, exc: Exception | None):
        if exc is None:
            self._close_fut.set_result(None)
        else:
            self._close_fut.set_exception(exc)

    def datagram_received(self, data: bytes, addr):
        # Whenever we receive a datagram, feed it to the Sans-IO protocol.
        # This may fail if the datagram is corrupted, so consider logging it
        # or sending the exception to the caller.
        try:
            self._proto.receive_datagram(data)
        except PayloadError as e:
            if self._send_fut is not None:
                self._send_fut.set_exception(e)

        # The protocol may tell us to send packets in response.
        for packet in self._proto.packets_to_send():
            self.transport.sendto(bytes(packet))

        # After parsing the datagram, we may receive events resulting from it.
        # It can take several datagrams in the case of multi-packet responses.
        events = self._proto.events_received()
        if not events or self._send_fut is None:
            return

        print(f"Parsed event: {type(events[0]).__name__}")
        try:
            self._send_fut.set_result(events)
        except asyncio.InvalidStateError:
            pass  # Future was probably cancelled

    # Bridge methods
    # This is how we convert our low-level, callback-based transport
    # to high-level async/await syntax.

    async def _send(self, packet: ClientPacket) -> list[ClientEvent]:
        # If we send multiple packets at once, we may receive events
        # out-of-order. For simplicitly, we'll lock send / read entirely.
        async with self._send_lock:
            self.transport.sendto(bytes(packet))
            print(f"Sent packet: {type(packet).__name__}")

            fut = asyncio.get_running_loop().create_future()
            self._send_fut = fut
            return await fut

    # Request methods

    async def info(self) -> ClientEventInfo:
        event = await self._send_or_challenge(self._proto.info)
        assert isinstance(event, ClientEventInfo)  # can be false if out-of-order
        return event

    async def players(self) -> ClientEventPlayers:
        event = await self._send_or_challenge(self._proto.players)
        assert isinstance(event, ClientEventPlayers)  # can be false if out-of-order
        return event

    async def rules(self) -> ClientEventRules:
        event = await self._send_or_challenge(self._proto.rules)
        assert isinstance(event, ClientEventRules)  # can be false if out-of-order
        return event

    async def _send_or_challenge(
        self,
        request: Callable[[], ClientPacket],
    ) -> ClientEvent:
        events = await self._send(request())

        # Since we have one sender at a time, we shouldn't receive
        # more than one event per request.
        assert len(events) == 1

        # If we receive a challenge, regenerate the request so the
        # A2S protocol can suffix the challenge to the new payload.
        #
        # Just in case, we'll set a limit so we don't spam traffic.

        remaining = 3
        while remaining > 0 and isinstance(events[0], ClientEventChallenge):
            events = await self._send(request())
            assert len(events) == 1
            remaining -= 1

        return events[0]

    # Cleanup methods

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, tb):
        await self.close()

    async def close(self):
        self.transport.close()
        return await asyncio.shield(self._close_fut)


if __name__ == "__main__":
    asyncio.run(main())
