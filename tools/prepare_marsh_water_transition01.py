"""Freeze own-body, exact staged endpoints and old-motion-only transition refs."""
from pathlib import Path
import json,hashlib,sys
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];mode,side=sys.argv[1:3]
assert mode in ('pickup','drain') and side in ('east','west','north','south')
B=ROOT/'character/marsh-water-transition-material-v1';S=B/'sources';S.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
def resolve(p,n):return ROOT/n.removeprefix('res://') if n.startswith('res://') else (p.parent/n).resolve()
cat=ROOT/'character/marsh-v2/catalog.json';selected={}
for n in json.loads(cat.read_text())['body']:
    p=resolve(cat,n)
    for state in json.loads(p.read_text())['states']:selected[state['id']]=(p,state)
master=resolve(selected['idle-'+side][0],selected['idle-'+side][1]['frameFiles'][0])
revision={'east':'02','west':'01','north':'04','south':'01'}[side]
swim=ROOT/f'character/marsh-loaded-swim-material-v1/{side}-loop-{revision}-unselected/000.png'
carry=ROOT/f"character/marsh-{side}-carry-material-v1/candidate-{'03' if side in ('east','west') else '01'}/000.png"
ends=[master,swim] if mode=='pickup' else [swim,carry]
key=('swim-pickup-' if mode=='pickup' else 'cargo-drain-')+side
mp,state=selected[key];old=[resolve(mp,n) for n in state['frameFiles']]
def board(name,paths,labels):
    im=Image.new('RGB',(224*len(paths),238),'#293b40');d=ImageDraw.Draw(im)
    for i,p in enumerate(paths):
        q=Image.open(p).convert('RGBA');im.paste(q,(224*i+(20 if q.width==184 else 0),25),q);d.text((224*i+4,5),labels[i],fill='white')
    p=S/(name+'.png');im.save(p);return p
stem=mode+'-'+side+'-01'
refs=[board(stem+'-body-primary',[master],['OWN '+side.upper()+' BODY MASTER']),board(stem+'-endpoints',ends,['EXACT ORIGIN','EXACT DESTINATION']),board(stem+'-old-motion-only',old,['OLD MOTION ONLY '+str(i) for i in range(len(old))]),ROOT/f'character/marsh-motion-polish-v1/sources/{side}-standing-identity-01.png']
height=146 if side=='north' else 147
face={'east':'Own RIGHT profile facing imageRIGHT, visible anatomicalRIGHT temple implant, one outerRIGHT leading case latch.','west':'Own LEFT profile facing imageLEFT, near anatomicalLEFT temple BARE; RIGHT implant far side hidden. One outerLEFT leading case latch. NEVER mirrored East.','south':'Own front facing imageDOWN/viewer; anatomicalRIGHT implant on viewerLEFT, two frontal ivory case latches.','north':'Own back facing imageUP/away; rear panel/harness, face/temple hidden naturally. Case held FORWARD beyond chest, partly occluded, never a backpack.'}[side]
poses='''FOUR complete transition figures in left-to-right motion order, plus ONE empty-handed upright neutral scale ruler.
Figure1 deep connected crouch/reach: hips and knees flex while BOTH hands grasp same small rigid case low before feet, case firmly supported, chest leans forward. Figure2 rise/lean with case lifted toward upper chest, knees still bent, body beginning to become buoyant. Figure3 launch into water: whole torso nearly horizontal PRONE, both hands holding case ahead of chest, correct hips/knees trail behind, legs unfolding away from head. Figure4 fully prone swimmer close to EXACT DESTINATION, one trailing leg extended/other folded, same adult volume and camera as endpoint. This is pose progression from standing through crouch/lift into swimming, NOT four standing waist-carry poses or four disconnected walk poses.'''
if mode=='drain':poses='''FOUR complete transition figures in left-to-right motion order, plus ONE empty-handed upright neutral scale ruler.
Figure1 swimmer begins rising as water drains: same case gripped ahead of chest, horizontal torso tilts toward upright, legs begin dropping below hips with knees naturally bent. Figure2 partly upright with legs dropping below hips, bent knees, case still secured before chest, no detached hands. Figure3 almost upright feet seeking floor below hips, knees partially flexed, case lowers toward waist. Figure4 fully upright PLANTED floor contact: BOTH feet flat at same ground level, knees/hips straight, case supported at waist with connected two-hand grip. This held grounded pose must precede EXACT DESTINATION carry stride; do not copy its stepping feet into Figure4. This is buoyant prone-to-grounded loaded standing, not an unloaded pose, not walking, and case must never become a backpack.'''
prompt=f'''Production whole sprite sheet on true transparent background, one horizontal row, generous transparent gutters, no text/grid/background/shadows/bubbles. {poses}
Reference1 PRIMARY own adult body/head/proportions/material. Reference2 EXACT endpoint physical adult/equipment volume and water camera. Reference3 OLD MOTION ONLY, not its bulk/grade/gear authority. Reference4 original own directional identity. {face}
Same slim adult android botanist, full articulated adult limb length/narrow waist/modest sage shoulder plates/compact slate boots, muted greyed ivory/sage/slate and sandy hair, restrained outlines/quiet matte density. Same existing chest/rear panel,harness,pouches only. No helmet/extra gear/backpack/gold glossy ivory or saturated hair. Head physical21-22units high relative{height}standing adult, not tiny swimmer head or babyface. Identical physical adult and case scale across all stages; foreshorten organically at camera35degrees above water plane, no perpose resize/squeeze.
Rigid dark small case same dimensions/hardware as exact endpoint, divided inset panel/ivory latch visibility appropriate to own direction, correct two articulated hands gripping edges, no enlarged shield/detached parcel/moving latches. Head/torso/pelvis/limbs/case form one connected whole pose. Natural correct knees/elbows, two separate boots, no extra limbs. Keep direction fixed {side.upper()} throughout, no unintended yaw or mirrored source. Water plane becomes grounded stance through whole physical articulation, not scaling.
Final figure SAME adult upright empty-handed {side.upper()} neutral, relaxed arms/both feet flat, exact own PRIMARY proportions/material. One common neutral{height}height ruler for ALL whole figures. Complete figures fit separate cells; no clipping/pasted heads or limbs/recolour patches/per-pose fitting. Whole organic reauthoring only.'''
p=S/(stem+'.prompt.txt');p.write_text(prompt,encoding='utf-8')
r={'normalAdmission':False,'fullGoalComplete':False,'status':'frozen before generation','promptSha256':sha(p),'orderedReferences':[ref(p) for p in refs],'sourceFrames':[ref(master)]+[ref(p) for p in ends+old],'stagedEndpoints':[ref(p) for p in ends],'selectedTransitionManifest':ref(mp),'selectedTransitionState':state,'selectedIdleMaster':ref(master),'neutralOccupiedTargetHeight':height,'intermediateFigures':4,'rules':'Whole independent own direction; one neutral ruler, exact endpoints/normal timing; no patches/mirror/per-pose fitting. Physical contact/root/proportions/camera/grade remain review requirements.'}
(S/(stem+'.request.json')).write_text(json.dumps(r,indent=2)+'\n')
print(stem,'frozen',state.get('frameDurationsMs'),state.get('loop'))
