"""Freeze a whole-figure East loaded-swim request against current selections."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
B=ROOT/'character/marsh-loaded-swim-material-v1';S=B/'sources';S.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
def resolve(p,n):return ROOT/n.removeprefix('res://') if n.startswith('res://') else (p.parent/n).resolve()
cat=ROOT/'character/marsh-v2/catalog.json';selected={}
for n in json.loads(cat.read_text())['body']:
    p=resolve(cat,n)
    for state in json.loads(p.read_text())['states']:selected[state['id']]=(p,state)
motion=selected['swim-carry-east'];frames=[resolve(motion[0],n) for n in motion[1]['frameFiles']]
board=Image.new('RGB',(224*len(frames),232),'#293b40');d=ImageDraw.Draw(board)
for i,p in enumerate(frames):
    im=Image.open(p).convert('RGBA');board.paste(im,(224*i,24),im);d.text((224*i+4,4),'MOTION ONLY '+str(i),fill='white')
guide=S/'east-selected-motion-only.png';board.save(guide)
refs=[ROOT/'character/marsh-cargo-held-material-v1/sources/east-cargo-endpoint.png',ROOT/'character/marsh-cargo-held-material-v1/sources/east-body-primary.png',guide,ROOT/'character/marsh-motion-polish-v1/sources/east-standing-identity-01.png']
prompt='''Create a production sprite source atlas on a genuinely transparent background: five equally wide cells in ONE horizontal row, complete figures with clear empty margins, no labels, no ground shadows, no bubbles or equipment helmet.
REFERENCE ROLES: FIRST is precise rigid cargo case and own East carry endpoint authority. SECOND is PRIMARY body/face/material/proportion authority: fitted slim adult Marsh android botanist in matte ivory/sage suit, restrained dark outline, near RIGHT temple implant. THIRD shows old swimming action only; do NOT copy its bulky body, huge head, colour grade or case design. FOURTH is original East directional identity, secondary. Do not mirror. Quiet same warm ivory and sage, natural sandy short hair, small adult head, compact padded joints and narrow chest/waist, no bulky spacesuit, no extra hardware or seams.
Cells 1-4: FOUR successive whole East loaded-swimming poses of the SAME adult, body horizontal facing RIGHT, head and upper chest gently lifted as he swims forward, BOTH hands securely supporting the SAME small rigid dark rectangular carry case just in front of the upper chest, close enough for bent elbows. Case correct side inset panel and one ivory latch at its RIGHT edge, never a suitcase with handle or round bag. Keep case at approximately 34x23 units compared with the adult standing extent 147 units; its perspective may change with body but rigid size never grows. Four genuinely different leg propulsion phases: 1 near leg extended/far knee tucked, 2 near knee folds/far leg extends, 3 reverse propulsion near tucked/far extended, 4 recover toward first with knees intermediate. Both articulated legs visible, separate boots and clear knee anatomy; arms maintain connected grip throughout. Preserve consistent side-camera perspective and physical torso/head proportions. No skating walking stance: swimming body is long horizontally, slight overhead view of top surfaces only, matches reference game camera.
Cell 5: EXACT SAME character upright neutral East standing, BOTH feet flat, arms relaxed and empty hands, slim adult profile matching second reference. This is the common scale ruler for the WHOLE atlas: same camera and bone proportions in every cell, not larger than swimmers. Make this neutral visibly as narrow and fitted as the primary master; do not widen the torso or enlarge head. Use constant density/details/grade across all five figures. Swimming should use the full same adult body length, not a miniaturized swimmer. One complete figure per cell. Keep every complete silhouette strictly within its own equal cell with transparent separation; no text/grid/border/prop detachment. All artwork is newly authored whole connected poses; no cut-and-paste limbs, no mirrored opposite side, no independent body/case scaling.'''
promptpath=S/'east-loop-01.prompt.txt';promptpath.write_text(prompt,encoding='utf-8')
request={'normalAdmission':False,'fullGoalComplete':False,'status':'frozen before generation','promptSha256':sha(promptpath),'orderedReferences':[ref(p) for p in refs],'sourceFrames':[ref(p) for p in frames]+[ref(ROOT/'character/marsh-v2/frames/bare/idle-east/000.png'),ref(ROOT/'character/marsh-east-carry-material-v1/candidate-03/000.png')],'selectedMotionManifest':ref(motion[0]),'selectedMotionState':motion[1],'catalogue':ref(cat),'rules':'Five whole cells, common own-East standing neutral scale, no clipping/mirroring/body or case patches/per-pose fitting. Source then native review; not admitted.'}
(S/'east-loop-01.request.json').write_text(json.dumps(request,indent=2)+'\n')
families={}
for key,(p,state) in selected.items():
    base=key
    for f in ['east','west','north','south']:
        if base.endswith('-'+f):base=base[:-(len(f)+1)];break
    families.setdefault(base,[]).append({'state':key,'manifest':p.relative_to(ROOT).as_posix(),'slots':len(state['frameFiles'])})
(B/'current-catalogue-family-inventory.json').write_text(json.dumps({'bodyManifests':len(json.loads(cat.read_text())['body']),'states':len(selected),'slots':sum(len(s['frameFiles']) for p,s in selected.values()),'families':families,'scope':'Current ordered selection coverage, not master-match or visual acceptance.'},indent=2)+'\n')
print(json.dumps({'states':len(selected),'slots':sum(len(s['frameFiles']) for p,s in selected.values()),'chosenNext':'East loaded swim whole material/body redraw','references':[r['path'] for r in request['orderedReferences']]}))
