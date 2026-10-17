"""Run the native window review with a scratch profile and owner-file fingerprints."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
PACK = Path(__file__).resolve().parent
OWNER = Path(os.environ['APPDATA']) / 'Godot/app_userdata/BrineSpace'

def fingerprint():
    return {str(p.relative_to(OWNER)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in OWNER.rglob('*') if p.is_file()}

before = fingerprint()
(PACK/'owner-before.json').write_text(json.dumps(before, indent=2))
env = os.environ.copy()
env['APPDATA'] = str(PACK/'scratch-appdata')
env['BRINE_WINDOW_TEST'] = 'isolated'
(PACK/'scratch-appdata').mkdir(exist_ok=True)
with (PACK/'native-review.log').open('w') as log:
    result = subprocess.run([
        'C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe',
        '--path', str(ROOT), '--rendering-method', 'gl_compatibility',
        '-s', 'res://tools/review_ocean_windows.gd', '--', *sys.argv[1:],
    ], env=env, stdout=log, stderr=subprocess.STDOUT, timeout=180)
after = fingerprint()
(PACK/'owner-after.json').write_text(json.dumps(after, indent=2))
summary = {'exit_code':result.returncode,'owner_unchanged':before==after,
           'owner_files':len(before),'native_captures':len(list((PACK/'review').glob('*.png'))),
           'owner_changed_paths':[k for k in before if k in after and before[k]!=after[k]],
           'owner_added_paths':[k for k in after if k not in before],
           'owner_removed_paths':[k for k in before if k not in after]}
(PACK/'verification.json').write_text(json.dumps(summary, indent=2))
print(json.dumps(summary))
for line in (PACK/'native-review.log').read_text(errors='replace').splitlines():
    if any(word in line for word in ['Error','ERROR','WINDOW_REVIEW','WINDOW_PROFILE']): print(line)
raise SystemExit(result.returncode or (0 if before==after else 1))
