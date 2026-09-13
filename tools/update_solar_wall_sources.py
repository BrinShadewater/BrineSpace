"""Update minified Solar Array wall registrations without reformatting geometry."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UPDATES = {
    "thermal-control-wall.json": (
        "res://assets/material-polish-v3/thermal-north.png",
        "659f8a3465ca27d9b9205cb14ea767ab78f99b04f85d7eda261f9743852c635f",
        "res://assets/solar-directional-v2/thermal-north-muted-v1.png",
        "082f7550e7383d89fdefbf0f007a4bae312c85d445593bb7adcce6e89bec85f5",
    ),
    "side-thermal-control-wall-east.json": (
        "res://assets/solar-directional-v1/thermal-sides.png",
        "52e3ce7fdc40818e7e66fcccb461cf6218fd875ad0dad2f2083509e00a0c7393",
        "res://assets/solar-directional-v2/thermal-sides-muted-v1.png",
        "18acb57dbb7dd6ca30149f18e192d455cc144c728f20b6984112bd99653df4f8",
    ),
    "side-thermal-control-wall-west.json": (
        "res://assets/solar-directional-v1/thermal-sides.png",
        "52e3ce7fdc40818e7e66fcccb461cf6218fd875ad0dad2f2083509e00a0c7393",
        "res://assets/solar-directional-v2/thermal-sides-muted-v1.png",
        "18acb57dbb7dd6ca30149f18e192d455cc144c728f20b6984112bd99653df4f8",
    ),
}


def main() -> None:
    registration_dir = ROOT / "rooms/full-wall-v1/registrations"
    for name, (old_source, old_hash, new_source, new_hash) in UPDATES.items():
        path = registration_dir / name
        data = path.read_bytes()
        old = f'"source":"{old_source}","sha256":"{old_hash}"'.encode()
        new = f'"source":"{new_source}","sha256":"{new_hash}"'.encode()
        if data.count(old) != 1:
            raise SystemExit(f"Expected one old binding in {path}, found {data.count(old)}")
        path.write_bytes(data.replace(old, new))
        print(f"PASS {name}")


if __name__ == "__main__":
    main()
