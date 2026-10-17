from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=r/'character/james-east-inspect-body-grade-v25';out.mkdir(exist_ok=True)
source=r/'character/james-tablet-east-matte-v3'
template=(source/'material-bake.gd').read_text()
template=template.replace('const OUT="res://character/james-tablet-east-matte-v3/"','const OUT="res://character/james-east-inspect-body-grade-v25/"')
template=template.replace('const SOURCE="res://character/james-tablet-east-belt-fixed-source-v2/"','const SOURCE="res://character/james-tablet-east-matte-v3/"')
a=template.index('func selected(');b=template.index('func run():',a)
template=template[:a]+'''func selected(pixel:Color,point:Vector2i) -> bool:
 if pixel.a<=0 or point.x<56 or point.x>=110 or point.y<24 or point.y>=172:return false
 var r:=pixel.r*255.;var g:=pixel.g*255.;var b:=pixel.b*255.
 # Continuous violet selection, not semantic hair/fabric segmentation.
 return minf(r,b)-g>2.0 and absf(r-b)<20.0 and (r+g+b)/3.0>16.0
'''+template[b:]
template=template.replace('material-study.gdshader','body-material.gdshader')
template=template.replace(' and (protection.get_pixelv(at).r<.5 or spill)', ' and protection.get_pixelv(at).r<.5')
template=template.replace('Native shader green-channel despill and bounded pale-violet equipment matte. Re-export original alpha and original RGB outside colour selection; exact endpoints, no pose/clock/UV change. Not a semantic tablet mask.',
 'Native smooth violet-chroma correction bounded to body/hair region, skin/amber excluded by chroma, shared helmet differences exact. Selected matte tablet sources preserved, original alpha/outside selector exact, endpoints exact. Not semantic segmentation.')
template=template.replace('JAMES MATERIAL BAKE:','JAMES BODY MATERIAL BAKE:')
(out/'material-bake.gd').write_text(template,encoding='utf-8')
files=[Path(__file__),out/'material-bake.gd',out/'body-material.gdshader',source/'material-bake.gd',p/'review.json',p/'raw.png',p/'prompt.txt',r/'character/james-side-motion-review-2026-10-02/run_validation.py']
for mode in ['bare','helmet']:
 f=source/(mode+'-manifest.json');files.append(f);data=json.loads(f.read_bytes());state=next(s for s in data['states'] if s['id']=='inspect-east')
 files.extend((f.parent/x).resolve() for x in state['frameFiles'])
(out/'native-inputs.json').write_text(json.dumps({'preLaunchSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in set(files)}},indent=2)+'\n')
print('Native paired body-color study prepared,282 selected source frames frozen. Normal loader untouched.')
