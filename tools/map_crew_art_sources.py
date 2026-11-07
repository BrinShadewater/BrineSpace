"""Match frozen native body frames to preserved pack pixels, allowing padding.

Unmatched and ambiguous pixels are reported rather than guessed or regenerated.
"""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def signature(path):
    with Image.open(path) as source:
        image = source.convert('RGBA')
    box = image.getbbox()
    if box is None:
        raise ValueError('Empty source: '+str(path))
    pixels = np.array(image.crop(box))
    pixels[pixels[:,:,3]==0] = 0
    return (pixels.shape, hashlib.sha256(pixels.tobytes()).hexdigest()), box


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, default=ROOT/'output/crew-replacement-2026-09-12/runtime-baseline-v2')
    args = parser.parse_args()
    base = args.baseline.resolve()
    roots = ['dr-veld-v1','chief-engineer-branforth-v1','crew-construction-v1',
             'crew-actions-v1','crew-life-v1','crew-underwater-v1','marsh-v1',
             'animation-expansion-v5','sprite-polish-v4']
    lookup = {}
    records = {}
    manifests = {}
    for root in roots:
        for path in sorted((ROOT/'character'/root).rglob('*manifest.json')):
            data = json.loads(path.read_text(encoding='utf-8'))
            for state in data.get('states',[]):
                for rel in state.get('frameFiles',[]):
                    frame = (path.parent/rel).resolve()
                    key = frame.relative_to(ROOT).as_posix()
                    if key in records:
                        continue
                    sig, box = signature(frame)
                    manifest = path.relative_to(ROOT).as_posix()
                    records[key] = {'manifest':manifest,'sha256':hashlib.sha256(frame.read_bytes()).hexdigest(),'bounds':list(box),'pivot':data.get('pivot',[46,86])}
                    manifests[manifest] = hashlib.sha256(path.read_bytes()).hexdigest()
                    lookup.setdefault(sig,[]).append(key)
    summary = {}
    for actor in ['veld','branforth','marsh']:
        inventory = json.loads((base/(actor+'.json')).read_text())
        unmatched = []
        used = set()
        for state in inventory['states']:
            for frame in state['frames']:
                sig, box = signature(base/frame['file'])
                candidates = [key for key in lookup.get(sig,[]) if actor in key]
                if not candidates:
                    # Runtime joins may clip a wide source into their fixed canvas.
                    # Reproduce that exact operation; never mistake lost edges for new art.
                    for key, record in records.items():
                        if actor not in key or 'swim-north' not in key:
                            continue
                        offset = [int(a-b) for a,b in zip(frame['meta']['crew_pivot'],record['pivot'])]
                        canvas = Image.new('RGBA',tuple(frame['size']))
                        with Image.open(ROOT/key) as original:
                            canvas.alpha_composite(original.convert('RGBA'),tuple(offset))
                        pixels = np.array(canvas.crop(canvas.getbbox()))
                        pixels[pixels[:,:,3]==0] = 0
                        if (pixels.shape,hashlib.sha256(pixels.tobytes()).hexdigest()) == sig:
                            candidates = [key]
                            frame['sourceOffset'] = offset
                            frame['runtimeSourceClipped'] = True
                            break
                    if not candidates:
                        unmatched.append(frame['file'])
                        continue
                key = candidates[0]
                used.add(key)
                frame['sourceFrame'] = key
                frame.setdefault('sourceOffset',[box[0]-records[key]['bounds'][0],box[1]-records[key]['bounds'][1]])
                if len(candidates)>1:
                    frame['identicalSourceCandidates'] = candidates
        inventory['sourceFrames'] = {key:records[key] for key in sorted(used)}
        selected = {records[key]['manifest'] for key in used}
        inventory['sourceManifests'] = {key:manifests[key] for key in sorted(selected)}
        inventory['unmatchedBodyFrames'] = unmatched
        inventory['method'] = 'Native alpha-normalized content matching; identical candidates retained. Equipment remains native evidence and requires source fitting recipes.'
        (base/(actor+'-source-map.json')).write_text(json.dumps(inventory,indent=2)+'\n')
        summary[actor] = {'matchedBodyReferences':sum(len(row['frames']) for row in inventory['states'])-len(unmatched),'unmatchedBodyReferences':len(unmatched),'uniqueSources':len(used),'sourceManifests':len(selected)}
    (base/'source-map-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
