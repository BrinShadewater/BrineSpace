"""Freeze own-North authorities and old motion before whole-source generation."""
from pathlib import Path
import json, hashlib
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'character/marsh-loaded-swim-material-v1/sources'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p): return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
def resolve(p,n): return ROOT/n.removeprefix('res://') if n.startswith('res://') else (p.parent/n).resolve()
cat=ROOT/'character/marsh-v2/catalog.json'; selected={}
for n in json.loads(cat.read_text())['body']:
    p=resolve(cat,n)
    for state in json.loads(p.read_text())['states']: selected[state['id']]=(p,state)
manifest,state=selected['swim-carry-north']; frames=[resolve(manifest,n) for n in state['frameFiles']]
board=Image.new('RGB',(224*len(frames),232),'#293b40'); d=ImageDraw.Draw(board)
for i,p in enumerate(frames):
    im=Image.open(p).convert('RGBA');board.paste(im,(224*i,24),im);d.text((224*i+4,4),'MOTION ONLY '+str(i),fill='white')
guide=S/'north-selected-motion-only.png';board.save(guide)
refs=[ROOT/'character/marsh-cargo-held-material-v1/sources/north-body-primary.png',ROOT/'character/marsh-cargo-held-material-v1/sources/north-cargo-endpoint.png',guide,ROOT/'character/marsh-motion-polish-v1/sources/north-standing-identity-01.png']
prompt='''Create a production sprite atlas with genuine transparent background: FIVE separate COMPLETE figures in one horizontal row, wide empty separation, no text, grid, labels, scenery, cast shadows or bubbles. Four loaded swimmers and one upright neutral scale ruler. All depict exactly the same slim adult android botanist, own NORTH direction, moving AWAY/up the image, seen from behind at the same slightly overhead game camera.
Reference1 is PRIMARY body, rear silhouette, proportions, quiet matte ivory/greyed sage material and small sandy-haired adult head. Reference2 governs the rigid cargo case and rear carry geometry ONLY. Reference3 is OLD SWIM MOTION ONLY, not anatomy, grade or hardware authority. Reference4 is original NORTH standing directional identity. Never mirror a side or front sprite. Maintain fitted narrow adult torso/waist, complete articulated legs and compact boots, modest shoulder plates, existing rear seams only. No bulky spacesuit, backpack, added tubes, yellow/gold ivory or glossy finish. Preserve head size across ALL poses, about21-22 units high relative to standing146; upright rear neutral width55 units relative to146 height.
Figures1-4: northward horizontal swimming away/up, foreshortened organically from the rear at the original slightly overhead camera, crown/head leading above shoulders, hips below torso and two separately readable trailing legs/boots below hips. Both bent arms and hands hold the SAME small dark rigid rectangular case FORWARD in front of upper chest, AWAY from the viewer. It is partly occluded by the body from this rear view, with only naturally visible forward edge/corners. Do NOT strap it across the back or paint a rectangular backpack on the rear torso. Do not expose a full front-view case through the torso. Same rigid case dimensions and connected two-hand grip through the loop. Respect natural foreshortening; do not shorten the physical adult to a child or inflate the head.
Four distinct successive alternating propulsion phases: 1 left leg extended/trailing, right knee folded; 2 left knee starts folding as right starts extension; 3 left knee folded/right extended; 4 left begins extension/right begins folding, clearly different intermediate angle from2. Legs remain connected at hips with correct knees and boots, separate near/far forms without extra limbs. Keep upper-body heading, case grip, camera, scale and material consistent. No swimming figures copied from one pose or per-pose rescaling.
Figure5: same adult upright NORTH neutral, back toward viewer, empty relaxed hands, both feet flat; exact proportions/grade/rear silhouette of primary reference. This whole neutral is the single common scale ruler for all five figures, not independently scaled. Entire figures and any visible case parts strictly inside their separate cells. Author whole connected organic drawings, no pasted heads/limbs, no independent prop fit or recolouring patches. Transparent empty space between all figures.'''
p=S/'north-loop-01.prompt.txt';p.write_text(prompt,encoding='utf-8')
r={'normalAdmission':False,'fullGoalComplete':False,'status':'frozen before generation','promptSha256':sha(p),'orderedReferences':[ref(p) for p in refs],'sourceFrames':[ref(p) for p in frames]+[ref(ROOT/'character/marsh-v2/frames/bare/idle-north/000.png')],'selectedMotionManifest':ref(manifest),'selectedMotionState':state,'catalogue':ref(cat),'rules':'Whole figures, own-North neutral146 scale, no mirrors/patches/recolour/per-pose fit; forward-held case must not become backpack. All joins and world root provisional.'}
(S/'north-loop-01.request.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'references':[r['path'] for r in r['orderedReferences']],'slots':len(frames)}))
