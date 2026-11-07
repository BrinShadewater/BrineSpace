"""Build the local Universal 2 Mac candidate with verified official templates.

Run bundle/PCK audits after export; native Mac acceptance remains a separate gate.
"""
import argparse
import configparser
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def selected_template(root):
    settings = configparser.ConfigParser(interpolation=None)
    settings.read(root / 'export_presets.cfg', encoding='utf-8-sig')
    matches = [section for section in settings.sections()
               if not section.endswith('.options')
               and settings[section].get('name') == '"macOS Game"']
    if len(matches) != 1:
        raise RuntimeError('Expected exactly one macOS Game preset')
    preset = matches[0]
    if settings[preset].get('platform') != '"macOS"':
        raise RuntimeError('macOS Game must select the macOS platform')
    options = settings[preset + '.options']
    path = json.loads(options.get('custom_template/release', '""'))
    if not path:
        raise RuntimeError('macOS Game must select an explicit verified template')
    if path.startswith('res://'):
        path = path[6:]
    return (root / path).resolve()


def digest(stream, algorithm='sha256'):
    result = hashlib.new(algorithm)
    for chunk in iter(lambda: stream.read(1024 * 1024), b''):
        result.update(chunk)
    return result.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--godot', required=True)
    parser.add_argument('--output', required=True, help='New candidate directory')
    parser.add_argument('--preflight-only', action='store_true', help='Verify selected template without exporting or writing manifests')
    args = parser.parse_args()
    target = Path(args.output).resolve()
    if (target / 'BrineSpace.zip').exists():
        raise RuntimeError('Choose a new candidate directory; existing ZIP will not be overwritten')
    templates = ROOT / 'output/export-tools/4.7.2-stable'
    selected = selected_template(ROOT)
    bundle = templates / 'Godot_v4.7.2-stable_export_templates.tpz'
    sums = (templates / 'SHA512-SUMS.txt').read_text(encoding='utf-8')
    expected = [parts[0] for line in sums.splitlines() if len(parts := line.split()) == 2
                and parts[-1].lstrip('*') == bundle.name]
    with bundle.open('rb') as stream:
        if len(expected) != 1 or digest(stream, 'sha512') != expected[0].lower():
            raise RuntimeError('Template archive SHA512 mismatch')
    version = subprocess.check_output([args.godot, '--version'], text=True).strip()
    with zipfile.ZipFile(bundle) as archive:
        template_version = archive.read('templates/version.txt').decode().strip()
        if not version.startswith(template_version + '.'):
            raise RuntimeError(f'Editor/template version mismatch: {version} / {template_version}')
        with archive.open('templates/macos.zip') as stream:
            expected_mac = digest(stream)
        with selected.open('rb') as stream:
            if digest(stream) != expected_mac:
                raise RuntimeError('Mac template differs from verified official archive')
    if args.preflight_only:
        print(f'Verified selected Mac template: {selected}; editor {version}')
        return
    target.mkdir(parents=True, exist_ok=True)
    for script, options in [('build_release_manifest.py', ['--preset', 'macOS Game']),
                            ('set_raw_png_import_keep.py', [])]:
        subprocess.run([sys.executable, str(ROOT / 'tools' / script), *options], cwd=ROOT, check=True)
    shutil.copy2(ROOT / 'assets/runtime-release.json', target / 'expected-manifest.json')
    shutil.copy2(ROOT / 'build_info.json', target / 'build_info.json')
    log = target / 'export.log'
    with log.open('w', encoding='utf-8') as stream:
        process = subprocess.run([args.godot, '--headless', '--path', str(ROOT),
                                  '--export-release', 'macOS Game', str(target / 'BrineSpace.zip')],
                                 stdout=stream, stderr=subprocess.STDOUT)
    errors = [line for line in log.read_text(encoding='utf-8', errors='replace').splitlines()
              if 'ERROR:' in line or 'SCRIPT ERROR' in line]
    if process.returncode or errors:
        raise RuntimeError(f'Export failed; inspect {log}: ' + '\n'.join(errors[:5]))
    subprocess.run([sys.executable, str(ROOT / 'tools/audit_macos_bundle.py'),
                    str(target / 'BrineSpace.zip')], check=True)
    print(f'Export and bundle structure passed: {target}. Exact PCK and native Mac checks remain.')


if __name__ == '__main__':
    main()
