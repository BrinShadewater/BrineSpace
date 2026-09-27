"""Measure Studio report regressions and validate drone sampling with isolated saves."""
import os, json, hashlib, subprocess, sys, shutil
from pathlib import Path
root = Path(__file__).resolve().parents[1]
out = root / 'output/owner-report-fixes-2026-09-27'
out.mkdir(parents=True, exist_ok=True)
owner = Path(os.environ['APPDATA']) / 'Godot/app_userdata/BrineSpace'
def fingerprint():
    return {p.relative_to(owner).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(owner.rglob('*')) if p.is_file()}
before = fingerprint()
env = os.environ.copy()
env.update(APPDATA=str(out/'scratch/roaming'), LOCALAPPDATA=str(out/'scratch/local'), BRINE_REPORT_TEST='isolated')
for key in ['APPDATA', 'LOCALAPPDATA']: Path(env[key]).mkdir(parents=True, exist_ok=True)
profile = Path(env['APPDATA'])/'Godot/app_userdata/BrineSpace'
profile.mkdir(parents=True, exist_ok=True)
shutil.copy2(owner/'room_layouts.json', profile/'room_layouts.json')
log_path = out/'studio-latency.log'
try:
    with log_path.open('w', encoding='utf-8') as log:
        proc = subprocess.run(['C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe',
            '--path', str(root), '--script', 'res://tests/test_studio_report_latency.gd'],
            cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=180)
        if proc.returncode == 0:
            proc = subprocess.run(['C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe',
                '--headless', '--path', str(root), '--script', 'res://tests/test_drone_runtime_animation.gd'],
                cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=60)
finally:
    after = fingerprint()
    (out/'studio-owner-fingerprints.json').write_text(json.dumps({'before':before,'after':after}, indent=2))
    print('Owner profile unchanged:', before == after)
text = log_path.read_text(encoding='utf-8', errors='replace')
for line in text.splitlines():
    if 'ERROR' in line or 'STUDIO PROBE' in line or 'DRONE RUNTIME' in line: print(line[:350])
sys.exit(int(proc.returncode != 0 or before != after or 'ERROR' in text or 'STUDIO PROBE COMPLETE' not in text))
