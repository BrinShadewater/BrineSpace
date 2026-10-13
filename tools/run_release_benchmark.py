"""Native release-readiness workloads; results are evidence, never release approval."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MIN_FREE_BYTES = 20 * 1024 ** 3


def require_storage(path: Path, additional_bytes: int = 0) -> None:
    """Refuse QA writes that would consume the last 20 GiB on their volume."""
    existing = path.resolve()
    while not existing.exists():
        existing = existing.parent
    free = shutil.disk_usage(existing).free
    if free < MIN_FREE_BYTES + additional_bytes:
        raise OSError(f'Benchmark stopped: {existing} needs 20 GiB free after '
                      f'{additional_bytes / 1024 ** 3:.2f} GiB of planned writes; '
                      f'only {free / 1024 ** 3:.2f} GiB is free')

def fingerprint(folder: Path) -> dict[str, str]:
    if not folder.exists():
        return {}
    return {str(p.relative_to(folder)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in folder.rglob('*') if p.is_file() and 'logs' not in p.relative_to(folder).parts}

def owner_folder() -> Path:
    if sys.platform == 'win32':
        return Path(os.environ['APPDATA']) / 'Godot/app_userdata/BrineSpace'
    if sys.platform == 'darwin':
        return Path.home() / 'Library/Application Support/Godot/app_userdata/BrineSpace'
    return Path(os.environ.get('XDG_DATA_HOME', str(Path.home() / '.local/share'))) / 'Godot/app_userdata/BrineSpace'

def isolated_environment(scratch: Path) -> tuple[dict, Path]:
    env = os.environ.copy()
    # Keep native QA silent even when scene settings or focus handlers run.
    env['BRINE_SILENT'] = '1'
    scratch = scratch.resolve()
    if sys.platform == 'win32':
        # GLES shader caches append long shader names/hashes. Deep evidence
        # folders can fail native directory creation even when the save fits.
        if len(str(scratch / 'Godot/app_userdata/BrineSpace')) > 100:
            evidence = scratch
            scratch = Path(tempfile.mkdtemp(prefix='bs-bench-')).resolve()
            evidence.mkdir(parents=True, exist_ok=True)
            (evidence / 'profile-location.json').write_text(json.dumps({
                'appdata': str(scratch),
                'profile': str(scratch / 'Godot/app_userdata/BrineSpace'),
                'reason': 'Keep Windows shader-cache paths short',
            }, indent=2))
        env['APPDATA'] = str(scratch)
        profile = scratch / 'Godot/app_userdata/BrineSpace'
    elif sys.platform == 'darwin':
        env['HOME'] = str(scratch)
        profile = scratch / 'Library/Application Support/Godot/app_userdata/BrineSpace'
    else:
        env['XDG_DATA_HOME'] = str(scratch)
        profile = scratch / 'Godot/app_userdata/BrineSpace'
    profile.mkdir(parents=True, exist_ok=True)
    return env, profile

def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def prepare_release_copy(executable: Path, destination: Path) -> Path:
    """QA overrides belong beside a physical copy, never beside the deliverable."""
    executable = executable.resolve()
    destination = destination.resolve()
    pack = executable.with_suffix('.pck')
    if not executable.is_file() or not pack.is_file():
        raise ValueError('Windows release benchmarking requires an EXE and matching external PCK')
    if destination.exists():
        raise FileExistsError(destination)
    require_storage(destination, executable.stat().st_size + pack.stat().st_size)
    destination.mkdir(parents=True, exist_ok=False)
    for source in (executable, pack):
        shutil.copy2(source, destination / source.name)
    source = (ROOT / 'tools/release_benchmark.gd').read_text(encoding='utf-8')
    if not source.startswith('extends SceneTree\n') or source.count('current_scene = game') != 1 or source.count('func run() -> void:\n') != 1:
        raise ValueError('Benchmark lifecycle changed; review the release adapter before running')
    source = source.replace('extends SceneTree', 'extends Node\nvar root: Window:\n\tget: return get_tree().root\nfunc quit(code := 0): get_tree().quit(code)', 1)
    source = source.replace('await process_frame', 'await get_tree().process_frame').replace('current_scene = game', 'get_tree().current_scene = game')
    source = source.replace('func run() -> void:\n', 'func run() -> void:\n\tif OS.is_debug_build(): fail("Actual release runtime required"); return\n', 1)
    (destination / 'benchmark.gd').write_text(source, encoding='utf-8')
    (destination / 'empty.tscn').write_text('[gd_scene format=3]\n[node name="ReleaseBenchmark" type="Node"]\n', encoding='utf-8')
    # BugReport writes its session lock in _enter_tree, before the workload's
    # run() guard. Verify the resolved profile before invoking that lifecycle.
    guard = '\n'.join([
        'extends "res://scripts/bug_report.gd"',
        'var qa_profile_verified := false',
        'func _enter_tree() -> void:',
        '\tvar expected := ""',
        '\tfor arg in OS.get_cmdline_user_args():',
        '\t\tif arg.begins_with("--user-dir="): expected = arg.trim_prefix("--user-dir=")',
        '\tqa_profile_verified = not expected.is_empty() and OS.get_user_data_dir().replace("\\\\", "/").simplify_path() == expected.replace("\\\\", "/").simplify_path()',
        '\tif not qa_profile_verified:',
        '\t\tpush_error("Packaged profile isolation mismatch; refusing session writes")',
        '\t\tget_tree().quit(2)',
        '\t\treturn',
        '\tsuper._enter_tree()',
        'func _ready() -> void:',
        '\tif qa_profile_verified: super._ready()',
        '',
    ])
    (destination / 'guarded_report.gd').write_text(guard, encoding='utf-8')
    (destination / 'override.cfg').write_text(
        '[application]\nrun/main_scene=' + json.dumps((destination / 'empty.tscn').as_posix()) +
        '\n[autoload]\nBugReport=' + json.dumps('*' + (destination / 'guarded_report.gd').as_posix()) + '\nReleaseBenchmark=' + json.dumps('*' + (destination / 'benchmark.gd').as_posix()) + '\n', encoding='utf-8')
    build_info = executable.parent / 'build_info.json'
    (destination / 'identity.json').write_text(json.dumps({
        'build': json.loads(build_info.read_text(encoding='utf-8')) if build_info.exists() else None,
        'executable_sha256': file_sha256(executable),
        'pck_sha256': file_sha256(pack),
        'fixture_sha256': hashlib.sha256(source.encode('utf-8')).hexdigest(),
        'profile_guard_sha256': hashlib.sha256(guard.encode('utf-8')).hexdigest(),
    }, indent=2), encoding='utf-8')
    return destination / executable.name


def release_copy_storage(executable: Path) -> None:
    """Remove only unchanged physical QA binaries; preserve small evidence files."""
    identity = json.loads((executable.parent / 'identity.json').read_text(encoding='utf-8'))
    targets = [(executable, identity['executable_sha256']),
               (executable.with_suffix('.pck'), identity['pck_sha256'])]
    # Validate both before deleting either. Never follow a substituted link.
    for path, expected in targets:
        if path.is_symlink() or not path.is_file() or file_sha256(path) != expected:
            raise ValueError(f'QA runtime changed; retained for investigation: {path}')
    removed_bytes = sum(path.stat().st_size for path, _ in targets)
    for path, _ in targets:
        path.unlink()
    (executable.parent / 'storage-cleanup.json').write_text(json.dumps({
        'removed_bytes': removed_bytes, 'removed': [str(p) for p, _ in targets],
        'reason': 'Finished benchmark; delivery binaries and build identity retained',
    }, indent=2), encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    runtime = parser.add_mutually_exclusive_group(required=True)
    runtime.add_argument('--godot', help='Editor executable for development diagnostics')
    runtime.add_argument('--release-exe', type=Path, help='Windows release EXE with adjacent PCK; tested through an isolated physical copy')
    parser.add_argument('--save', type=Path, required=True, help='Frozen 12-room report checkpoint; always copied')
    parser.add_argument('--output', type=Path, required=True, help='New evidence directory')
    parser.add_argument('--scenarios', nargs='+', choices=['fresh', 'reported', 'large', 'mixed_large'], default=['fresh', 'reported', 'large'])
    parser.add_argument('--resolutions', nargs='+', default=['1920x1080', '2560x1440'])
    parser.add_argument('--runs', type=int, default=3)
    parser.add_argument('--frames', type=int, default=180)
    parser.add_argument('--trace', action='store_true', help='Collect up to 4096 CPU frame-boundary records outside measured samples')
    parser.add_argument('--texture-inventory', action='store_true', help='Opt-in bounded pool metadata inventory after measured phases; no GPU readbacks')
    parser.add_argument('--actions', nargs='+', choices=['idle', 'pan', 'zoom', 'lighting', 'placement', 'demolition', 'interface', 'save'], default=['idle', 'pan', 'zoom', 'lighting', 'placement', 'demolition', 'interface', 'save'])
    args = parser.parse_args()
    out = args.output.resolve()
    owner = owner_folder().resolve()
    if out.exists() or out == owner or owner in out.parents:
        parser.error('Use a new evidence directory outside the owner profile')
    if args.runs < 1 or args.frames < 60 or not args.save.is_file():
        parser.error('Need an existing checkpoint, at least one run and 60 frames per phase')
    if args.release_exe and sys.platform != 'win32':
        parser.error('--release-exe currently supports Windows; Mac bundle isolation remains separate')
    require_storage(out)
    require_storage(Path(tempfile.gettempdir()))
    out.mkdir(parents=True)
    before = fingerprint(owner)
    (out/'owner-before.json').write_text(json.dumps(before))
    records = []
    result_code = 0
    release_copy = None
    try:
        release_copy = prepare_release_copy(args.release_exe, out / 'release-runtime') if args.release_exe else None
        for scenario in args.scenarios:
            for resolution in args.resolutions:
                width, height = map(int, resolution.split('x'))
                env, profile = isolated_environment(out / f'{scenario}-{resolution}-profile')
                if (owner/'room_layouts.json').exists():
                    shutil.copy2(owner/'room_layouts.json', profile/'room_layouts.json')
                for repeat in range(args.runs):
                    require_storage(out)
                    require_storage(profile)
                    label = f'{scenario}-{resolution}-{repeat+1}'
                    checkpoint = profile/'input.save'
                    shutil.copy2(args.save, checkpoint)
                    result = out/(label+'.json')
                    launch = [str(release_copy), '--windowed', '--resolution', resolution] if release_copy else [args.godot, '--path', str(ROOT), '-s', 'res://tools/release_benchmark.gd']
                    cmd = launch + ['--',
                           f'--user-dir={profile}', f'--save={checkpoint}', f'--scenario={scenario}',
                           f'--width={width}', f'--height={height}', f'--frames={args.frames}', f'--actions={",".join(args.actions)}', f'--out={result}']
                    if args.trace:
                        cmd.append('--trace=true')
                    if args.texture_inventory:
                        cmd.append('--texture-inventory=true')
                    with (out/(label+'.log')).open('w', encoding='utf-8') as log:
                        completed = subprocess.run(cmd, cwd=release_copy.parent if release_copy else ROOT, env=env, stdout=log, stderr=log, timeout=600)
                    log_text = (out/(label+'.log')).read_text(encoding='utf-8', errors='replace')
                    valid = completed.returncode == 0 and result.exists() and 'RELEASE BENCHMARK COMPLETE' in log_text and 'ERROR:' not in log_text
                    record = {'run': label, 'valid': valid, 'profile': str(profile), 'loading_kind': 'fresh application/profile; OS disk cache uncontrolled' if repeat == 0 else 'warm application manifest; fresh process'}
                    if valid:
                        data = json.loads(result.read_text())
                        if release_copy and data.get('debug') is not False:
                            print('Release result did not prove debug=false'); return 1
                        record.update(scene_load_ms=data.get('scene_load_ms'), scene_request_to_ready_ms=data.get('scene_request_to_ready_ms'), engine_uptime_at_ready_ms=data.get('engine_uptime_at_ready_ms'), automatic_reports_saved=data.get('automatic_reports_saved'))
                        record.update(debug=data['debug'], execution_kind='packaged release fixture' if release_copy else 'editor fixture', ready_ms=data['ready_ms'], texture_mb=data['memory_end_mb'],
                                      phases_passing=sum(p['p95_ms'] <= 16.7 and p['p99_ms'] <= 25 and p['max_ms'] <= 100 for p in data['phases']),
                                      phase_count=len(data['phases']))
                    else:
                        result_code = 1
                    records.append(record)
                    (out/'summary.json').write_text(json.dumps(records, indent=2))
                    print(json.dumps(record), flush=True)
                    if not valid:
                        print(log_text[-2000:]); return 1
    finally:
        if release_copy is not None:
            try:
                release_copy_storage(release_copy)
            except (OSError, ValueError) as error:
                print(f'QA storage cleanup incomplete: {error}', file=sys.stderr)
                result_code = 1
        after = fingerprint(owner)
        changes = [k for k in before.keys() | after.keys() if before.get(k) != after.get(k)]
        (out/'owner-check.json').write_text(json.dumps({'before': len(before), 'after': len(after), 'changes': changes}, indent=2))
        if changes:
            print('Owner profile changed during run; investigate before accepting evidence.', file=sys.stderr)
            result_code = 1
    return result_code

if __name__ == '__main__':
    raise SystemExit(main())
