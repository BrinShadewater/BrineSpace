"""Update Shield Generator registrations without reformatting geometry."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRATION_DIR = ROOT / "rooms/full-wall-v1/registrations"
UPDATES = {
    "shield-pressure-wall.json": (
        "res://assets/room-consistency-v1/shield-north.png",
        "d134a2d21691337b3cc12867ee5fd484c5bf095f85875efa1e2d7ce019d43695",
        "res://assets/rooms/shield-generator/walls/north.png",
        "cfdea5a6f239d9598489981d8cf2ff7762de8b4f4913752fc89c34129ada9542",
    ),
    "side-shield-pressure-wall-east.json": (
        "res://assets/shield-directional-v1/shield-sides-overhead.png",
        "82a4e1160f8220ad57e15ceebabe1dc2ba65b39c141f52649a039557b2db2310",
        "res://assets/rooms/shield-generator/walls/sides.png",
        "0710f3a2d0304dcf17aaef50869031317f1003a80bc93cb50b9689970fdda781",
    ),
    "side-shield-pressure-wall-west.json": (
        "res://assets/shield-directional-v1/shield-sides-overhead.png",
        "82a4e1160f8220ad57e15ceebabe1dc2ba65b39c141f52649a039557b2db2310",
        "res://assets/rooms/shield-generator/walls/sides.png",
        "0710f3a2d0304dcf17aaef50869031317f1003a80bc93cb50b9689970fdda781",
    ),
    "side-shield-pressure-wall-south.json": (
        "res://assets/room-facing-repair-v3/shield-pressure-wall-south.png",
        "4f10c0094e2b84a48c02d8aa99feef0fffb30ad219e36f1925c96c0f909f2d0b",
        "res://assets/rooms/shield-generator/walls/south.png",
        "a3276bfce9bd35e575cc95755affc7b8261437e268609839bcbc9d8068c9952c",
    ),
}


def replace_once(data: bytes, old: str, new: str, path: Path) -> bytes:
    old_bytes = old.encode()
    if data.count(old_bytes) != 1:
        raise SystemExit(f"Expected one {old!r} in {path}, found {data.count(old_bytes)}")
    return data.replace(old_bytes, new.encode())


def main() -> None:
    for name, (old_source, old_hash, new_source, new_hash) in UPDATES.items():
        path = REGISTRATION_DIR / name
        data = path.read_bytes()
        data = replace_once(data, old_source, new_source, path)
        data = replace_once(data, old_hash, new_hash, path)
        path.write_bytes(data)
        print(f"PASS {name}")


if __name__ == "__main__":
    main()
