"""Freeze a whole-pose dry South collapse study against current material authority."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-collapse-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    sources=BASE/'sources';sources.mkdir(parents=True,exist_ok=True)
    catalog=ROOT/'character/marsh-v2/catalog.json';states={}
    for name in json.loads(catalog.read_text())['body']:
        manifest=ROOT/name.removeprefix('res://') if name.startswith('res://') else catalog.parent/name
        for state in json.loads(manifest.read_text())['states']:
            states[state['id']]=[ROOT/p.removeprefix('res://') if p.startswith('res://') else manifest.parent/p for p in state['frameFiles']]
    board=Image.new('RGB',(6*368,450),'#293b40');draw=ImageDraw.Draw(board)
    guide=states['death-ground-south'];idle=states['idle-south'][0]
    for i,path in enumerate(guide[1:]+[idle]):
        im=Image.open(path).convert('RGBA');board.paste(im.resize((368,368),Image.Resampling.NEAREST),(i*368,65),im.resize((368,368),Image.Resampling.NEAREST))
        draw.text((i*368+8,8),['1 knees soften','2 knees down','3 hands brace','4 body lowers','5 settled floor','6 selected idle ruler'][i],fill='white')
        draw.text((i*368+8,30),'POSE ONLY / old material wrong' if i<5 else 'PRIMARY material / proportions',fill='#a4d4c3')
    board.save(sources/'collapse-pose-guide.png')
    primary=ROOT/'character/marsh-south-step-v1/sources/idle-gait-reference.png'
    master=ROOT/'character/marsh-motion-polish-v1/sources/south-standing-identity-01.png'
    prompt='''Create one transparent pixel-art animation source sheet of SIX COMPLETE separate figures of Marsh, the exact South/front-view adult male android shown in reference1. Arrange a single horizontal row with wide clear gutters. Reference1 selected idle/gait is PRIMARY body scale, fitted proportions, elevated frontal camera, warm matte ivory/sage material and drawing detail authority. Reference2 shows FIVE OLD dry collapse poses plus selected idle ruler: use ONLY its motion/ground positions, NEVER its dark boots/cool grade. Reference3 is identity/temple-hardware authority.

Figures1-5 are a gentle dry mechanical shutdown collapse, following reference2's whole anatomical poses in order: knees soften and torso dips; knees contact the floor; hands brace naturally on floor with connected shoulders/elbows/wrists; chest/pelvis settle lower; final side/front diagonal body rests on floor, both complete legs and arms visible without crossing or duplicated joints. Match reference2's slight elevated South camera and ground-plane orientation. Preserve exact adult head/torso/leg proportions from reference1. Crouching and floor poses shorten naturally; DO NOT fit every pose to standing height. This is an android shutdown: no blood, white liquid, smoke, sparks, debris, or puddle. No floor/background/shadow or labels.

Figure6 is the standing neutral ruler, exact reference1 idle silhouette and stance: body width58 and declared standing height148 at target density, sole centers27pixels apart. Same source drawing scale for ALL six figures; this figure establishes one global scale. Fitted physique, hands beside hips, no bulky shoulders or huge head. Keep swept blond hair, silver temple hardware, adult face, ivory collar and rectangular chest panel, olive shoulder pads and pouches, both harness straps, dark gloves. Entire suit legs/knees/shins/ankles/boot UPPERS stay warm matte ivory, with only narrow dark soles; do NOT make feet black or replace boots with dark calves. Subdued warm matte ivory/sage grade identical to reference1 throughout, restrained pixel outlines and crisp pixel detail, no glossy highlights or new lighting. No body mirroring. Every figure is fully contained with clear gaps: head, fingers, forearms and both boot tips inside its cell. Draw complete poses; do not patch isolated limbs. Essential correction is coherent selected-idle identity and material THROUGH all collapse poses, with ivory boot uppers and matched grade.'''
    prompt_path=sources/'collapse-01.prompt.txt';assert not prompt_path.exists()
    prompt_path.write_text(prompt+'\n',encoding='utf-8')
    refs=[primary,sources/'collapse-pose-guide.png',master]
    request={'status':'frozen before whole-pose dry South collapse generation','normalAdmission':False,'promptSha256':sha(prompt_path),'orderedReferences':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in refs],'guideSourceFrames':[{'path':p.resolve().relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in guide[1:]+[idle]],'sheetGrid':[6,1],'transparentBackground':True,'contract':{'canvas':[184,184],'pivot':[92,172],'standingHeight':148,'durationsMs':[180]*6,'loop':False},'scope':'Dry collapse source only. Injury fluid/rise and normal runtime remain unchanged until source motion/identity/material review.'}
    (sources/'collapse-01.request.json').write_text(json.dumps(request,indent=2)+'\n')
    print('Frozen exact prompt, three ordered references, five selected collapse guides and selected idle ruler.')
if __name__=='__main__':main()
