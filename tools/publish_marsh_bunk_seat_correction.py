"""Retain before/after native seat evidence; unchanged whole art, corrected contact."""
from pathlib import Path
import json
import hashlib
import shutil
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
O = ROOT / 'character/marsh-bunk-seat-correction-2026-10-03'
O.mkdir(exist_ok=True)
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
runs = {}
for label, folder, checks in [('before', 'bunk-seat-probe-2026-10-03', 112),
                              ('after', 'bunk-seat-corrected-2026-10-03', 117)]:
    a = ROOT / 'output/marsh-animation-audit' / folder
    assert read(a / 'owner-before.json') == read(a / 'owner-after.json')
    assert read(a / 'inputs-before.json') == read(a / 'inputs-after.json')
    assert (a / 'native-exit.txt').read_text().strip() == '0'
    log = (a / 'native.log').read_text()
    assert 'ERROR:' not in log and 'WARNING:' not in log and f'CONTACT CHECKS: {checks}' in log
    geometry = read(a / 'geometry.json')
    runs[label] = {'geometry': geometry, 'checks': checks, 'failures': 0,
                   'ownerFilesUnchanged': len(read(a / 'owner-before.json')),
                   'stableBoundedInputs': len(read(a / 'inputs-before.json')),
                   'fullCaptures': []}
    for stamp in [0, 200, 550, 800, 1100, 1400, 1700]:
        p = a / 'captures' / f'restore-bare-{stamp:04}.png'
        dest = O / f'{label}-{stamp:04}.png'
        shutil.copy2(p, dest)
        runs[label]['fullCaptures'].append({'path': dest.relative_to(ROOT).as_posix(), 'sha256': sha(dest)})
assert runs['before']['geometry']['belowMattressWorldUnits'] > 12
assert abs(runs['after']['geometry']['belowMattressWorldUnits']) < .00001
boards = []
stamps = [0, 200, 550, 800, 1100, 1400, 1700]
for page, start in enumerate([0, 4]):
    group = stamps[start:start+4]
    board = Image.new('RGB', (360*len(group), 780), '#293b40')
    draw = ImageDraw.Draw(board)
    for row, label in enumerate(['before', 'after']):
        for col, stamp in enumerate(group):
            im = Image.open(O / f'{label}-{stamp:04}.png').convert('RGB')
            board.paste(im.crop((310,390,490,570)).resize((360,360),Image.Resampling.NEAREST), (col*360,row*390+30))
            draw.text((col*360+4,row*390+5),f'{label} / {stamp}ms / restored',fill='white')
    p = O / f'contact-before-after-{page:02}.png'
    board.save(p)
    boards.append({'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'actuallyInspected':False})
report = {'runs':runs,'boards':boards,'propArtwork':{'path':'assets/station-props-v2/sp-crew_hab-3.png','sha256':sha(ROOT/'assets/station-props-v2/sp-crew_hab-3.png')},
          'scope':'Actual normalq3 bunk chooser/arrival, seven full disk restores per run, pause/interruption/completion/lowbattery/invalid saves. New offset derived from lower mattress source row239 of334 and prop size, saved per action; old missing offset defaults16. Sleeping endpoint and authored source pixels unchanged.',
          'probeSourceHashesRecordedAfterRun':{p.relative_to(ROOT).as_posix():sha(p) for p in [ROOT/'tools/probe_marsh_bunk_seat.gd',ROOT/'tools/review_marsh_bunk_seat_corrected.gd']},
          'limits':'497 bounded inputs stable per interval; probe source hashes separately retained, not added retroactively to before fingerprints. Native restored poses, not continuous playback/all rotations/owner layouts/titleContinue/full-set acceptance.',
          'fullGoalComplete':False}
(O/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print('Bunk support gap12.007 world units -> <0.00001; before112/after117 checks,14 native captures retained.')
