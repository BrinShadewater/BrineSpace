"""Freeze whole correction for physical case hardware and endpoint volume."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'character/marsh-water-transition-material-v1/sources'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((S/'pickup-east-01.request.json').read_text())
refs=[ROOT/q['path'] for q in r['orderedReferences']]+[S/'pickup-east-01.raw.png']
prompt=(S/'pickup-east-01.prompt.txt').read_text()+'''
WHOLE CORRECTION: Reference5 is the rejected first study, motion progression ONLY, never its wrong case hardware/body width. Reauthor all five whole figures organically. Preserve exact slim32x147 profile neutral, not35wide. Four transition figures FIRST, upright empty neutral LAST, five separated figures only. Own RIGHT profile remains fixed, including anatomicalRIGHT silver temple implant.
The SAME rigid case is side-facing throughout, EXACT endpoint dark divided side panel and ONE ivory outerRIGHT edge latch visible, even crouching. Do NOT show two frontal latches in pose1, do not turn case front toward viewer independently while body stays profile. Both hands securely grip existing side case. Same physical case width/height across lift, naturally pitch only. Last prone pose must match endpoint adult volume and projected lengthabout146units (NOT162), heightabout70, head about21-22high. Prior figure4 stretches legs/body; restore proper physical lengths through whole natural bent-knee articulation and same35degree water camera. Do not fit individual poses or shrink head; use one147 upright ruler for all.
Keep exact body material muted ivory/greyed sage/slate, narrow adult waist/shoulders/boots, do not add accessories or saturated edge speckles. New whole drawings only, no limb/head/prop patches or recolour.'''
p=S/'pickup-east-02.prompt.txt';p.write_text(prompt,encoding='utf-8')
r.update(status='frozen before whole correction',promptSha256=sha(p),orderedReferences=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in refs])
for k in ['generationId','originalGeneratedPath','rawSha256']:r.pop(k,None)
(S/'pickup-east-02.request.json').write_text(json.dumps(r,indent=2)+'\n')
print('Whole East pickup02 correction frozen, five observed refs.')
