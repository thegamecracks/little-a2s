"""A convenience script to convert example responses from Valve's documentation.

https://developer.valvesoftware.com/wiki/Server_queries

: FF FF FF FF 49 2F 53 65 6E 73 65 6D 61 6E 6E 20    ÿÿÿÿI/Sensemann
: 53 69 4E 20 44 4D 00 70 61 72 61 64 6F 78 00 53    SiN DM.paradox.S
: 69 4E 20 31 00 53 69 4E 20 31 00 1D 05 00 10 00    iN 1.SiN 1......
: 6C 77 00 00 31 2E 30 2E 30 2E 30 00                lw..1.0.0.0.
:
b"\xff\xff\xff\xff\x49\x2f\x53\x65\x6e\x73\x65\x6d\x61\x6e\x6e\x20\x53\x69"
b"\x4e\x20\x44\x4d\x00\x70\x61\x72\x61\x64\x6f\x78\x00\x53\x69\x4e\x20\x31"
b"\x00\x53\x69\x4e\x20\x31\x00\x1d\x05\x00\x10\x00\x6c\x77\x00\x00\x31\x2e"
b"\x30\x2e\x30\x2e\x30\x00"

"""


def main() -> None:
    lines = []
    while True:
        line = input(": ")
        if line:
            lines.append(line)
        elif lines:
            print(format_data(lines))
            lines.clear()
        else:
            break


def format_data(lines: list[str]) -> str:
    data = []
    for line in lines:
        line, _, _ = line.partition("  ")
        data.extend(rf"\x{c.lower()}" for c in line.split())

    chunks = [data[i : i + 18] for i in range(0, len(data), 18)]
    chunks = [f'b"{"".join(c)}"' for c in chunks]
    return "\n".join(chunks)


if __name__ == "__main__":
    main()
