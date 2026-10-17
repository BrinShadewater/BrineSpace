from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
sources=[p/'late-pose.png',r/'character/james-west-master-carry-v1/local-v3-carry-pose.png']
for name,source in zip(['meter-target','meter-reference'],sources):
    Image.open(source).convert('RGBA').crop((120,128,160,168)).resize((480,480),Image.Resampling.NEAREST).save(p/(name+'.png'))
prompt='''EDIT TARGET: first square waist/wrist/hip crop from James's late carrying pose. SUPPORTING REFERENCE: second crop from West carrying pose, demonstrating ONE partly hidden belt meter.

Remove ONLY the extra lower rectangular meter copy below the wrist on image right. Its small yellow display lies near50percent across/45percent down this square, inside a dark-grey box near40..60percent across/35..60percent down. Replace that extra lower box with coherent matte graphite belt/hip fabric and normal narrow worn silver belt fastening as in reference. Keep the ORIGINAL upper partially hidden meter, whose yellow corner is near20percent across/15percent down, exactly where it is. Keep ALL original glove/fingers/wrist/case/leg anatomy, pose and material unchanged. No new meter or tool; one original meter partly behind forearm. No dark cavity or blank transparent hole, no bright yellow extra mark below hand. Preserve exact square composition, neutral matte grey/yellow grade and transparent background. Only remove the lower duplicate, never move the retained upper meter or modify grip/case. Return one same square crop.'''
(p/'meter-prompt.txt').write_text(prompt+'\n',encoding='utf-8')
files=sources+[p/'meter-target.png',p/'meter-reference.png',p/'meter-prompt.txt',Path(__file__)]
(p/'meter-inputs.json').write_text(json.dumps({'preCallSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'base':sources[0].relative_to(r).as_posix(),'crop':[120,128,160,168],'admissionRegion':[136,142,144,154],'selected':False,'scope':'Lower duplicate meter removal only; upper partial meter/grip protected outside rectangle.'},indent=2)+'\n',encoding='utf-8')
print('Late lower duplicate-meter crop/reference and8x12native admission frozen; retained upper meter outside region.')
