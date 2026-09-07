"""Validate packaged pixels and source provenance, not artistic acceptance."""
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parent
failures = []
clips = []
for manifest_path in sorted((ROOT/'pilot').glob('*/manifest.json')):
    manifest = json.loads(manifest_path.read_text())
    sources_path = manifest_path.with_name('sources.json')
    if sources_path.exists():
        for evidence in json.loads(sources_path.read_text()):
            if hashlib.sha256((ROOT/evidence['source']).read_bytes()).hexdigest() != evidence['sha256']:
                failures.append(f'{manifest_path.parent.name}: stale selected pose source')
    contract_path = manifest_path.with_name('contract.json')
    if contract_path.exists():
        contract = json.loads(contract_path.read_text())
        if 'source' in contract:
            source = ROOT / contract['source']
            if hashlib.sha256(source.read_bytes()).hexdigest() != contract['sourceSha256']:
                failures.append(f'{manifest_path.parent.name}: stale source')
    for state in manifest['states']:
        bounds = []
        hashes = []
        if len(state['frameFiles']) != len(state['frameDurationsMs']):
            failures.append(f'{state["id"]}: timing count mismatch')
        for relative in state['frameFiles']:
            path = manifest_path.parent / relative
            im = Image.open(path).convert('RGBA')
            box = im.getbbox()
            size = (manifest['frameWidth'], manifest['frameHeight'])
            if im.size != size or box is None or min(box[:2]) < 1 or box[2] >= size[0] or box[3] >= size[1]:
                failures.append(f'{path}: empty, wrong size or touching edge')
            if not set(im.getchannel('A').tobytes()).issubset({0,255}):
                failures.append(f'{path}: nonbinary alpha')
            bounds.append(box)
            hashes.append(hashlib.sha256(path.read_bytes()).hexdigest())
        clips.append({'clip':manifest_path.parent.name,'state':state['id'],
                      'frames':len(hashes),'uniqueFiles':len(set(hashes)),
                      'bounds':bounds,'pixelSha256':hashes})
fittings = []
for manifest_path in sorted((ROOT/'equipment/fitting').glob('*/manifest.json')):
    actor, clip = manifest_path.parent.name.split('-', 1)
    registration_path = manifest_path.parent.parent / (clip + '-registration.json')
    if not registration_path.exists():
        failures.append(f'{actor}-{clip}: missing fitting provenance')
        continue
    registration = json.loads(registration_path.read_text())
    view = 'front' if clip == 'tread-south' else 'east'
    if clip == 'tread-north': view = 'north'
    view = registration.get('overlayView', view)
    overlay_path = ROOT/'equipment'/view/'overlay.png'
    if hashlib.sha256(overlay_path.read_bytes()).hexdigest() != registration['overlaySha256']:
        failures.append(f'{actor}-{clip}: stale helmet overlay')
    base_dir = ROOT/'pilot'/f'{actor}-{clip}'
    base = json.loads((base_dir/'manifest.json').read_text())
    fitted = json.loads(manifest_path.read_text())
    if base['states'] != fitted['states'] or base['pivot'] != fitted['pivot']:
        failures.append(f'{actor}-{clip}: equipment timing, frames or pivot mismatch')
    evidence = registration['characters'][actor]
    files = base['states'][0]['frameFiles']
    if [hashlib.sha256((base_dir/f).read_bytes()).hexdigest() for f in files] != evidence['sourceFrameSha256']:
        failures.append(f'{actor}-{clip}: stale body fitting')
    overlay = Image.open(overlay_path).convert('RGBA')
    for index, relative in enumerate(files):
        expected = Image.open(base_dir/relative).convert('RGBA')
        positions = evidence['overlayTopLeft']
        position = positions[index] if isinstance(positions[0], list) else positions
        foreground = [(rect, expected.crop(tuple(rect))) for rect in evidence.get('foregroundRects', [[] for _ in files])[index]]
        rotation = evidence.get('overlayRotationDegrees', [0]*len(files))[index]
        frame_overlay = overlay.rotate(rotation, resample=Image.Resampling.NEAREST, expand=True)
        expected.alpha_composite(frame_overlay, tuple(position))
        for rect, limb in foreground:
            expected.alpha_composite(limb, tuple(rect[:2]))
        actual = Image.open(manifest_path.parent/relative).convert('RGBA')
        if actual.size != expected.size or actual.tobytes() != expected.tobytes():
            failures.append(f'{actor}-{clip}/{relative}: fitting differs from registered composition')
    fittings.append({'clip':actor+'-'+clip,'frames':len(files)})
dry_fittings = []
crew = {'bill':'major-bill-v2','veld':'dr-veld-v1','branforth':'chief-engineer-branforth-v1'}
for path in sorted((ROOT/'equipment/dry').glob('*/manifest.json')):
    actor, clip = path.parent.name.split('-', 1)
    fitted = json.loads(path.read_text())
    registration = json.loads(path.with_name('registration.json').read_text())
    source_path = ROOT.parent/crew[actor]/'final/manifest.json'
    source = json.loads(source_path.read_text())
    original = next(s for s in source['states'] if s['id'] == clip)
    state = fitted['states'][0]
    if {k:v for k,v in state.items() if k != 'frameFiles'} != {k:v for k,v in original.items() if k != 'frameFiles'} or fitted['pivot'] != source['pivot']:
        failures.append(f'{actor}-{clip}: dry equipment contract mismatch')
    overlay_path = ROOT/registration['overlay']
    if hashlib.sha256(overlay_path.read_bytes()).hexdigest() != registration['overlaySha256']:
        failures.append(f'{actor}-{clip}: stale dry overlay')
    overlay = Image.open(overlay_path).convert('RGBA')
    assert len(state['frameFiles']) == len(original['frameFiles']) == len(registration['frames'])
    for relative, original_relative, evidence in zip(state['frameFiles'], original['frameFiles'], registration['frames']):
        body_path = ROOT.parent/evidence['source']
        if body_path.resolve() != (source_path.parent/original_relative).resolve() or hashlib.sha256(body_path.read_bytes()).hexdigest() != evidence['sha256']:
            failures.append(f'{actor}-{clip}/{relative}: stale dry body')
        expected = Image.open(body_path).convert('RGBA')
        expected.alpha_composite(overlay, tuple(evidence['overlayTopLeft']))
        actual = Image.open(path.parent/relative).convert('RGBA')
        if actual.size != expected.size or actual.tobytes() != expected.tobytes():
            failures.append(f'{actor}-{clip}/{relative}: dry composition mismatch')
    dry_fittings.append({'clip':actor+'-'+clip,'frames':len(state['frameFiles'])})
report = {'scope':'Packaged pixel geometry and source/fitting provenance only; no visual or runtime acceptance',
          'clips':clips,'fittings':fittings,'dryFittings':dry_fittings,'failures':failures}
(ROOT/'pilot/pixel-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'{len(clips)} clips checked; {len(failures)} failures')
for failure in failures: print(failure)
raise SystemExit(bool(failures))
