"""Read-only active-art preflight. This does not certify motion or a packaged EXE.

Run with the project's Python. Writes output/character-closeout/bindings.json.
"""
from pathlib import Path
import hashlib,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]

def audit():
    registry=json.loads((ROOT/'character/ACTIVE_ASSETS.json').read_text())
    errors=[];packs={};portraits={}
    for entry in registry['bindings']:
        if entry['contains'] not in (ROOT/entry['script']).read_text(encoding='utf-8'):
            errors.append('Missing runtime binding: '+entry['script']+' -> '+entry['contains'])
    for group in registry['animationRoots']:
        for name in group['packs']:
            path=ROOT/group['root']/name/'manifest.json'
            try:
                manifest=json.loads(path.read_text());digest=hashlib.sha256(path.read_bytes());count=0;ids=set()
                for state in manifest['states']:
                    if state['id'] in ids:raise ValueError('Duplicate state '+state['id'])
                    ids.add(state['id'])
                    if len(state['frameFiles'])!=len(state['frameDurationsMs']) or not state['frameFiles']:raise ValueError('Timing mismatch '+state['id'])
                    if any(v<=0 for v in state['frameDurationsMs']):raise ValueError('Nonpositive timing')
                    for relative in state['frameFiles']:
                        frame=(path.parent/relative).resolve()
                        if not frame.is_relative_to(ROOT):raise ValueError('Frame outside project')
                        data=frame.read_bytes()
                        if not data.startswith(b'\x89PNG\r\n\x1a\n'):raise ValueError('Missing PNG bytes / possible LFS pointer '+str(frame))
                        digest.update(data)
                        with Image.open(frame) as im:
                            if im.size!=(manifest['frameWidth'],manifest['frameHeight']):raise ValueError('Frame dimensions '+relative)
                            if set(im.convert('RGBA').getchannel('A').tobytes())-{0,255}:raise ValueError('Soft alpha '+relative)
                        count+=1
                packs[str(path.relative_to(ROOT))]={'clips':len(ids),'frameReferences':count,'contentSha256':digest.hexdigest()}
            except (OSError,ValueError,KeyError) as exc:errors.append(str(path.relative_to(ROOT))+': '+str(exc))
    for name,relative in registry['portraits'].items():
        try:
            path=ROOT/relative
            with Image.open(path) as im:im.verify()
            portraits[name]={'path':relative,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
        except (OSError,ValueError) as exc:errors.append(relative+': '+str(exc))
    for relative in registry['reviews']:
        if not (ROOT/relative).exists():errors.append('Missing review '+relative)
    result={'errors':errors,'packs':packs,'portraits':portraits,'scope':'Asset integrity and declared source bindings only; native behavior and visual evidence are in the dated handoff.'}
    out=ROOT/'output/character-closeout';out.mkdir(parents=True,exist_ok=True)
    (out/'bindings.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({'errors':errors,'packs':len(packs),'clips':sum(p['clips'] for p in packs.values()),'frameReferences':sum(p['frameReferences'] for p in packs.values()),'portraits':len(portraits)}))
    return bool(errors)

if __name__=='__main__':raise SystemExit(audit())
