#!/usr/bin/env python3
"""Prepare a local development Xcode project; never uploads or distributes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EDITOR = Path('/Users/alexyesilcimen/Desktop/Mac Test/Brinespace/qa-sdk/Godot.app/Contents/MacOS/Godot')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--team-id', default=os.environ.get('BRINESPACE_IOS_TEAM_ID', ''))
    parser.add_argument('--godot', type=Path, default=DEFAULT_EDITOR)
    parser.add_argument('--output', type=Path, default=Path('/Users/Shared/BrineSpace-iPad-QA-build'))
    parser.add_argument('--preflight-only', action='store_true')
    args = parser.parse_args()
    env = os.environ.copy()
    developer = Path('/Applications/Xcode.app/Contents/Developer')
    if developer.is_dir():
        env['DEVELOPER_DIR'] = str(developer)
    problems = []
    result = subprocess.run(['xcrun', '--find', 'xcodebuild'], env=env, capture_output=True, text=True)
    if result.returncode:
        problems.append('Install full Xcode and open it once to complete setup (Command Line Tools alone are insufficient).')
    if not re.fullmatch(r'[A-Za-z0-9]{10}', args.team_id):
        problems.append('Select your signing team in Xcode, then provide its 10-character Team ID with --team-id. No password is needed here.')
    if not args.godot.is_file():
        problems.append('Godot executable not found: ' + str(args.godot))
    else:
        version = subprocess.check_output([str(args.godot), '--version'], text=True).strip()
        if version != '4.7.2.stable.official.ed1daf0bf':
            problems.append('Expected verified official Godot 4.7.2; found ' + version)
    expected = json.loads((ROOT/'IPAD_QA_PREPARATION.json').read_text())['ios_template_sha256']
    template = ROOT/'output/export-tools/4.7.2-stable/ios.zip'
    if not template.is_file() or hashlib.sha256(template.read_bytes()).hexdigest() != expected:
        problems.append('iOS template missing or hash differs from the verified official archive.')
    if problems:
        for problem in problems:
            print('PENDING: ' + problem)
        return 2
    print('PREFLIGHT PASS: Xcode located, official engine/template match, signing team supplied.')
    if args.preflight_only:
        return 0
    output = args.output.resolve()
    if output.exists() and any(output.iterdir()):
        raise RuntimeError('Choose a fresh output folder; previous evidence will not be overwritten.')
    output.mkdir(parents=True, exist_ok=True)
    preset = ROOT/'export_presets.cfg'
    text = preset.read_text()
    marker = '[preset.5.options]'
    before, options = text.split(marker, 1)
    options = re.sub(r'^application/app_store_team_id=.*$', 'application/app_store_team_id=' + json.dumps(args.team_id), options, count=1, flags=re.M)
    preset.write_text(before + marker + options)
    for tool, extra in [('build_release_manifest.py', ['--preset', 'iPad QA']), ('set_raw_png_import_keep.py', [])]:
        subprocess.run([sys.executable, str(ROOT/'tools'/tool), *extra], cwd=ROOT, env=env, check=True)
    for name in ['build_info.json', 'IPAD_QA_PREPARATION.json']:
        (output/name).write_bytes((ROOT/name).read_bytes())
    (output/'expected-manifest.json').write_bytes((ROOT/'assets/runtime-release.json').read_bytes())
    with (output/'export.log').open('w') as log:
        result = subprocess.run([str(args.godot), '--headless', '--path', str(ROOT), '--export-release', 'iPad QA', str(output/'BrineSpaceiPad.ipa')], cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
    body = (output/'export.log').read_text(errors='replace')
    if result.returncode or 'ERROR:' in body or 'SCRIPT ERROR' in body:
        raise RuntimeError('Export failed; inspect ' + str(output/'export.log'))
    project = output/'BrineSpaceiPad.xcodeproj'
    if not project.is_dir():
        raise RuntimeError('Exporter did not produce the expected Xcode project; inspect export.log.')
    print('Xcode project created: ' + str(project))
    print('Device compilation, signing, installation and actual iPad testing remain separate steps.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
