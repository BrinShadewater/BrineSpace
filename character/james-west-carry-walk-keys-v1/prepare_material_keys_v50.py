from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'master-material-keys-v50';out.mkdir(exist_ok=True)
indices=list(range(0,49,6));atlas=Image.new('RGBA',(768,768));sources=[]
for cell,index in enumerate(indices):
    f=p/'master-head-review-v16'/('bare-%03d.png'%index);im=Image.open(f).convert('RGBA');assert im.size==(256,256)
    atlas.alpha_composite(im,(cell%3*256,cell//3*256));sources.append(f)
atlas.resize((1536,1536),Image.Resampling.NEAREST).save(out/'edit-atlas.png')
refs=[out/'edit-atlas.png',p/'master-material-v49/original-master.png',p/'master-material-v49/bare-head-protected.png']
prompt='''Edit Image1: ONE transparent animation source atlas, exactly3columns by3rows of James walking while holding a case, nine different existing chronological poses. Each square cell is256native units on a768square canvas, presented enlarged1536square. Image2 is the authoritative ORIGINAL character master for matte material/color, identity, proportions and fine restrained fabric detail. Image3 is the material-repaired walking entry: supporting finish reference only. Never copy its leg pose into other cells.
Across ALL NINE sprites, correct ONLY excessively bright stitching and shiny hardware to the same matte charcoal finish as Image2, using the subdued seam and silver intensity demonstrated by Image3. Neutral/warm charcoal quilted fabric, muted engineering yellow shoulder accents, worn dull silver pads/fittings. No white seam outlines, purple/magenta cast, glossy highlights, solid black shadow patches or loss of quilting.
Keep EVERY original cell's distinct exact pose: head position/size/identity, torso/shoulder angle, raised forearms and hands, case outer dimensions/position and grip, fixed belt wrench/meter, two separate legs, knee bends, boot locations and floor contacts. No pose averaging, no body reproportioning, no changing case geometry, no added equipment, no repeated standing pose. Preserve original3x3 layout, margins, canvas registration and each cell's physical pivot. Do not move, recenter, crop or individually rescale any sprite.
Return ONE square3x3 source atlas on real transparent background, nine complete sprites in exactly the same positions and scale. No labels, no frames, no backdrop, no shadow. Match the original fine pixel-art density rather than shiny high-contrast line art. Material-only correction, not new motion.'''
(out/'prompt.txt').write_text(prompt,encoding='utf-8')
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
(out/'inputs.json').write_text(json.dumps(dict(indices=indices,grid=[3,3],cellSize=256,sourceSha256={f.relative_to(r).as_posix():sha(f) for f in sources},referenceSha256={f.relative_to(r).as_posix():sha(f) for f in refs},promptSha256=sha(out/'prompt.txt'),normalChanged=False),indent=2)+'\n')
print('Nine distributed existing walking poses packed without pose resizing; input hashes frozen.')
