"""Freeze North whole-collapse authoring against selected idle/gait and master."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-north-collapse-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    sources=BASE/'sources';sources.mkdir(parents=True,exist_ok=True)
    catalog=ROOT/'character/marsh-v2/catalog.json';states={}
    for name in json.loads(catalog.read_text())['body']:
        manifest=ROOT/name.removeprefix('res://') if name.startswith('res://') else catalog.parent/name
        for state in json.loads(manifest.read_text())['states']:
            states[state['id']]=[ROOT/p.removeprefix('res://') if p.startswith('res://') else manifest.parent/p for p in state['frameFiles']]
    idle=states['idle-north'][0];guide=states['death-ground-north'][1:]
    primary_paths=[idle,states['idle-north'][1],states['walk-north'][0],states['walk-north'][3]]
    primary=sources/'selected-north-idle-gait.png';assert not primary.exists()
    board=Image.new('RGB',(4*552,620),'#293b40');draw=ImageDraw.Draw(board)
    for i,path in enumerate(primary_paths):
        image=Image.open(path).convert('RGBA');assert image.size==(184,184)
        image=image.resize((552,552),Image.Resampling.NEAREST);board.paste(image,(552*i,50),image)
        draw.text((552*i+10,10),['SELECTED North idle0','SELECTED North idle1','SELECTED North gait0','SELECTED North gait3'][i],fill='white')
        draw.text((552*i+10,30),'PRIMARY material / body / camera / density',fill='#a4d4c3')
    board.save(primary)
    pose_guide=sources/'collapse-pose-guide.png'
    board=Image.new('RGB',(6*368,450),'#293b40');draw=ImageDraw.Draw(board)
    for i,path in enumerate(guide+[idle]):
        image=Image.open(path).convert('RGBA').resize((368,368),Image.Resampling.NEAREST)
        board.paste(image,(i*368,65),image)
        draw.text((i*368+8,8),['1 knees soften','2 lower crouch','3 knees/hands down','4 chest settles','5 prone / soles visible','6 selected neutral ruler'][i],fill='white')
        draw.text((i*368+8,30),'POSE ONLY: body/detail can drift' if i<5 else 'PRIMARY proportions / grade',fill='#a4d4c3')
    board.save(pose_guide)
    master=ROOT/'character/marsh-motion-polish-v1/sources/north-standing-identity-01.png'
    prompt='''Create a transparent pixel-art animation source sheet of SIX COMPLETE separated figures of Marsh, the exact NORTH/rear-view adult male android from reference1. One horizontal row with wide transparent gutters. Reference1 selected North idle/gait is PRIMARY authority for fitted adult build, head/torso/limb proportions, warm matte ivory/sage suit, body density and elevated rear camera. Reference2 gives only the old whole-body collapse motion and projected floor orientation; its widened torso/head/detail must NOT override the selected idle. Reference3 original standing rear master controls identity, rear harness, ivory back plate, blond hair whorl and right temple hardware. Its magenta background must NOT appear.

Figures1-5: gentle dry mechanical shutdown. 1 Knees soften, body lowers slightly, arms naturally bend without bulky shoulders; 2 a deeper crouch, torso pitches forward; 3 both knees settle on floor and complete connected arms/hands brace at sides; 4 chest lowers and forearms support the body; 5 fully prone, head facing away from viewer, both complete connected legs extend toward viewer, both black boot SOLES exposed and grounded, arms rest connected at shoulders and elbows. Preserve the rear-facing anatomical perspective of reference2 through these poses, especially final foreshortened legs/soles. No front faces, reflection or arbitrary turn toward viewer. Ivory ankle/shin/boot upper guards stay ivory; charcoal soles and heel undersides are intentionally DARK where exposed. Do not whiten soles and do not paint entire calves or boot uppers dark. This is DRY shutdown: no fluid, blood, smoke, sparks or puddle.

Figure6 is exact reference1 neutral standing rear ruler. At target drawing density the selected idle occupied silhouette is55wide by146high within the declared148standing ruler, p92/172 on184canvas; do not make a new stockier or wider neutral. Preserve the original fitted torso, head size, narrow natural stance and same shoulder/pouch/glove/heel relationships. ONE common drawing scale for ALL figures based on this neutral: do not size each crouched or prone pose to standing height, do not enlarge head or shoulders as he crouches. Natural occupied width can expand with complete arm articulation; it must not be forced to55 in all poses. Keep the head and rigid suit equipment at consistent master anatomical density throughout.

Muted warm matte ivory fabric and panels, sage shoulder pads/pouches, slate flexible joint bands, dark full gloves and dark soles, swept blond hair whorl, back straps and belt. Preserve rear backplate hardware and identity; no new backpack, helmet, tools or extra joints/fingers/feet. Subtle warm pixel shading and crisp restrained clusters, no glossy highlights, blue/cyan lighting or broad black outlines. Same material grade through all poses. Each figure fully contained with hands, elbows and sole tips inside its clear cell. No floor plane, cast shadow, text, labels or background: actual transparency. Draw COMPLETE whole figures, not separately patched limbs.'''
    prompt_path=sources/'collapse-01.prompt.txt';prompt_path.write_text(prompt+'\n',encoding='utf-8')
    refs=[primary,pose_guide,master]
    request={'status':'frozen whole North dry collapse request before generation','normalAdmission':False,'promptSha256':sha(prompt_path),'orderedReferences':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in refs],'primarySourceFrames':[{'path':p.resolve().relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in primary_paths],'guideSourceFrames':[{'path':p.resolve().relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in guide+[idle]],'transparentBackground':True,'sheetGrid':[6,1],'contract':{'canvas':[184,184],'pivot':[92,172],'standingHeight':148,'durationsMs':[180]*6,'loop':False},'constraints':'Complete poses at one common neutral scale. Dark exposed sole material preserved, warm ivory boot upper guards. No anatomical patch, reflection, per-pose height fitting or palette mapping.'}
    (sources/'collapse-01.request.json').write_text(json.dumps(request,indent=2)+'\n')
    print('Frozen exact North collapse prompt, ordered references and selected guide source hashes.')
if __name__=='__main__':main()
