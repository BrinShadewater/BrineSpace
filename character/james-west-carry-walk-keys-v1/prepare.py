from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];audit=r/'character/james-west-carry-depth-v1/walk-donor-inputs.json';a=json.loads(audit.read_bytes());m=r/a['manifest'];data=json.loads(m.read_bytes());state=next(s for s in data['states'] if s['id']=='walk-west')
case=r/'character/james-west-carry-depth-v1/case-grip-reference.png';Image.open(case).save(p/'case-grip-reference.png')
template=(r/'character/james-west-carry-depth-v1/walk12-carry-prompt.txt').read_text(encoding='utf-8')
for index in [0,28,36]:
    name=f'walk{index:02}-carry';ref=state['frameFiles'][index];source=r/ref.removeprefix('res://') if ref.startswith('res://') else m.parent/ref;out=Image.new('RGBA',(256,256));out.alpha_composite(Image.open(source).convert('RGBA'),(round(128-data['pivot'][0]),round(224-data['pivot'][1])));out.save(p/(name+'-original.png'));out.crop((80,88,176,184)).resize((768,768),Image.Resampling.LANCZOS).save(p/(name+'-target.png'))
    prompt=template+f'\nThis is selected walking phase{index}, an independent source carrying-pose edit. Keep its ORIGINAL torso inclination/hips and shoulder position while adding the same case/grip. Preserve all belt items/markings and matte grade; no new tool or arm-pose/material redesign between phases.\n'
    (p/(name+'-prompt.txt')).write_text(prompt,encoding='utf-8');files=[source,m,p/(name+'-original.png'),p/(name+'-target.png'),case,p/'case-grip-reference.png',p/(name+'-prompt.txt'),Path(__file__)]
    (p/(name+'-inputs.json')).write_text(json.dumps({'preCallSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'crop':[80,88,176,184],'admissionRegion':[88,104,166,169],'baseFile':name+'-original.png','sourceIndex':index,'sourceState':'walk-west','scope':'One authored carrying upper source on actual selected walk frame; full loop/dynamics/join/normal admission pending.'},indent=2)+'\n',encoding='utf-8')
print('Selected walking0/28/36 upper-carry sources frozen from actual49frame manifest.')
