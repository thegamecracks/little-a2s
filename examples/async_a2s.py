import asyncio

from little_a2s import AsyncA2S

host = "127.0.0.1"
port = 27015


async def main():
    a2s = AsyncA2S.from_addr(host, port)
    async with a2s, asyncio.timeout(1):
        print(await a2s.info())
        print(await a2s.players())
        print(await a2s.rules())


asyncio.run(main())
