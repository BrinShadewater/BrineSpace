"""Publish bounded staged actor/player packet restore evidence, not title Continue."""
from pathlib import Path
import collections, hashlib, json
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'output/marsh-animation-audit/south-snapshots-native-v1-2026-10-02'
UNIT = ROOT / 'output/marsh-animation-audit/south-snapshots-v1-2026-10-02'
DEST = ROOT / 'character/marsh-south-stop-v1/snapshot-review-v1'
VERSIONS = {0: '06', 1: '06', 2: '06', 3: '01', 4: '07', 5: '01'}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    report = json.loads((RUN / 'report.json').read_text())
    assert report['failures'] == 0 and report['cases'] == 48 and report['topologyCases'] == 2
    assert len(report['captures']) == 96
    inputs = json.loads((RUN / 'inputs-before.json').read_text())
    after = json.loads((RUN / 'inputs-after.json').read_text())
    assert inputs == after
    for path, digest in inputs.items():
        assert sha(ROOT / path) == digest, path
    assert sha(RUN / 'loaded-grid-source.txt') == sha(RUN / 'frozen-grid-source.txt') == inputs['scripts/grid_canvas.gd']
    owner = json.loads((RUN / 'owner-before.json').read_text())
    assert owner == json.loads((RUN / 'owner-after.json').read_text())
    assert 'ERROR:' not in (RUN / 'native.log').read_text(encoding='utf-8-sig')
    unit_before = json.loads((UNIT / 'inputs-before.json').read_text())
    assert unit_before == json.loads((UNIT / 'inputs-after.json').read_text())
    assert unit_before == json.loads((UNIT / 'regression-inputs-after.json').read_text())
    for prefix in ['', 'regression-', 'repaired-stop-']:
        assert json.loads((UNIT / f'{prefix}owner-before.json').read_text()) == json.loads((UNIT / f'{prefix}owner-after.json').read_text())
    expected_units = {'unit.log': 378, 'test_marsh_north_production.log': 72, 'test_marsh_north_stop_controller.log': 71, 'test_marsh_north_step_controller.log': 1529, 'test_marsh_south_start_controller.log': 155, 'repaired-stop-unit.log': 451}
    for file, count in expected_units.items():
        log = (UNIT / file).read_text(encoding='utf-8-sig')
        assert f'{count} checks,0 failures' in log and 'ERROR:' not in log, file
    for path in ['scripts/marsh_south_snapshot.gd', 'scripts/marsh_npc.gd', 'character/marsh-south-start-v1/start_controller.gd', 'character/marsh-south-stop-v1/stop_controller.gd', 'tests/test_marsh_south_snapshots.gd']:
        assert inputs[path] == unit_before[path]
    expected_cases = {f'start-{t:.2f}' for t in [.04, .18, .28, .36, .4, .7]}
    expected_cases |= {f'stop-{p}-{t:.2f}' for p in range(6) for t in [.04, .18, .28, .36]}
    expected_cases |= {f'{kind}-{p}' for p in range(6) for kind in ['cancel', 'idle-pending', 'idle-drawn']}
    pairs = collections.defaultdict(list)
    for cap in report['captures']:
        pairs[cap['case']].append(cap)
    assert set(pairs) == expected_cases
    assert {p['case'] for p in report['casePackets']} == expected_cases
    for packet in report['casePackets']:
        assert packet['diskPath'].startswith('user://south-snapshot-')
        disk = RUN / 'scratch-profile/Godot/app_userdata/BrineSpace' / packet['diskPath'][7:]
        assert disk.is_file()
        packet['scratchDiskFile'] = disk.relative_to(ROOT).as_posix()
        packet['scratchDiskSha256'] = sha(disk)
    for name, caps in pairs.items():
        assert [c['moment'] for c in caps] == ['before', 'restored']
        assert caps[0]['foot'] == caps[1]['foot'] and caps[1]['callbacks'] == 0
        assert Image.open(RUN / caps[0]['sourceFile']).convert('RGBA').tobytes() == Image.open(RUN / caps[1]['sourceFile']).convert('RGBA').tobytes()
    groups = collections.defaultdict(list); records = []
    DEST.mkdir(exist_ok=True)
    for cap in report['captures']:
        key, slot = cap['key'], cap['slot']
        if key.startswith('walk-stop-phase'):
            phase = int(key.split('phase')[1].split('-')[0])
            folder = f'character/marsh-south-stop-v1/candidate-{VERSIONS[phase]}/phase-{phase}'
        else:
            folder = {'walk-start-south': 'character/marsh-south-idle-material-v1/candidate-01/south-start', 'walk-south': 'character/marsh-south-walk-material-v1/candidate-02', 'idle-south': 'character/marsh-south-idle-material-v1/candidate-01'}[key]
        canonical = ROOT / folder / f'{slot:03d}.png'
        source = Image.open(RUN / cap['sourceFile']).convert('RGBA')
        expected = Image.open(canonical).convert('RGBA')
        assert source.size == expected.size and source.tobytes() == expected.tobytes()
        name = 'start' if cap['case'].startswith('start-') else 'phase-' + cap['case'].split('-')[1 if cap['case'].startswith('stop-') or cap['case'].startswith('cancel-') else -1]
        groups[name].append((cap, Image.open(RUN / cap['file']).convert('RGB').crop((400, 200, 550, 400)), source))
        clean = {k: v for k, v in cap.items() if k != 'sourceShaPending'}
        records.append({**clean, 'nativeSha256': sha(RUN / cap['file']), 'capturedSourceSha256': sha(RUN / cap['sourceFile']), 'sourcePath': canonical.relative_to(ROOT).as_posix(), 'sourceFileSha256': sha(canonical)})
    previews = []
    for name, entries in groups.items():
        rows = (len(entries) + 7) // 8
        native = Image.new('RGB', (1200, rows * 236), '#293b40'); source = Image.new('RGB', (1472, rows * 220), '#293b40')
        nd, sd = ImageDraw.Draw(native), ImageDraw.Draw(source)
        for index, (cap, shot, pose) in enumerate(entries):
            for board, draw, panel, width, height in [(native, nd, shot, 150, 236), (source, sd, pose, 184, 220)]:
                x, y = index % 8 * width, index // 8 * height
                board.paste(panel, (x, y + 36), panel if panel.mode == 'RGBA' else None)
                draw.text((x + 2, y + 2), cap['case'] + ' ' + cap['moment'], fill='white')
                draw.text((x + 2, y + 18), f"#{cap['slot']} callbacks{cap['callbacks']}", fill='white')
        nf, sf = name + '-native.png', name + '-source.png'; native.save(DEST / nf); source.save(DEST / sf)
        previews.append({'name': name, 'nativeBoard': nf, 'sourceBoard': sf, 'captures': len(entries)})
    evidence = {**report, 'captures': records, 'targetedInputs': inputs, 'targetedInputsAfter': after, 'targetedInputsStable': len(inputs), 'unitInputs': unit_before, 'unitInputsStable': len(unit_before), 'unitChecks': 378, 'regressionChecks': 2278, 'ownerNonLogFiles': len(owner), 'ownerUnchanged': True, 'unitAndRegressionOwnerUnchanged': True, 'sourceNativePairs': 96, 'exactOriginalRestoredSourcePairs': 48, 'loadedRendererMatchesFrozen': True, 'normalAdmission': False, 'runSaveDiskContinueVerified': False, 'previews': previews, 'publisherSha256': sha(Path(__file__)), 'nativeLogSha256': sha(RUN / 'native.log'), 'visualReview': 'Pending all seven original/restored native/source board pairs. No full station checkpoint/title Continue or natural traffic acceptance.'}
    (DEST / 'verification.json').write_text(json.dumps(evidence, indent=2) + '\n', encoding='utf-8')
    html = '<!doctype html><meta charset="utf-8"><title>Marsh South staged snapshot parity</title><style>body{background:#17282c;color:#e4e7dd;font:18px system-ui;max-width:1500px;margin:30px auto}img{max-width:100%;image-rendering:pixelated}</style><h1>Staged South actor/player snapshot parity</h1><p>' + str(report['checks']) + ' native checks/48packet cases/2topology cases/96source-native captures,0failures.378snapshot+2278related controller unit checks pass.</p><p>' + report['scope'] + '</p><p>' + str(len(inputs)) + 'targeted native inputs stable; loaded renderer matches frozen bytes. ' + str(len(owner)) + 'owner files unchanged. Original actor/player packets are isolated Godot binary files, not RunSave checkpoints.</p>'
    for p in previews:
        html += f'<h2>{p["name"]}</h2><img src="{p["nativeBoard"]}"><img src="{p["sourceBoard"]}">'
    html += '<p>' + evidence['visualReview'] + '</p><a href="verification.json">Bound evidence</a>'
    (DEST / 'index.html').write_text(html, encoding='utf-8')
    print(report['checks'], 'native checks;48original/restored source pairs;96capture pairs;378snapshot+2278regression checks;', len(owner), 'owner files unchanged')

if __name__ == '__main__':
    main()
