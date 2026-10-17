from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
for name,file,old in [('early','early-v3-pose.png',10),('late','late-v2-pose.png',11)]:
    src=r/'character/james-carry-authored-turn-v1'/file
    im=Image.open(src).convert('RGBA');im.crop((96,64,160,128)).resize((512,512),Image.Resampling.NEAREST).save(p/(name+'-target.png'))
    prompt=f'''EDIT TARGET: square crop of James's head and collar in his existing carrying turn. Correct ONLY the top contour of grey hair to keep his head crown level with adjoining master poses. Current grey hair crown starts{old}/64 of the way down the square; required crown starts12/64 of the way down. Trim the excess height by making the grey hair cap slightly thinner at the TOP ONLY ({12-old}/64 of canvas height), retaining natural grey hair shape and painterly texture. Do not move/scale/rotate the whole head or copy another orientation. Keep current exact face angle, eyes/nose/moustache, ears, goggles, face proportions, collar and shoulder pixels unchanged; goggles remain at their existing height. Preserve compact master head, neutral matte grey/yellow grade. Keep exact same composition/transparent margins. No new face, bald spot, helmet, scene, labels or shadow. Genuine transparent alpha. Return one same square crop. Only tiny hair-roof contour adjustment; the body is outside this crop and must not change.'''
    (p/(name+'-prompt.txt')).write_text(prompt+'\n',encoding='utf-8')
    files=[src,p/(name+'-target.png'),p/(name+'-prompt.txt'),Path(__file__)]
    (p/(name+'-inputs.json')).write_text(json.dumps({'preCallSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'base':src.relative_to(r).as_posix(),'crop':[96,64,160,128],'admissionRegion':[110,74,141,82],'targetCrown':76,'selected':False,'scope':'Hair-roof contour only; full head height/proportions/motion still require review.'},indent=2)+'\n',encoding='utf-8')
print('Early2px/late1px hair-crown targets frozen; only31x8 native roof admission, no head/body scaling.')
