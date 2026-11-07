"""Update selected Current Turbine registrations without reformatting geometry."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRATION_DIR = ROOT / "rooms/full-wall-v1/registrations"
UPDATES = {
    "side-current-turbine-east.json": (
        "res://assets/turbine-directional-v3/east-overhead-clean.png",
        "5ed59db9d4a18621fe10392ef37748284c29674b7383146ee41c4531bbc5f161",
        "res://assets/turbine-directional-v4/turbine-sides-muted-v1.png",
        "7eae3f817c6971b8f1324e0423581bebf06aaa503ff9c23300ac4aeba72bd9de",
    ),
    "side-current-turbine-west.json": (
        "res://assets/turbine-directional-v3/east-overhead-clean.png",
        "5ed59db9d4a18621fe10392ef37748284c29674b7383146ee41c4531bbc5f161",
        "res://assets/turbine-directional-v4/turbine-sides-muted-v1.png",
        "7eae3f817c6971b8f1324e0423581bebf06aaa503ff9c23300ac4aeba72bd9de",
    ),
    "side-current-turbine-south.json": (
        "res://assets/turbine-directional-v1/turbine-south.png",
        "12354d2e79c55cb3ea67b072e0941eecf66cd543c12009918c96d260b569bdaf",
        "res://assets/turbine-directional-v4/turbine-south-muted-v1.png",
        "8cca000bd7d55fae9e7ab7d4861ea1428d4717dccc6313017c1a9acea0f8a568",
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
