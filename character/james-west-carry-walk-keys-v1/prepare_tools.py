from pathlib import Path
from PIL import Image
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
for index in [0,28,36]:
    name=f'walk{index:02}-tool-fix';source=p/f'walk{index:02}-carry.png';target=Image.open(source).convert('RGBA').crop((112,112,160,160)).resize((576,576),Image.Resampling.LANCZOS);target.save(p/(name+'-target.png'))
    prompt='''Edit this fixed48x48native square case/wrist/belt crop enlarged12x, original framing/alpha margins unchanged. There are TWO yellow-screen fragments. Remove ONLY the small EXTRA upper yellow-screen triangle just ABOVE the SILVER WRIST CUFF: center native world x127,y125..129 (crop x15,y13..17). That upper fragment is a phantom copied from a case-grip reference, not a real belt item. Replace it with coherent original neutral graphite torso/forearm cloth behind cuff, correct subtle cloth detail and natural overlap. No dark hole, blank transparency, black cavity or another tool.
Keep the REAL full rectangular diagnostic meter LOWER on the belt exactly unchanged, screen around native y136..141 (crop y24..29), complete housing below it. Preserve the case panel, both gloved hands and silver latches, wrist cuff, chest marks, lower meter/tool, belt/wrench/hips and every other pixel position/design. No exposure/color/material shift or case resizing. Same subdued MATTE graphite/ochre/dull silver, clean alpha transparency, no purple or pale outline. Return only the repaired ORIGINAL full square crop, same framing, with the SMALL UPPER phantom gone and original LOWER meter retained.'''
    (p/(name+'-prompt.txt')).write_text(prompt+'\n',encoding='utf-8');files=[source,p/(name+'-target.png'),p/(name+'-prompt.txt'),Path(__file__)]
    (p/(name+'-inputs.json')).write_text(json.dumps({'preCallSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'crop':[112,112,160,160],'admissionRegion':[124,122,134,132],'baseFile':source.name,'scope':'Remove upper phantom screen only, real lower meter and complete source outside10x10rectangle exact.'},indent=2)+'\n',encoding='utf-8')
print('Three10x10upper phantom-screen removals prepared; real belt meters outside admission.')
