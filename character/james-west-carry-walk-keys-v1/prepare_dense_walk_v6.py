from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];crop=[80,88,176,184];keys=[0,8,12,20,28,36,44,48]
manifest=r/'character/crew-runtime-matte-v1/branforth/manifest.json';m=json.loads(manifest.read_bytes());state=next(s for s in m['states'] if s['id']=='walk-west')
assert len(state['frameFiles'])==49 and m['pivot']==[92,172]
master=r/'character/james-west-master-carry-v1/local-v3-carry-pose.png'
Image.open(master).convert('RGBA').crop(crop).resize((384,384),Image.Resampling.LANCZOS).save(p/'dense-walk-v6-standing-reference.png')
anchors={}
for i in keys:
    f=p/('walk12-case-master-v5-seam.png' if i==12 else f'walk{i:02d}-case-master-v5.png');anchors[i]=f
    Image.open(f).convert('RGBA').crop(crop).resize((384,384),Image.Resampling.LANCZOS).save(p/f'dense-walk-v6-anchor-{i:02d}.png')
phases=[]
for i in range(49):
    if i in keys:continue
    n=f'walk{i:02d}-dense-carry-v6';donor=manifest.parent/state['frameFiles'][i];im=Image.open(donor).convert('RGBA');assert im.size==(184,184)
    base=Image.new('RGBA',(256,256));base.paste(im,(36,52));base.save(p/f'{n}-original.png')
    base.crop(crop).resize((384,384),Image.Resampling.LANCZOS).save(p/f'{n}-target.png')
    left=max(k for k in keys if k<i);right=min(k for k in keys if k>i)
    prompt=f'''Edit image1 ONLY. James actual West walk phase{i} of49, original matte graphite/ochre/dull silver sprite. Fixed96x96native upper-body crop enlarged4x; all images same scale/camera/crop/world registration. Image2 is standing carrying local3 reference derived from original selected idle, provisional NOT a new owner-approved master. Images3/4 are authored carrying poses at original phases{left}/{right}, contact/rigid-case continuity guides, not replacement bodies. Raise BOTH original hanging arms into a natural steady two-handed equipment-case carry. Keep image1 own torso angle, original shoulders/backpack/chest straps and walking hips/thighs exactly; never copy reference body/legs or change head/height/camera/grade. One rigid graphite rectangular case low in front of waist toward character-facing LEFT, approximately native world x95..124,y130..152. Match same physical panel dimensions, modest depth, four original-style muted dull-silver corner latches from image2 and same low waist reach as adjacent carrying poses. No chest-high box, enlarged/undersized/squat changing box, thick cartoon outlines, chrome shine or pixel-art re-rendering. Near gloved hand wraps/supports RIGHT case edge, far glove wraps LEFT edge, both wrists connect original silver cuffs and coherent forearms. No hanging loose hand below box, floating fingers, double arm/cuff, body clipping, transparent holes or black underarm/backpack cavities. Preserve original matte material and original upper-body detail. Original anatomical-left belt meter stays at its actual HIGH attachment, naturally occluded where new carrying glove/forearm overlaps it; retain authentic visible donor portions only where not covered, never relocate full meter to lower belt or invent screen/bars/buttons/yellow fragments. Anatomical-right LONG yellow-shaft wrench stays on FAR hip in West view/body-occluded; do not draw invented near-side silver loop/ring/U/hourglass or move hardware to opposite hip. Natural graphite belt cloth behind hand; no new pouches/hardware. Return the FULL original square image1 crop with coherent carrying arms/rigid case, alpha/framing preserved. Actual phase{i} head above104and legs below169must retain original registration; no perpose scale/warping or copied gait pose.'''
    (p/f'{n}-prompt.txt').write_text(prompt+'\n',encoding='utf-8')
    refs=[p/f'{n}-target.png',p/'dense-walk-v6-standing-reference.png',p/f'dense-walk-v6-anchor-{left:02d}.png',p/f'dense-walk-v6-anchor-{right:02d}.png']
    files=[donor,manifest,master,anchors[left],anchors[right],p/f'{n}-original.png',*refs,p/f'{n}-prompt.txt',Path(__file__)]
    (p/f'{n}-inputs.json').write_text(json.dumps({'preCallSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'crop':crop,'admissionRegion':[88,104,166,169],'baseFile':f'{n}-original.png','phase':i,'adjacentPhases':[left,right],'references':[str(f) for f in refs],'scope':'Actual original chronological donor pose with authored carrying upper correction; no duplicated/nearest key fake motion. All visual/material/tool/seam/cadence acceptance pending.'},indent=2)+'\n',encoding='utf-8')
    phases.append(i)
(p/'dense-walk-v6-plan.json').write_text(json.dumps({'sourceManifest':manifest.relative_to(r).as_posix(),'sourceManifestSha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),'state':state,'originalKeys':keys,'remainingAuthoredPhases':phases,'status':'prepared_not_generated','normalChanged':False},indent=2)+'\n',encoding='utf-8')
print(f'{len(phases)}distinct original-pose targets prepared;49source chronology retained, no key repetition.')
