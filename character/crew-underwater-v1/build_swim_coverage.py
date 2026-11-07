"""Inventory active swim packs without treating packaging as visual acceptance."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
rows=[]
for actor in ['bill','veld','branforth']:
    for direction in ['east','west','south','north']:
        version='v3' if actor=='branforth' and direction=='north' else 'v2'
        retained=actor=='veld' and direction=='north'
        body=ROOT/('pilot/veld-swim-north' if retained else f'revisions/{actor}-swim-{direction}-{version}')
        helmet=ROOT/('equipment/fitting/veld-swim-north' if retained else f'revisions/{actor}-swim-{direction}-{version}/helmet')
        m=json.loads((body/'manifest.json').read_text(encoding='utf-8'))
        h=json.loads((helmet/'manifest.json').read_text(encoding='utf-8'))
        for key in ['states','pivot','frameWidth','frameHeight']: assert m[key]==h[key]
        sources={}
        for pack,manifest in [(body,m),(helmet,h)]:
            for path in [pack/'manifest.json']+[pack/f for f in manifest['states'][0]['frameFiles']]:
                sources[path.relative_to(ROOT).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append({'actor':actor,'direction':direction,'selection':'retained pilot' if retained else 'provisional revision','body':body.relative_to(ROOT).as_posix(),'helmet':helmet.relative_to(ROOT).as_posix(),'frames':len(m['states'][0]['frameFiles']),'canvas':[m['frameWidth'],m['frameHeight']],'pivot':m['pivot'],'sourceSha256':sources,'continuousVisualAcceptance':False})
report={'scope':'Current swim pack inventory; verify consumer selection and native evidence separately','rows':rows}
(ROOT/'revisions/current-swim-coverage.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(f'{len(rows)} directional packs inventoried with body/equipment hashes')
