from little_a2s import A2S

host = "127.0.0.1"
port = 27015

with A2S.from_addr(host, port, timeout=1) as a2s:
    print(a2s.info())
    print(a2s.players())
    print(a2s.rules())
