"""Bind six real South stop interruption branches and representative visual boards."""
from pathlib import Path
import collections, hashlib, json
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'output/marsh-animation-audit/south-stop-six-interruptions-v1-2026-10-02'
DEST = ROOT / 'character/marsh-south-stop-v1/six-interruption-review-v1'
VERSIONS = {0: '06', 1: '06', 2: '06', 3: '01', 4: '07', 5: '01'}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    report = json.loads((RUN / 'report.json').read_text())
    assert report['failures'] == 0 and report['cases'] == 384 and report['branches'] == 6
    assert len(report['captures']) == 960
    before = json.loads((RUN / 'inputs-before.json').read_text())
    after = json.loads((RUN / 'inputs-after.json').read_text())
    changed = [p for p in before if before[p] != after[p]]
    assert set(changed) <= {'scripts/grid_canvas.gd'}, changed
    for path, digest in after.items():
        assert sha(ROOT / path) == digest, path
    renderer = sha(RUN / 'loaded-grid-source.txt')
    assert renderer == sha(RUN / 'frozen-grid-source.txt') == before['scripts/grid_canvas.gd']
    owner = json.loads((RUN / 'owner-before.json').read_text())
    assert owner == json.loads((RUN / 'owner-after.json').read_text())
    assert 'ERROR:' not in (RUN / 'native.log').read_text(encoding='utf-8-sig')
    contract = json.loads((ROOT / 'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states']
    cases = collections.defaultdict(list)
    for cap in report['captures']:
        cases[(cap['gaitPhase'], cap['work'], cap['kind'], cap['phase'])].append(cap)
    assert len(cases) == 384
    expected_cases = {(p, w, k, t) for p in range(6) for w in ['curiosity', 'hunger', 'fatigue', 'maintenance'] for k in ['power', 'suspension'] for t in [.04, .18, .28, .36]}
    expected_cases |= {(p, 'curiosity', k, t) for p in range(6) for k in ['fire', 'water-medium', 'water-high', 'charge', 'injury', 'death', 'crew', 'floor-removed'] for t in [.04, .18, .28, .36]}
    assert set(cases) == expected_cases
    for (phase, work, kind, clock), caps in cases.items():
        assert phase in range(6) and clock in [.04, .18, .28, .36]
        assert [c['moment'] for c in caps] == (['before', 'after', 'finished'] if kind in ['power', 'suspension'] else ['before', 'after'])
        assert caps[0]['key'] == f'walk-stop-phase{phase}-south'
        assert all(c['callbacks'] == 0 for c in caps)
        if kind in ['power', 'suspension']:
            assert len({tuple(c['foot']) for c in caps[:2]}) == 1
            assert caps[1]['cancelled'] and caps[1]['goal'] == ''
            assert caps[1]['choiceEntryGoal'] == '' and caps[1]['choiceEntryPathSize'] == 0
            assert caps[2]['choices'] >= 2 and caps[2]['clock'] == -1
        else:
            assert caps[1]['clock'] == -1
    groups = collections.defaultdict(list)
    records = []
    DEST.mkdir(exist_ok=True)
    for cap in report['captures']:
        key, slot = cap['key'], cap['slot']
        if key.startswith('walk-stop-phase'):
            phase = cap['gaitPhase']
            expected = ROOT / f'character/marsh-south-stop-v1/candidate-{VERSIONS[phase]}/phase-{phase}/{slot:03d}.png'
            pivot = [92, 172]
        elif key in ['idle-south', 'walk-start-south', 'walk-south']:
            folder = {'idle-south': 'character/marsh-south-idle-material-v1/candidate-01', 'walk-start-south': 'character/marsh-south-idle-material-v1/candidate-01/south-start', 'walk-south': 'character/marsh-south-walk-material-v1/candidate-02'}[key]
            expected, pivot = ROOT / folder / f'{slot:03d}.png', [92, 172]
        else:
            expected, pivot = ROOT / contract[key]['files'][slot], contract[key]['pivot']
            assert sha(expected) == contract[key]['hashes'][slot]
        source = Image.open(RUN / cap['sourceFile']).convert('RGBA')
        canonical = Image.open(expected).convert('RGBA')
        assert source.size == canonical.size and source.tobytes() == canonical.tobytes(), (key, slot)
        presentation = Image.new('RGBA', (184, 184))
        presentation.alpha_composite(source, (round(92 - pivot[0]), round(172 - pivot[1])))
        assert sum(a > 0 for a in presentation.getchannel('A').tobytes()) == sum(a > 0 for a in source.getchannel('A').tobytes())
        selected = cap['phase'] in [.18, .36] and (cap['kind'] not in ['power', 'suspension'] or cap['work'] == 'curiosity')
        if selected:
            native = Image.open(RUN / cap['file']).convert('RGB').crop((400, 200, 550, 400))
            groups[cap['gaitPhase']].append((cap, native, presentation))
        path = expected.relative_to(ROOT).as_posix()
        records.append({**cap, 'sourcePath': path, 'sourceFileSha256': sha(expected), 'capturedSourceSha256': sha(RUN / cap['sourceFile']), 'nativeSha256': sha(RUN / cap['file']), 'sourcePivot': pivot, 'visualBoardSelected': selected, 'sourceIncludedInPrelaunchFreeze': path in before})
    previews = []
    for phase in range(6):
        entries = groups[phase]
        assert len(entries) == 44
        rows = (len(entries) + 7) // 8
        native = Image.new('RGB', (1200, rows * 236), '#293b40')
        source = Image.new('RGB', (1472, rows * 220), '#293b40')
        nd, sd = ImageDraw.Draw(native), ImageDraw.Draw(source)
        for index, (cap, shot, pose) in enumerate(entries):
            for board, draw, panel, width, height in [(native, nd, shot, 150, 236), (source, sd, pose, 184, 220)]:
                x, y = index % 8 * width, index // 8 * height
                board.paste(panel, (x, y + 36), panel if panel.mode == 'RGBA' else None)
                draw.text((x + 2, y + 2), f"{cap['kind']} {cap['moment']}", fill='white')
                draw.text((x + 2, y + 18), f"{cap['phase']:.2f}s #{cap['slot']} {cap['goal']}", fill='white')
        nf, sf = f'phase-{phase}-native.png', f'phase-{phase}-source.png'
        native.save(DEST / nf); source.save(DEST / sf)
        previews.append({'phase': phase, 'nativeBoard': nf, 'sourceBoard': sf, 'captures': len(entries)})
    evidence = {**report, 'captures': records, 'targetedInputs': before, 'targetedInputsAfter': after, 'changedDiskInputs': changed, 'targetedDiskInputsStable': len(before) - len(changed), 'loadedRendererSha256': renderer, 'loadedRendererMatchesFrozen': True, 'ownerNonLogFiles': len(owner), 'ownerUnchanged': True, 'sourcePairsVerified': len(records), 'visualBoardPairs': 264, 'previews': previews, 'normalAdmission': False, 'publisherSha256': sha(Path(__file__)), 'nativeLogSha256': sha(RUN / 'native.log'), 'visualReview': 'Pending six representative source/native board pairs. Boards cover curiosity power/suspension and every hazard at .18/.36s; all384cases/960pairs retained and source-verified. No full wet visibility or full escape/recharge/injury/death clip acceptance.', 'inputFreezeScope': f'{len(before)} targeted source/controller/runtime/fixture inputs, including prior takeover source banks and runtime contract. Any additional takeover sources checked against that contract and captured RGBA at publication; explicit per-record inclusion flag. Not recursive world dependency inventory.'}
    (DEST / 'verification.json').write_text(json.dumps(evidence, indent=2) + '\n', encoding='utf-8')
    html = '<!doctype html><meta charset="utf-8"><title>Marsh six South stop interruption branches</title><style>body{background:#17282c;color:#e4e7dd;font:18px system-ui;max-width:1500px;margin:30px auto}img{max-width:100%;image-rendering:pixelated}</style><h1>Six South stops: actual interruption boundaries</h1><p>' + str(report['checks']) + 'checks/384cases/960 exact source-native pairs,0failures.264 representative visual pairs across all six branches.</p><p>' + report['scope'] + '</p><p>' + evidence['inputFreezeScope'] + '</p><p>' + str(len(owner)) + ' owner files unchanged; loaded renderer matches frozen bytes.</p>'
    for p in previews:
        html += f'<h2>Phase{p["phase"]}</h2><img src="{p["nativeBoard"]}"><img src="{p["sourceBoard"]}">'
    html += '<p>' + evidence['visualReview'] + '</p><a href="verification.json">Bound evidence</a>'
    (DEST / 'index.html').write_text(html, encoding='utf-8')
    print(report['checks'], 'checks;384cases;960 exact pairs;264 board pairs;', len(owner), 'owner files unchanged')

if __name__ == '__main__':
    main()
