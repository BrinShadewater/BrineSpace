"""Package reviewed east/west ground motion without changing frozen walk packs."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]


def build_west():
    source = ROOT / 'character/marsh-motion-polish-v1'
    runtime = ROOT / 'character/marsh-v2'
    output = runtime / 'supplemental/ground-west'
    output.mkdir(parents=True, exist_ok=True)
    states, hashes, inputs = [], {}, {}
    for action in ('start', 'stop', 'step'):
        folder = source / ('review/short-step-west-candidate-03' if action == 'step' else f'review/{action}-west-video-candidate-01')
        recipe_path = source / ('short-step-west-candidate-recipe.json' if action == 'step' else f'{action}-west-candidate-recipe.json')
        recipe = json.loads(recipe_path.read_text())
        manifest_path = folder / 'trial-manifest.json'
        manifest = json.loads(manifest_path.read_text())
        assert manifest['frameWidth'] == manifest['frameHeight'] == 256
        assert manifest['pivot'] == [128,224] and manifest['standingHeight'] == 148
        inputs[action] = dict(recipe=recipe_path.relative_to(ROOT).as_posix(),
                             recipeSha256=hashlib.sha256(recipe_path.read_bytes()).hexdigest(),
                             source=recipe['source'], sourceSha256=hashlib.sha256((ROOT/recipe['source']).read_bytes()).hexdigest(),
                             selectionManifest=manifest_path.relative_to(ROOT).as_posix(),
                             selectionManifestSha256=hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
                             extractionDurationsMs=recipe['durations'], selectedDurationsMs=manifest['states'][0]['frameDurationsMs'])
        state = manifest['states'][0]
        count = 7 if action == 'step' else 4
        assert state['id'] == f'walk-{action}-west' and state['loop'] is False
        assert state['frameDurationsMs'] == [120 if action == 'step' else 100] * count
        state.update(facings=['west']*count, waterKinds=['walk']*count, waterPoses=[False]*count, depthOffsets=[0.0]*count)
        for name in state['frameFiles']:
            shutil.copyfile(folder / name, output / name)
            hashes[name] = hashlib.sha256((output / name).read_bytes()).hexdigest()
        states.append(state)
    (output / 'manifest.json').write_text(json.dumps(dict(frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,states=states),indent=2)+'\n')
    (output / 'provenance.json').write_text(json.dumps(dict(source=source.relative_to(ROOT).as_posix(),sha256=hashes,inputs=inputs,scope='West dry empty-goal starts/stops and five-to-seven-unit short steps'),indent=2)+'\n')
    catalog_path=runtime/'catalog.json';catalog=json.loads(catalog_path.read_text())
    relative='supplemental/ground-west/manifest.json'
    if relative not in catalog['body']:catalog['body'].append(relative)
    catalog_path.write_text(json.dumps(catalog,indent=2)+'\n')
    return {'states':len(states),'frames':sum(len(s['frameFiles']) for s in states)}


def build():
    source = ROOT / 'character/marsh-motion-polish-v1'
    runtime = ROOT / 'character/marsh-v2'
    output = runtime / 'supplemental/ground-east'
    output.mkdir(parents=True, exist_ok=True)
    states, provenance = [], {}
    for action in ('start', 'stop', 'step'):
        recipe_path = source / ('short-step-east-root-recipe.json' if action == 'step' else f'{action}-east-candidate-recipe.json')
        recipe = json.loads(recipe_path.read_text())
        folder = source / ('review/short-step-east-root-candidate-02' if action == 'step' else f'review/{action}-east-video-candidate-01')
        manifest = json.loads((folder / 'trial-manifest.json').read_text())
        assert manifest['pivot'] == [128, 224] and manifest['standingHeight'] == 148
        state = manifest['states'][0]
        assert state['id'] == f'walk-{action}-east'
        count = 7 if action == 'step' else 4
        assert state['frameDurationsMs'] == [120 if action == 'step' else 100] * count and state['loop'] is False
        state.update(facings=['east'] * count, waterKinds=['walk'] * count,
                     waterPoses=[False] * count, depthOffsets=[0.0] * count)
        for name in state['frameFiles']:
            shutil.copyfile(folder / name, output / name)
            provenance[name] = hashlib.sha256((output / name).read_bytes()).hexdigest()
        states.append(state)
        provenance[recipe_path.relative_to(ROOT).as_posix()] = hashlib.sha256(recipe_path.read_bytes()).hexdigest()
    pack = {'frameWidth': 256, 'frameHeight': 256, 'pivot': [128, 224],
            'standingHeight': 148, 'states': states}
    (output / 'manifest.json').write_text(json.dumps(pack, indent=2) + '\n')
    (output / 'provenance.json').write_text(json.dumps({
        'source': source.relative_to(ROOT).as_posix(), 'sha256': provenance,
        'scope': 'Marsh dry east start, empty-goal stop and 3.5-4.5-unit short step; other directions are not authored.'
    }, indent=2) + '\n')
    catalog_path = runtime / 'catalog.json'
    catalog = json.loads(catalog_path.read_text())
    relative = (output / 'manifest.json').relative_to(runtime).as_posix()
    if relative not in catalog['body']:
        catalog['body'].append(relative)
    catalog_path.write_text(json.dumps(catalog, indent=2) + '\n')
    west = build_west()
    return {'states': len(states)+west['states'], 'frames': sum(len(s['frameFiles']) for s in states)+west['frames']}


if __name__ == '__main__':
    print(json.dumps(build()))
