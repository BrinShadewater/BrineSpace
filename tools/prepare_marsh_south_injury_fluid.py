"""Freeze effect-only authoring so Marsh's complete body source remains exact."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-injury-material-v1'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    sources=BASE/'sources';sources.mkdir(parents=True,exist_ok=True)
    refs=[ROOT/f'character/marsh-master-repair-v1/frames/injury-ground-south/{i:03d}.png' for i in [1,3,5]]
    board=Image.new('RGB',(3*552,620),'#293b40');draw=ImageDraw.Draw(board)
    for i,path in enumerate(refs):
        figure=Image.open(path).convert('RGBA').resize((552,552),Image.Resampling.NEAREST)
        board.paste(figure,(i*552,50),figure)
        draw.text((i*552+15,10),['White glove drips','Thin small floor puddle','Thin larger white floor puddle'][i],fill='white')
        draw.text((i*552+15,30),'FLUID ONLY reference / do not generate characters',fill='#a4d4c3')
    guide=sources/'white-fluid-reference.png';assert not guide.exists();board.save(guide)
    prompt='''Create a transparent pixel-art EFFECT-ONLY sprite sheet: FOUR isolated swatches of WHITE ANDROID COOLANT, in one horizontal row with very wide transparent gutters. Use the reference ONLY for its tiny white liquid droplets and thin floor puddle near the left glove. Absolutely NO people, bodies, heads, hands, gloves, suit pieces, boots, floor tiles, ground, labels or rulers. The characters in the reference are context, and must not appear in this output.

Draw all four effects at ONE common pixel/drawing scale, as modest matte off-white liquid, subtle warm grey underside/edge and sparse ivory highlight pixels. Fluid is neutral white, not blood, not cyan, not glowing or luminous; no smoke, spark, froth, glossy glass shine or cast shadow. Match the reference's restrained small pixel shapes and elevated camera. No outline that looks like a black object. Crisp flat pixel clusters, no blurred halo.

Swatch1: sparse short downward drips from an offscreen glove: one tiny vertical bead trail, two separated droplets. At common drawing scale aim approximately20pixels wide by52pixels high. Swatch2: a slightly longer narrow white drip trail with three beads, approximately24wide by72high, no glove. Swatch3: a small flattened elliptical white floor puddle, approximately110wide by24high, ragged but compact fluid edge, no vertical splash. Swatch4: the fully developed modest flattened elliptical floor puddle, approximately160wide by32high, only a little broader than swatch3, matching the thin white puddle seen in reference3. These proportions are relative to each other at one common drawing scale. Keep every entire swatch complete and separated. Leave generous transparent margins.

This sheet will be uniformly reduced using the last puddle as a36pixel width calibration for the existing H148 character sprite. Do not make huge flood pools. The mature puddle should be wide and only about7pixels deep at target size, suggesting the floor plane under the left forearm. All four swatches share the same style, material and source density. Generate ONLY these four white fluid effects on actual transparency.'''
    prompt_path=sources/'fluid-01.prompt.txt';prompt_path.write_text(prompt+'\n',encoding='utf-8')
    request={'status':'frozen effect-only request before generation','normalAdmission':False,'promptSha256':sha(prompt_path),'orderedReferences':[{'path':guide.relative_to(ROOT).as_posix(),'sha256':sha(guide)}],'referenceSourceFrames':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in refs],'transparentBackground':True,'swatchCount':4,'calibration':{'commonScale':'36 / mature-puddle occupied source width','maturePuddleDenseWidth':36,'operation':'one common BOX scale; alpha128; complete effect translation behind exact whole body source'},'bodyAuthority':'character/marsh-south-collapse-material-v1/candidate-01','constraints':'No character pixels generated or edited. Dry shutdown stays dry. Only effect pixels author injury liquid.'}
    (sources/'fluid-01.request.json').write_text(json.dumps(request,indent=2)+'\n')
    print('Frozen white-fluid-only prompt, reference guide and calibration; complete body untouched.')
if __name__=='__main__':main()
