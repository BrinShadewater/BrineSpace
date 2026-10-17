from pathlib import Path
from PIL import Image
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1];crop=[80,112,160,192]
reference=p/'walk00-case-v2-fleck.png'
Image.open(reference).convert('RGBA').crop(crop).resize((640,640),Image.Resampling.LANCZOS).save(p/'case-family-reference.png')
for index in (12,28,36):
    name=f'walk{index:02}-case-v2'
    source=r/'character/james-west-carry-depth-v1/walk12-carry.png' if index==12 else p/f'walk{index:02}-tool-fix.png'
    base=p/f'{name}-original.png';Image.open(source).convert('RGBA').save(base)
    Image.open(source).convert('RGBA').crop(crop).resize((640,640),Image.Resampling.LANCZOS).save(p/f'{name}-target.png')
    prompt=f'''Edit image1 only: fixed80x80native crop enlarged8x of James carrying case during walk phase{index}. Image2 is corrected carrying-case geometry at identical scale/camera/crop. Image1 case currently looks short/squat with variable silver corner-latch spacing. Match image2 physical rigid case dimensions, tall panel aspect ratio, four dull silver corner latches and low waist position. Use SAME solid graphite case, not a different design or width each phase. Preserve image1 torso and upper-thigh walking pose, original arm cuff/cloth material, belt and tools; only adapt case and both gloved grips enough for coherent same rigid object. Keep case IN FRONT facing character LEFT, far glove at left side, near glove at right edge with fingertips visibly wrapping/supporting case, wrist joins original silver cuff. No floating/hanging hand below case, intersecting body or detached wrist. Keep current near forearm/cuff above native world124 unchanged; adjust just case/hand region below. Reference case approximately world92..126,y129..155; framing native crop80..160,112..192. This is a dimension/shape reference, do not copy its original standing legs or hip pose. Preserve image1 real belt meter/wrench housing/design, no new yellow fragment or screen above glove. Same subdued MATTE graphite/ochre/dull silver, no magenta/purple, bright chrome, black cavity or transparent hole. Keep square framing/alpha margins and return only edited image1 crop.'''
    (p/f'{name}-prompt.txt').write_text(prompt+'\n',encoding='utf-8')
    files=[source,reference,base,p/f'{name}-target.png',p/'case-family-reference.png',p/f'{name}-prompt.txt',Path(__file__)]
    (p/f'{name}-inputs.json').write_text(json.dumps({'preCallSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'crop':crop,'admissionRegion':[88,124,145,163],'baseFile':base.name,'scope':'Bounded rigid-case and glove refinement; original belt tooling within admission still requires identity review.'},indent=2)+'\n',encoding='utf-8')
print('Three local case/grip refinements prepared; original torso/head/legs outside bounded region retained.')
