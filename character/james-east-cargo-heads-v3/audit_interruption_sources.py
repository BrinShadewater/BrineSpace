"""Bind native diagnostic pixels to the current ordered James source bank."""
from pathlib import Path
import hashlib, json, re
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[2]
out = Path(__file__).resolve().parent
loader = (root / 'scripts/grid_canvas.gd').read_text()
branch = loader.split('elif actor == "branforth":', 1)[1]
branch = branch.split('\n\t\tset(actor+', 1)[0]
banks = {'bare': {}, 'helmet': {}}
profiles = {'bare': {}, 'helmet': {}}
inputs = {}
for kind, rel in re.findall(r'player\.(load_manifest|load_equipment_manifest)\([^\n]*?"res://([^"\n]+\.json)"', branch):
    manifest = root / rel
    inputs[rel] = hashlib.sha256(manifest.read_bytes()).hexdigest()
    pack = json.loads(manifest.read_bytes())
    mode = 'bare' if kind == 'load_manifest' else 'helmet'
    for state in pack['states']:
        files = state.get('frameFiles', [])
        if files:
            banks[mode][state['id']] = [(manifest.parent / p).resolve() for p in files]
            profiles[mode][state['id']] = {'pivot': pack.get('pivot',[46,86]), 'standingHeight': pack.get('standingHeight',74)}

def pixels(path):
    im = Image.open(path).convert('RGBA')
    return im.size, hashlib.sha256(im.tobytes()).hexdigest()

evidence = json.loads((out / 'interruption-probe-evidence.json').read_bytes())
results = []
for case in evidence['results']:
    mode = case['mode']
    captures = []
    for source in case['sources']:
        signature = pixels(out / source)
        matches = []
        for key, paths in banks[mode].items():
            if not key.startswith(('pickup-', 'carry-', 'unload-', 'idle-')):
                continue
            for index, path in enumerate(paths):
                if pixels(path) == signature:
                    matches.append({'state': key, 'index': index, 'path': path.relative_to(root).as_posix()})
        captures.append({'capture': source, 'matches': matches})
    assert all(c['matches'] for c in captures), (mode, case['target'])
    # Action draws do not advance the locomotion transition cache. During North
    # unloading that cache still says West; use the actual bound source pixels.
    expected = {'workshop_pickup': 'pickup-', 'workshop_carry': 'carry-', 'workshop_unload': 'unload-'}[case['target']]
    bound = next(m for m in captures[0]['matches'] if m['state'].startswith(expected))
    facing = case['beforeMotion']['direction'] if case['target'] == 'workshop_carry' else bound['state'].rsplit('-', 1)[1]
    assert facing in ('north', 'south', 'east', 'west')
    idle = banks[mode]['idle-' + facing][0]
    pickup = banks[mode].get('pickup-' + facing, [])
    unload = banks[mode].get('unload-' + facing, [])
    results.append({'mode': mode, 'stage': case['target'], 'captures': captures,
                    'endpointFacing': facing,
                    'locomotionCacheFacing': case['beforeMotion']['direction'],
                    'displayedSourceAliases': captures[0]['matches'],
                    'pickupFirstEqualsIdle': bool(pickup) and pixels(pickup[0]) == pixels(idle),
                    'unloadLastEqualsIdle': bool(unload) and pixels(unload[-1]) == pixels(idle),
                    'pickupUnloadExactReversal': bool(pickup) and len(pickup) == len(unload) and all(pixels(a) == pixels(b) for a,b in zip(pickup, reversed(unload)))})
report = {'results': results, 'loaderSha256': hashlib.sha256(loader.encode()).hexdigest(),
          'manifestHashesAtAudit': inputs,
          'scope': 'Current ordered source resolution and exact full-RGBA capture binding. Endpoint equality is source evidence only; no return motion, crate-floor disposition or runtime acceptance.'}
board = Image.new('RGB', (1560, 4 * 290), '#303b40')
draw = ImageDraw.Draw(board)
endpoints = []
for row, facing in enumerate(('east','west','north','south')):
    for gear, mode in enumerate(('bare','helmet')):
        for column, (label,key,index) in enumerate((('pickup start','pickup-'+facing,0),('unload end','unload-'+facing,-1),('selected idle','idle-'+facing,0))):
            path = banks[mode][key][index]
            im = Image.open(path).convert('RGBA')
            profile = profiles[mode][key]
            assert profile['standingHeight'] == 148, profile
            pivot = profile['pivot']
            bbox = im.getchannel('A').point(lambda a: 255 if a >= 128 else 0).getbbox()
            x = gear * 780 + column * 260
            y = row * 290
            draw.text((x+4,y+4),f'{mode} {facing}: {label}',fill='white')
            draw.text((x+4,y+18),f'opaque bounds {bbox}',fill='white')
            # Preserve source density; align each pack's actual foot pivot.
            board.paste(im,(x+128-int(pivot[0]),y+33+224-int(pivot[1])),im)
            draw.line((x,y+33+224,x+255,y+33+224),fill='#929d9f')
            endpoints.append({'mode':mode,'facing':facing,'label':label,'path':path.relative_to(root).as_posix(),'opaqueAlpha128Bounds':bbox,'profile':profile})
board.save(out/'cargo-standing-endpoint-review.png')
report['endpointRulerPresentations'] = endpoints
(out / 'interruption-source-audit.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps([{k:v for k,v in r.items() if k != 'captures'} for r in results], indent=2))
