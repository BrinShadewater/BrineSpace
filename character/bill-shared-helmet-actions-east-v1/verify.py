"""Validate the selected east action study before runtime installation."""

import json
from pathlib import Path

import numpy as np
from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OLD = ROOT / "major-bill-v3/packs/helmet-184x184-p92-172"
BARE_OLD = ROOT / "major-bill-v3/packs/bare-184x184-p92-172"
BARE = ROOT / "bill-action-east-matched-v1"
APPROVED = ROOT / "bill-shared-helmet-east-matte-v1"
BARE_IDLE = ROOT / "crew-runtime-matte-v1/bill"


def states(root: Path) -> dict:
    return {s["id"]: s for s in json.loads((root / "manifest.json").read_text(encoding="utf-8"))["states"]}


def metadata(root: Path) -> dict:
    return json.loads((root / "manifest.json").read_text(encoding="utf-8"))


def frame(root: Path, state: dict, i: int) -> np.ndarray:
    return np.asarray(Image.open(root / state["frameFiles"][i]).convert("RGBA"))


def main() -> None:
    old, bare_old = states(OLD), states(BARE_OLD)
    new, bare = states(HERE), states(BARE)
    approved, bare_idle = states(APPROVED), states(BARE_IDLE)
    checks = 0
    for root in (HERE, BARE):
        pack = metadata(root)
        assert pack["pivot"] == [92, 172]
        assert pack["standingHeight"] == 148
        checks += 2
    for key in new:
        for pack in (new, bare):
            assert len(pack[key]["frameFiles"]) == 6
            checks += 1
        assert new[key]["frameDurationsMs"] == old[key]["frameDurationsMs"]
        assert bare[key]["frameDurationsMs"] == bare_old[key]["frameDurationsMs"]
        checks += 2
        for i in range(6):
            assert frame(HERE, new[key], i).shape == (184, 184, 4)
            assert frame(BARE, bare[key], i).shape == (184, 184, 4)
            checks += 2
    for key, i in (("interact-east", 0), ("interact-east", 5), ("kneel-east", 0), ("stand-east", 5)):
        assert np.array_equal(frame(HERE, new[key], i), frame(APPROVED, approved["idle-east"], 0))
        assert np.array_equal(frame(BARE, bare[key], i), frame(BARE_IDLE, bare_idle["idle-east"], 0))
        checks += 2
    for first, last, second, start in (("kneel-east", 5, "repair-east", 0), ("repair-east", 5, "stand-east", 0)):
        assert np.array_equal(frame(HERE, new[first], last), frame(HERE, new[second], start))
        assert np.array_equal(frame(BARE, bare[first], last), frame(BARE, bare[second], start))
        checks += 2
    for i in range(1, 5):
        equipped_idle = frame(APPROVED, approved["idle-east"], 0)
        equipped_action = frame(HERE, new["interact-east"], i)
        bare_idle_frame = frame(BARE_IDLE, bare_idle["idle-east"], 0)
        bare_action = frame(BARE, bare["interact-east"], i)
        assert np.array_equal(equipped_action[:58], equipped_idle[:58]), (i, "helmet/head changed")
        assert np.array_equal(equipped_action[125:], equipped_idle[125:]), (i, "feet changed")
        assert np.array_equal(bare_action[:58], bare_idle_frame[:58]), (i, "bare head changed")
        assert np.array_equal(bare_action[125:], bare_idle_frame[125:]), (i, "bare feet changed")
        checks += 4
    anchors = json.loads((HERE / "checks.json").read_text(encoding="utf-8"))
    for key, rows in anchors.items():
        for i, info in enumerate(rows):
            hx, hy = info["helmet"]
            alpha = frame(HERE, new[key], i)[:, :, 3]
            assert int(alpha[hy + 40, hx + 9:hx + 38].min()) >= 250, (key, i, "neck join")
            checks += 1
    a = frame(HERE, new["interact-east"], 0)
    b = frame(HERE, new["interact-east"], 1)
    region = (slice(66, 110), slice(65, 112))
    x, y = a[region], b[region]
    x_median = float(np.median(x[x[:, :, 3] > 235, :3].mean(axis=1)))
    y_median = float(np.median(y[y[:, :, 3] > 235, :3].mean(axis=1)))
    assert abs(x_median - y_median) < 4, (x_median, y_median)
    checks += 1
    print(f"BILL EAST ACTION CANDIDATE: {checks} checks, 0 failures; standing suit median {x_median:.1f}/{y_median:.1f}")


if __name__ == "__main__":
    main()
