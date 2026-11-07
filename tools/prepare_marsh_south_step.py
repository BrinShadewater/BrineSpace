"""Freeze a whole-figure South short-step request and ordered reference evidence."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-south-step-v1'
PROMPT='''Create a coherent six-pose pixel-art source sheet for Marsh, the exact blond male android botanist in these references. This is one small South/front-facing step TOWARD the viewer, followed by bringing the trailing foot forward, not a walking loop. Identity authority: reference 2, including his visible left-image temple hardware, stocky adult male proportions, short blond swept hair, neutral face, collar, two harness straps, chest panel, belt pouches, fitted ivory and sage suit, dark gloves, ivory shin/ankle/boot uppers with only narrow dark soles. Runtime style/camera/material authority: reference 1, which shows the currently selected South idle and gait at nearest-neighbor enlargement. Preserve that muted warm matte ivory/sage palette, shading, crisp pixel treatment, frontal slight elevated camera and body width/height. No extra gear, helmet, lighting, glossy surfaces, black boots, broadening shoulders, thinner torso or doll anatomy.

Return exactly 3 columns by 2 rows on true transparent background, six separate COMPLETE figures with generous transparent gutters and no labels, captions, floor lines, cast shadows or scene. Each cell has the same camera, drawing density and bodily scale; do not resize individual poses to a common bounding box. Read cells left-to-right then top-to-bottom. Keep BOTH boot tips, every finger and the top of the head fully visible.

Cell 0: tiny preparatory weight transfer onto the image-right foot. Both soles remain level; relaxed arms close to the body, chest facing South.
Cell 1: lift the image-left boot just clear of the floor, slightly bent knee; image-right boot remains the exact planted support, no wide arm swing.
Cell 2: image-left boot reaches modestly toward the viewer; show natural ankle/heel orientation and front leg in front. Image-right support remains planted. This is a compact shuffle, not a high knee or lunge.
Cell 3: image-left boot now planted one SMALL forward step ahead; torso transfers over it, image-right boot trails behind. Projected travel is about nine percent of standing height (13 pixels at a 148-pixel figure), no sideward travel. Preserve coherent hip/knee/ankle construction and ivory material.
Cell 4: image-left foot stays planted in exactly the same place as cell 3; trailing image-right boot lifts and comes forward toward the new standing line. Right boot still slightly behind the left, naturally flexed. Face/chest/front remain consistent; avoid rotating the whole body.
Cell 5: final neutral standing RULER, exact reference-1 idle proportions, head, material, posture and flat aligned boot stance. Both feet together at the new forward position. This cell calibrates the single sheet scale; it is not another moving pose.

Articulate each full figure coherently. Every arm connects through shoulder and elbow, both hands belong to their arms, and exactly two legs join through the pelvis. Keep the same facial identity, panel construction and warm matte grade throughout. Do not copy isolated limb stencils, mirror the body, add anatomy, or turn this into six unrelated standing variations.'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    sources=BASE/'sources';sources.mkdir(parents=True,exist_ok=True)
    prompt_path=sources/'step-01.prompt.txt';request_path=sources/'step-01.request.json'
    assert not prompt_path.exists() and not request_path.exists(),'Do not overwrite frozen request'
    selected=['character/marsh-south-idle-material-v1/candidate-01/000.png','character/marsh-south-walk-material-v1/candidate-02/000.png','character/marsh-south-walk-material-v1/candidate-02/003.png']
    board=Image.new('RGBA',(184*3,214),(41,59,64,255));draw=ImageDraw.Draw(board)
    for i,path in enumerate(selected):
        pose=Image.open(ROOT/path).convert('RGBA');board.alpha_composite(pose,(184*i,30));draw.text((184*i+4,5),['Selected idle','Selected gait0','Selected gait3'][i],fill='white')
    ref=sources/'idle-gait-reference.png';board.resize((board.width*3,board.height*3),Image.Resampling.NEAREST).save(ref)
    refs=[ref,ROOT/'character/marsh-motion-polish-v1/sources/south-standing-identity-01.png']
    prompt_path.write_text(PROMPT,encoding='utf-8')
    request={'status':'frozen before generation; unselected whole-figure source study','normalAdmission':False,'promptSha256':sha(prompt_path),'orderedReferences':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in refs],'selectedReferenceInputs':[{'path':p,'sha256':sha(ROOT/p)} for p in selected],'transparentBackground':True,'desiredSheetGrid':[3,2],'bodyScaleContract':'One neutral-ruler scale for complete figures; no per-pose height fitting, mirroring or anatomical edits.'}
    request_path.write_text(json.dumps(request,indent=2)+'\n')
    print('Frozen South short-step request;2ordered references;3selected source hashes.')
if __name__=='__main__':main()
