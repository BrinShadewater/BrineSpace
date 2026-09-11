#!/usr/bin/env python3
"""Native-aware test runner for the tests/ tree.

Solves the problems a naive headless sweep hits (2026-09-10 audit):
  - Tests that await RenderingServer.frame_post_draw, or read
    get_texture().get_image(), hang or abort under the headless dummy driver.
    They are routed to the NATIVE lane and skipped headless, not failed.
  - Tests that deliberately reject headless execution exit with code 2
    (project convention: camera_pixel_stability, content_cache_parity,
    layout_performance_guards). Exit 2 maps to SKIP-NATIVE, not FAIL.
  - Godot's shutdown teardown noise ("Unreferenced static string", RID leaks)
    is a kill signature, not a failure. A timed-out test that already printed
    its PASS line is reported PASS-HUNG.

Lanes are detected from test source at run time (always current); exceptions
and subsystem groups live in tests/index.json.

Examples:
  python tools/run_tests.py --list                 # classify without running
  python tools/run_tests.py                        # headless lane, all tests
  python tools/run_tests.py --subsystem flood      # one subsystem
  python tools/run_tests.py --only test_run_save   # explicit selection
  python tools/run_tests.py --native               # run the native lane
                                                   # (real display required)

Results go to output/test-runs/<stamp>/ (summary.tsv + per-test logs).
Exit code: non-zero if any selected test FAILs or times out without a PASS line.
"""
import argparse
import datetime
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GODOT = {
    "win32": "C:/Users/Alex/Desktop/Projects/Godot_v4.6.1-stable_win64.exe",
}
PASS_LINE = re.compile(r"\bPASS\b|failures=0|:\s*0 failures\b")
FAIL_LINE = re.compile(r"\bFAIL\b|SCRIPT ERROR|failures=[1-9]|:\s*[1-9]\d* failures")
KILL_NOISE = re.compile(
    r"Unreferenced static string|ObjectDB instances leaked|resources still in use"
    r"|RID allocations|Pages in use exist|NavMeshGeometryParser"
)


def load_index() -> dict:
    path = ROOT / "tests/index.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def detect_lane(test: Path, index: dict) -> tuple[str, str]:
    """Return (lane, reason). Lane: headless | native | skip."""
    override = index.get("lanes", {}).get(test.stem)
    if override:
        return override.get("lane", "headless"), override.get("reason", "index.json override")
    src = test.read_text(encoding="utf-8", errors="replace")
    render_bound = "frame_post_draw" in src or "get_texture().get_image()" in src
    guarded = "headless" in src
    if render_bound and not guarded:
        return "native", "awaits rendered frames with no headless guard"
    return "headless", "headless-safe (guards its captures)" if render_bound else "no render dependency"


def classify_result(code: int, output: str, timed_out: bool) -> tuple[str, str]:
    """Return (verdict, detail line)."""
    lines = [l for l in output.splitlines() if l.strip() and not KILL_NOISE.search(l)]
    passed = any(PASS_LINE.search(l) and not FAIL_LINE.search(l) for l in lines)
    failed = any(FAIL_LINE.search(l) for l in lines)
    detail = next((l for l in lines if FAIL_LINE.search(l)), "")
    if not detail:
        detail = next((l for l in reversed(lines) if PASS_LINE.search(l)), "")
    if timed_out:
        if passed and not failed:
            return "PASS-HUNG", detail or "printed PASS, then hung at exit"
        return "TIMEOUT", detail or "no verdict line before the timeout"
    if code == 2 and ("native" in output.lower() or "headless" in output.lower()):
        return "SKIP-NATIVE", "test rejects headless execution by design (exit 2)"
    if code == 0 and not failed:
        return "PASS", detail
    return f"FAIL({code})", detail[:240]


def run(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--godot", default=DEFAULT_GODOT.get(sys.platform, "godot"))
    parser.add_argument("--timeout", type=int, default=120, help="seconds per test")
    parser.add_argument("--subsystem", help="group from tests/index.json")
    parser.add_argument("--only", help="comma-separated test names (stem)")
    parser.add_argument("--native", action="store_true",
                        help="run the native lane (real display) instead of headless")
    parser.add_argument("--list", action="store_true", help="classify only, run nothing")
    parser.add_argument("--playtests", action="store_true",
                        help="include tests/playtest_*.gd (long; native recommended)")
    args = parser.parse_args(argv)

    index = load_index()
    patterns = ["test_*.gd"] + (["playtest_*.gd"] if args.playtests else [])
    tests = sorted(p for pattern in patterns for p in (ROOT / "tests").glob(pattern))
    if args.subsystem:
        wanted = set(index.get("subsystems", {}).get(args.subsystem, []))
        if not wanted:
            known = ", ".join(sorted(index.get("subsystems", {})))
            print(f"Unknown subsystem {args.subsystem!r}. Known: {known}")
            return 2
        tests = [t for t in tests if t.stem in wanted]
    if args.only:
        wanted = {name.strip() for name in args.only.split(",")}
        tests = [t for t in tests if t.stem in wanted]

    lane_wanted = "native" if args.native else "headless"
    plan = [(t, *detect_lane(t, index)) for t in tests]
    if args.list:
        for t, lane, reason in plan:
            print(f"{t.stem}\t{lane}\t{reason}")
        counts = {}
        for _, lane, _ in plan:
            counts[lane] = counts.get(lane, 0) + 1
        print("LANES:", ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
        return 0

    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = ROOT / "output" / "test-runs" / f"{stamp}-{lane_wanted}"
    (out_dir / "logs").mkdir(parents=True, exist_ok=True)
    summary_rows = []
    tally = {}
    for t, lane, reason in plan:
        if lane == "skip":
            verdict, detail, duration = "SKIP", reason, 0.0
        elif lane != lane_wanted:
            verdict, detail, duration = f"SKIP-{lane.upper()}", reason, 0.0
        else:
            cmd = [args.godot, "--path", str(ROOT), "-s", f"res://tests/{t.name}"]
            if not args.native:
                cmd.insert(1, "--headless")
            per_timeout = int(index.get("lanes", {}).get(t.stem, {}).get("timeout", args.timeout))
            started = time.monotonic()
            timed_out = False
            try:
                proc = subprocess.run(cmd, capture_output=True, text=True,
                                      timeout=per_timeout, errors="replace")
                code, output = proc.returncode, proc.stdout + proc.stderr
            except subprocess.TimeoutExpired as exc:
                timed_out, code = True, -1
                output = ((exc.stdout or "") if isinstance(exc.stdout, str) else "") + \
                         ((exc.stderr or "") if isinstance(exc.stderr, str) else "")
            duration = time.monotonic() - started
            (out_dir / "logs" / f"{t.stem}.log").write_text(output, encoding="utf-8")
            verdict, detail = classify_result(code, output, timed_out)
        tally[verdict.split("(")[0]] = tally.get(verdict.split("(")[0], 0) + 1
        summary_rows.append(f"{t.stem}\t{verdict}\t{duration:.1f}s\t{detail}")
        print(summary_rows[-1])
    (out_dir / "summary.tsv").write_text("\n".join(summary_rows) + "\n", encoding="utf-8")
    print("RESULT:", ", ".join(f"{k}={v}" for k, v in sorted(tally.items())),
          f"-> {out_dir.relative_to(ROOT)}")
    bad = sum(v for k, v in tally.items() if k.startswith("FAIL") or k == "TIMEOUT")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(run())
