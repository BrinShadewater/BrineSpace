from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
JOINT=ROOT/'character/bill-west-water-joint-continuity-v1'
hashes={}
def read(p):
 hashes[p.relative_to(ROOT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
 return Image.open(p).convert('RGBA')
def meta(p):
 hashes[p.relative_to(ROOT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
 return json.loads(p.read_text(encoding='utf-8'))
def common(p):
 im=read(p);assert im.size in [(256,256),(352,320)]
 c=Image.new('RGBA',(352,320));c.alpha_composite(im,(32,0) if im.size==(256,256) else (0,0));return c
original=ROOT/'character/bill-water-exit-west-master-v8/sources/master-west-reference.png'
master=read(original);density=148/956
# Reviewed source landmarks: hair crown20 and lowest forefoot sole976.
# Keep the original background; uniform affine sampling positions the physical sole,
# not the bottom of its1024px image, at pivot224. No anatomical/pose fitting.
correct=master.transform((352,320),Image.Transform.AFFINE,(1/density,0,180-160/density,0,1/density,976-224/density),Image.Resampling.BICUBIC)
legacy=Image.new('RGBA',(352,320));old=master.resize((round(master.width*density),round(master.height*density)),Image.Resampling.LANCZOS);legacy.alpha_composite(old,(160-old.width//2,224-old.height))
correct.save(OUT/'master-sole-registered.png')
ba=meta(ROOT/'character/bill-walk-west-master-repair-v2/bank-assessment.json')
barepaths={v['frame']:ROOT/'character/bill-walk-west-master-repair-v2'/v['study'] for v in ba['poses']}
equipped=ROOT/'character/bill-equipped-west-selected-v1';em=meta(equipped/'manifest.json');assert em['standingHeight']==148 and em['pivot']==[128,224]
idle=equipped/next(s for s in em['states'] if s['id']=='interact-west')['frameFiles'][0]
canonical=read(ROOT/'character/bill-cargo-helmet-west-v1/sources/canonical-head.png');reg=meta(ROOT/'character/bill-cargo-helmet-west-v1/helmet-registration.json')
assert hashlib.sha256((ROOT/'character/bill-cargo-helmet-west-v1/sources/canonical-head.png').read_bytes()).hexdigest()==reg['canonicalHeadSha256']
groups={
 'bare':[('Master: sole registered',correct),('Old board: image bottom',legacy),('Prior walk28',common(ROOT/'character/bill-walk-west-material-v1/frames/bare/walk-west/028.png')),('Current walk28',common(barepaths[28])),('Current Ready',common(JOINT/'bare-ready-candidate.png')),('Current Rise',common(JOINT/'bare-rise-candidate.png')),('Current resumed34',common(barepaths[34]))],
 'helmet':[('Established equipped idle',common(idle)),('Prior walk28',common(ROOT/'character/bill-walk-west-material-v1/frames/helmet/walk-west/028.png')),('Current walk28',common(ROOT/'character/bill-walk-west-helmet-master-repair-v1/canvas-normalized-study-028.png')),('Current Ready',common(JOINT/'helmet-ready-candidate.png')),('Current Rise',common(JOINT/'helmet-rise-candidate.png')),('Current resumed0',common(ROOT/'character/bill-walk-west-helmet-master-repair-v1/canvas-normalized-study-000.png'))]}
boards=[]
for gear,items in groups.items():
 board=Image.new('RGB',(352*len(items),740),(31,35,40));draw=ImageDraw.Draw(board)
 for n,(name,im) in enumerate(items):
  x=n*352;draw.text((x+5,10),name,fill='white');board.paste(im,(x,35),im)
  draw.line((x+100,259,x+250,259),fill=(65,180,195))
  crop=im.crop((120,55,200,135)).resize((240,240),Image.Resampling.NEAREST);board.paste(crop,(x+55,430),crop)
  draw.text((x+5,400),'Fixed source head/collar x3',fill='white')
 draw.text((10,710),'Common standing ruler148; cyan physical pivot224. Whole-source translation/padding only. Head pose/foreshortening still require visual judgment.',fill='white')
 name=f'{gear}-head-master-review.png';board.save(OUT/name);boards.append(name)
c=Image.new('RGB',(650,300),(31,35,40));c.paste(canonical.resize((240,240),Image.Resampling.NEAREST),(20,35),canonical.resize((240,240),Image.Resampling.NEAREST));ImageDraw.Draw(c).text((20,10),'Established helmet crop40x40 at H148, x6',fill='white');c.save(OUT/'canonical-helmet-review.png')
assert hashes=={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in hashes}
report={'inputSHA256':hashes,'boards':boards,'standingRuler':148,'commonPivot':[160,224],'masterSourceLandmarks':{'crownY':20,'forefootSoleY':976,'uncertaintySourcePixels':2,'density':density,'reviewedSoleBoard':'master-sole-landmark-review.png'},'legacyMasterSoleMisregistrationPixels':float((master.height-976)*old.height/master.height),'normalAdmission':False,'visualAcceptance':False,'scope':'Master/established equipped idle and actual captured gait contexts on common physical ruler. Diagnostic landmarks and crops are not anatomical segmentation.'}
(OUT/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
html='<!doctype html><meta charset="utf-8"><title>Bill West master head audit</title><style>body{background:#1f2328;color:#eee;font:18px sans-serif;margin:28px}img{max-width:100%}</style><h1>Bill: master and head consistency</h1><p>Compare the original master, established helmet and current walking/water poses on the same physical scale. The master is positioned by its sole rather than the background edge. These are review comparisons, not approved animation changes.</p>'
for name in boards+['canonical-helmet-review.png','master-sole-landmark-review.png']:html+=f'<p><img src="{name}"></p>'
(OUT/'index.html').write_text(html,encoding='utf-8')
print(json.dumps({'frozenInputs':len(hashes),'boards':len(boards),'legacyMasterSoleMisregistrationPixels':report['legacyMasterSoleMisregistrationPixels']}))
