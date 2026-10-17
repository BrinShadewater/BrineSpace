"""Package Bill's reviewed side helmets and north/south helmet studies."""

import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BARE = ROOT / "crew-runtime-matte-v1" / "bill"
SIDES = ROOT / "bill-shared-helmet-sides-runtime-v1"
SOUTH = ROOT / "bill-shared-helmet-south-v1"
NORTH = ROOT / "bill-shared-helmet-north-v1"
SOURCES = {
    "walk-east": SIDES,
    "idle-east": SIDES,
    "walk-west": SIDES,
    "idle-west": SIDES,
    "walk-south": SOUTH,
    "idle-south": SOUTH,
    "walk-north": NORTH,
    "idle-north": NORTH,
}


def main() -> None:
    bare = json.loads((BARE / "manifest.json").read_text(encoding="utf-8"))
    sides = json.loads((SIDES / "manifest.json").read_text(encoding="utf-8"))
    side_states = {s["id"]: s for s in sides["states"]}
    result = {k: v for k, v in bare.items() if k != "states"}
    result["name"] = "Bill shared helmet four directions v2"
    result["status"] = "installed_four_direction_helmet_study"
    result["provenance"] = {
        "east": "owner-approved bill-shared-helmet-east-v4",
        "west": "owner-selected bill-shared-helmet-west-v2",
        "south": "bill-shared-helmet-south-v1 study",
        "north": "bill-shared-helmet-north-v1 shared rear shell study",
    }
    result["states"] = []
    for original in bare["states"]:
        key = original["id"]
        src = SOURCES[key]
        state = {k: v for k, v in original.items() if k != "sourceFrames"}
        state["frameFiles"] = []
        state["provenance"] = str(src.relative_to(ROOT)).replace("\\", "/")
        folder = HERE / "frames" / key
        folder.mkdir(parents=True, exist_ok=True)
        side = side_states.get(key)
        for i, bare_rel in enumerate(original["frameFiles"]):
            src_file = src / side["frameFiles"][i] if side else src / key.split("-")[0] / f"{i:03d}.png"
            if not src_file.is_file():
                raise FileNotFoundError(src_file)
            dest = folder / f"{i:03d}.png"
            shutil.copyfile(src_file, dest)
            outf = Image.open(dest).convert("RGBA")
            basef = Image.open(BARE / bare_rel).convert("RGBA")
            if outf.size != (184, 184) or outf.getchannel("A").getbbox() is None:
                raise AssertionError(f"Invalid frame {dest}")
            if outf.crop((0, 62, 184, 184)).tobytes() != basef.crop((0, 62, 184, 184)).tobytes():
                raise AssertionError(f"Approved suit changed below head: {dest}")
            state["frameFiles"].append(str(dest.relative_to(HERE)).replace("\\", "/"))
        if len(state["frameFiles"]) != state["frameCount"]:
            raise AssertionError(key)
        result["states"].append(state)
    (HERE / "manifest.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Bill equipped frames: {sum(s['frameCount'] for s in result['states'])}; states: {len(result['states'])}")


if __name__ == "__main__":
    main()
