"""Update Battery Array registrations without reformatting polygon geometry."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRATION_DIR = ROOT / "rooms/full-wall-v1/registrations"
FAMILIES = {
    "north": {
        "files": ["battery-wall-north-cells.json", "battery-wall-north-distribution.json"],
        "old_source": "res://assets/rooms/battery-array/walls/split-north.png",
        "old_hash": "006f79ee2d146caeb65efb0043608324eebf9feaaea32534fdc40bfacb60062c",
        "new_source": "res://assets/battery-directional-v2/battery-north-muted-v1.png",
        "new_hash": "ead96d044219885bafe9e88de91fe9d7fd996a2acdfd0bb4cfe24311555ac7d9",
    },
    "sides": {
        "files": [
            "battery-wall-east-cells.json",
            "battery-wall-east-distribution.json",
            "battery-wall-west-cells.json",
            "battery-wall-west-distribution.json",
        ],
        "old_source": "res://assets/battery-directional-v1/side-overhead.png",
        "old_hash": "aee5d67a4c1bfdef17dbc4cf2dd5c1242898f929d2497c9c1645588e74343023",
        "new_source": "res://assets/rooms/battery-array/walls/sides.png",
        "new_hash": "e1efe39a9f2bf35dd29bef9f18424b570f7186f968f15e8a59c7f8a7a3ea3696",
    },
    "south": {
        "files": ["battery-wall-south-cells.json", "battery-wall-south-distribution.json"],
        "old_source": "res://assets/battery-directional-v1/battery-south.png",
        "old_hash": "935b8b70e5b23963afa70af596527781fcb29ca5c4e4bde57d2aad9f962bde25",
        "new_source": "res://assets/rooms/battery-array/walls/south.png",
        "new_hash": "693cbf8cafe801ee921ca2d89e1a282776efb54f450c8f73f3fd95d267f88bb4",
    },
}


def replace_once(data: bytes, old: str, new: str, path: Path) -> bytes:
    old_bytes = old.encode()
    if data.count(old_bytes) != 1:
        raise SystemExit(f"Expected one {old!r} in {path}, found {data.count(old_bytes)}")
    return data.replace(old_bytes, new.encode())


def main() -> None:
    for family in FAMILIES.values():
        for name in family["files"]:
            path = REGISTRATION_DIR / name
            data = path.read_bytes()
            data = replace_once(data, family["old_source"], family["new_source"], path)
            data = replace_once(data, family["old_hash"], family["new_hash"], path)
            path.write_bytes(data)
            print(f"PASS {name}")


if __name__ == "__main__":
    main()
