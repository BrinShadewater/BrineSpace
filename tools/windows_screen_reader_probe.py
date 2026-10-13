"""Time the read-only Windows screen-reader query without Godot or game assets.

Diagnostic only: this does not certify frame pacing or change accessibility.
Writes only the explicitly requested JSON output, never a BrineSpace profile.
"""
from __future__ import annotations

import argparse
import ctypes
import json
import math
from pathlib import Path
import sys
import time


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--seconds', type=float, default=45)
    parser.add_argument('--interval-ms', type=float, default=1000 / 120)
    args = parser.parse_args()
    if sys.platform != 'win32':
        parser.error('This read-only probe requires Windows.')
    if not math.isfinite(args.seconds) or not 1 <= args.seconds <= 300:
        parser.error('--seconds must be between 1 and 300')
    if not math.isfinite(args.interval_ms) or not 1 <= args.interval_ms <= 1000:
        parser.error('--interval-ms must be between 1 and 1000')
    if args.output.exists():
        parser.error('Choose a new output file; existing evidence is not overwritten.')

    from ctypes import wintypes as W
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    query = user32.SystemParametersInfoA
    query.argtypes = [W.UINT, W.UINT, ctypes.c_void_p, W.UINT]
    query.restype = W.BOOL
    rows = []
    started = time.perf_counter()
    deadline = started + args.seconds
    while time.perf_counter() < deadline:
        active = W.BOOL()
        unix = time.time()
        before = time.perf_counter()
        ctypes.set_last_error(0)
        ok = query(0x0046, 0, ctypes.byref(active), 0)  # SPI_GETSCREENREADER
        error = ctypes.get_last_error() if not ok else 0
        elapsed_ms = (time.perf_counter() - before) * 1000
        rows.append({'unix': unix, 'ms': elapsed_ms, 'ok': bool(ok),
                     'active': bool(active.value) if ok else None, 'error': error})
        time.sleep(args.interval_ms / 1000)

    durations = sorted(row['ms'] for row in rows)
    summary = {
        'calls': len(rows), 'elapsed_seconds': time.perf_counter() - started,
        'p95_ms': durations[math.ceil(len(rows) * .95) - 1],
        'p99_ms': durations[math.ceil(len(rows) * .99) - 1],
        'max_ms': max(durations), 'over_50_ms': sum(x > 50 for x in durations),
        'failures': sum(not row['ok'] for row in rows),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump({'schema_version': 1, 'query': 'SPI_GETSCREENREADER',
                   'windows_version': sys.getwindowsversion().build,
                   'interval_ms': args.interval_ms, 'summary': summary,
                   'samples': rows}, stream, indent=2)
    print(json.dumps(summary))
    return 1 if summary['failures'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
