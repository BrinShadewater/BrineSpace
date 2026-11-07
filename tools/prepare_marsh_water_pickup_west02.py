"""Whole correction for own West swimmer extent, camera and head volume."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'character/marsh-water-transition-material-v1/sources'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((S/'pickup-west-01.request.json').read_text());refs=[ROOT/q['path'] for q in r['orderedReferences']]+[S/'pickup-west-01.raw.png']
prompt=(S/'pickup-west-01.prompt.txt').read_text()+'''
WHOLE CORRECTION: Reference5 is the first study, progression ONLY; its launch and late swimmers164/160units long differ from exact ownWest endpoint141, and neutral33x148 differs from31x147 master. Reauthor all five whole figures. Maintain ownWest natural physical camera35degrees above water and full adult proportions/head21-22units. Four transition figures FIRST, own empty neutral LAST. Keep neutral31x147 physical proportions, slim adult shoulder/waist/boots, same matte grade.
Pose3 whole launch swimmer: avoid long nearly straight diagonally stretched hips/legs; connected natural bent trailing knees/two compact boots, organic water-plane foreshortening. Projected full extent about140-145units at147upright ruler. Pose4 full prone swimmer close to EXACT ownWest endpoint141x54, same bent-knee articulation/head/body/case volume; projected extent about141-145wide and54-66high. Do not shrink individual heads or fit individual figures; the single147neutral controls all. Match anatomy/camera through new connected whole drawing, not independent scaling.
Own anatomicalLEFT near temple stays BARE in every pose. RIGHT implant hidden on far side, do not mirror East or add silver hardware on nearLEFT. Same case small divided side panel with ONE outerLEFT leading ivory edge latch, even crouch, never two frontal latches. Two connected hands grip forward case at lift/prone. Whole identity and body authored organically; no pasted parts/recolour/extra gear/yellow ivory or saturated edge speckles.'''
p=S/'pickup-west-02.prompt.txt';p.write_text(prompt,encoding='utf-8');r.update(status='frozen before whole correction',promptSha256=sha(p),orderedReferences=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in refs])
for k in ['generationId','originalGeneratedPath','rawSha256']:r.pop(k,None)
(S/'pickup-west-02.request.json').write_text(json.dumps(r,indent=2)+'\n');print('OwnWest pickup02 whole correction frozen.')
