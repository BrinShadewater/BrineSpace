"""Freeze own East/North endpoint and body authorities for whole prone yaw poses."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-turn-material-v1';S=B/'sources';S.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
def resolve(p,n):return ROOT/n.removeprefix('res://') if n.startswith('res://') else (p.parent/n).resolve()
cat=ROOT/'character/marsh-v2/catalog.json';selected={}
for n in json.loads(cat.read_text())['body']:
    p=resolve(cat,n)
    for state in json.loads(p.read_text())['states']:selected[state['id']]=(p,state)
masters=[resolve(selected['idle-'+f][0],selected['idle-'+f][1]['frameFiles'][0]) for f in ['east','north']]
ends=[ROOT/'character/marsh-loaded-swim-material-v1/east-loop-02-unselected/000.png',ROOT/'character/marsh-loaded-swim-material-v1/north-loop-04-unselected/000.png']
for stem,paths in [('east-north-body-primary',masters),('east-north-swim-endpoints',ends)]:
    board=Image.new('RGB',(448,238),'#293b40');d=ImageDraw.Draw(board)
    for i,p in enumerate(paths):
        im=Image.open(p).convert('RGBA');board.paste(im,(224*i,25),im);d.text((224*i+4,5),['EAST / own RIGHT profile','NORTH / own BACK'][i],fill='white')
    board.save(S/(stem+'.png'))
mp,state=selected['swim-carry-turn-east-north'];oldframes=[resolve(mp,n) for n in state['frameFiles']]
board=Image.new('RGB',(224*len(oldframes),238),'#293b40');d=ImageDraw.Draw(board)
for i,p in enumerate(oldframes):
    im=Image.open(p).convert('RGBA');board.paste(im,(224*i,25),im);d.text((224*i+4,5),'OLD MOTION ONLY '+str(i),fill='white')
board.save(S/'east-north-old-motion-only.png')
refs=[S/'east-north-body-primary.png',S/'east-north-swim-endpoints.png',S/'east-north-old-motion-only.png',ROOT/'character/marsh-motion-polish-v1/sources/north-standing-identity-01.png']
prompt='''Create FOUR COMPLETE separate figures on genuine transparent background in a single horizontal row with wide transparent gutters, no labels/text/grid/scenery/shadows/bubbles: THREE prone loaded-swimming intermediate yaw poses from EAST toward NORTH, plus ONE upright North neutral scale ruler.
Reference1 PRIMARY own East/North adult body/head/proportions/quiet matte identity. Reference2 staged own East and North SWIM ENDPOINTS governs same physical body, water-plane camera and rigid case/connected grip. LEFT figure faces EAST/right; RIGHT figure faces NORTH/away. Reference3 OLD MOTION ONLY: follows the yaw path, not its bulky anatomy/head or old case. Reference4 original NORTH rear identity. Do not mirror. Muted offwhite ivory, greyed sage, slate/charcoal, sandy hair, small adult head about21units relative146standing adult. Same slim waist and modest shoulder armor, existing rear panel/harness/pouches; no added packs, glossy gold/yellow grade or giant face.
All three swimmers remain HORIZONTAL prone in water, camera about35degrees above water, torso/legs foreshorten naturally as heading rotates away. NOT upright standing/waist-carry/walking or floating upright. Both arms bent ahead of upper chest secure SAME small rigid dark case IN FRONT along heading. Head/torso/pelvis/legs/boots/case rotate together in water-plane yaw. Connected correct adult anatomy, two separate boots/legs, no pasted parts, no independent prop fitting.
Figure1 yaw22.5degrees from EAST/right toward NORTH/away: shallow REAR-RIGHT quarter, head/case lead diagonally upperRIGHT; boots trail lowerLEFT. Profile face still partly visible toward RIGHT; a narrow glimpse of back armor begins. AnatomicalRIGHT temple implant remains on correct own side if visible. Case right side inset panel and one ivory outer edge latch, in front/upperRIGHT of upper chest, small physical size unchanged from endpoint. Both hands connected.
Figure2 yaw45degrees: clear REAR-RIGHT quarter, head leads upperRIGHT, backplate and rear harness visible, face mostly turned away with only right-side ear/cheek glimpse. Torso starts naturally occluding the FORWARD case; only appropriate far-leading corner/edge around upperRIGHT may remain visible. Case MUST NOT move onto backplate or sit as a rectangular backpack across rear torso. Both hands hold it ahead, far hand hidden naturally.
Figure3 yaw67.5degrees: nearly NORTH/away, head leads mostlyUP with slightRIGHT, boots trail mostlyDOWN with slightLEFT. Rear head and back armor dominant, face/implant mostly hidden naturally; two bent elbows visible at sides, forward-held case mostly hidden beyond head/shoulders, consistent small rigid hardware, never across back. Natural knee/boot articulation in horizontal prone depth.
Three whole yaw angles clearly distinct, evenly progressing toward exact North endpoint. Maintain same physical adult/head and quiet grade throughout. Use small natural alternating trailing-leg adjustments without changing physical scale or adding a high upright knee pose. No per-pose scaling or cut-and-paste head. The same anatomy must change through real perspective, not flattened squeeze.
Figure4 SAME adult upright NORTH neutral, back toward viewer, empty relaxed hands, both flat feet. Exact width55height146 units of primary North master; common neutral ruler for all four whole figures. Keep head physical scale matching this ruler in all swimming figures. Complete bodies/case fully inside individual separated cells, no clipping. Newly author whole connected figures organically.'''
p=S/'east-north-01.prompt.txt';p.write_text(prompt,encoding='utf-8')
r={'normalAdmission':False,'fullGoalComplete':False,'status':'frozen before generation','promptSha256':sha(p),'orderedReferences':[ref(p) for p in refs],'sourceFrames':[ref(p) for p in masters+ends+oldframes],'stagedEndpoints':[ref(p) for p in ends],'selectedTurnManifest':ref(mp),'selectedTurnState':state,'neutralOccupiedTargetHeight':146,'anglesFromEast':[22.5,45,67.5],'rules':'Whole prone yaw figures, one own-North neutral146 scale; progressive forward-case occlusion, no mirroring/patches/per-pose fit. Whole turn assembly requires visual/native checks.'}
(S/'east-north-01.request.json').write_text(json.dumps(r,indent=2)+'\n');print('East-North prone three-angle whole request frozen; exact endpoint sources retained.')
