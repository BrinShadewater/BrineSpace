"""Run the September 27 report regression fixture without touching player saves."""
import os, json, hashlib, subprocess, sys, shutil, time
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
shutil.copy2(out/'003107/diagnostics/live_station.save', profile/'mining-report.save')
shutil.copy2(out/'003541/diagnostics/live_station.save', profile/'lag-report.save')
log_path = out/'controls.log'
try:
    with log_path.open('w', encoding='utf-8') as log:
        command = ['C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe',
            '--path', str(root), '--script', 'res://tests/test_report_controls_sept27.gd']
        if os.environ.get('BRINE_SAMPLE_CPU') == '1':
            import ctypes
            from ctypes import wintypes
            kernel = ctypes.WinDLL('kernel32', use_last_error=True)
            get_times = kernel.GetProcessTimes
            get_times.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
            get_times.restype = wintypes.BOOL
            samples = []
            with subprocess.Popen(command, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT) as proc:
                deadline = time.monotonic() + 180
                while proc.poll() is None:
                    if time.monotonic() > deadline:
                        proc.kill()
                        raise TimeoutError('Isolated replay exceeded 180 seconds')
                    values = [wintypes.FILETIME() for _ in range(4)]
                    if get_times(int(proc._handle), *(ctypes.byref(v) for v in values)):
                        cpu_ms = sum((v.dwHighDateTime << 32) | v.dwLowDateTime for v in values[2:]) / 10000
                        samples.append([time.time() * 1000, cpu_ms])
                    time.sleep(.01)
            (out/'camera-cpu-samples.json').write_text(json.dumps(samples))
        else:
            proc = subprocess.run(command, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=180)

finally:
    after = fingerprint()
    (out/'controls-owner-fingerprints.json').write_text(json.dumps({'before':before,'after':after}, indent=2))
    print('Owner profile unchanged:', before == after)
text = log_path.read_text(encoding='utf-8', errors='replace')
for line in text.splitlines():
    if 'ERROR' in line or 'REPORT CONTROLS' in line or 'LAG REPLAY' in line or 'CAMERA REPLAY' in line or 'CAMERA PREPARE' in line or 'CAMERA REVEAL' in line: print(line[:350])
sys.exit(int(proc.returncode != 0 or before != after or 'ERROR' in text or 'REPORT CONTROLS: 0 failures' not in text))
