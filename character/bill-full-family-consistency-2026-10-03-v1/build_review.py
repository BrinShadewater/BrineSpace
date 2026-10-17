"""Fixed physical scale, current selected sources; representative poses only."""
from pathlib import Path
import hashlib,json,importlib.util,contextlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('coverage',ROOT/'character/bill-coverage-audit-v1/build_audit.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);mod.P=P
with (P/'source-resolution.log').open('w',encoding='utf-8') as log,contextlib.redirect_stdout(log):mod.main()
audit=json.loads((P/'source-audit.json').read_text())
masters={
 'east':('character/bill-land-water-east-v3/master-relative-review.png',(0,25,320,345),(160,224)),
 'west':('character/bill-west-master-head-audit-v1/master-sole-registered.png',None,(160,224)),
 'north':('character/bill-video-north-v5/master-standing.png',None,(92,172)),
 'south':('character/bill-water-exit-south-v4/master-comparison.png',(1280,25,1600,345),(160,224))}
inputs={};samples=[]
def read(path):
 f=ROOT/path;inputs[path]=sha(f);return Image.open(f).convert('RGBA')
def registered(im,pivot,height):
 scale=148/height
 if scale!=1:im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
 result=Image.new('RGBA',(320,320));result.alpha_composite(im,(round(160-pivot[0]*scale),round(224-pivot[1]*scale)));return result
for path,digest in audit['manifestBindings'].items():assert sha(ROOT/path)==digest;inputs[path]=digest
loader=(ROOT/'scripts/grid_canvas.gd').read_text(encoding='utf-8').split('func _load_major_bill_animations()',1)[1].split('\nfunc ',1)[0]
for states in audit['selected'].values():
 for state in states.values():
  for path in state['files']:inputs[path]=sha(ROOT/path)
for direction in ['east','west','south','north']:
 path,crop,pivot=masters[direction];im=read(path)
 if crop:im=im.crop(crop)
 master=registered(im,pivot,148)
 for gear in ['bare','helmet']:
  tiles=[('Prepared rear stance reference' if direction=='north' else 'Registered original bare master',master,None)]
  for action in ['idle','walk','run','interact','kneel','repair','stand','carry','weld','swim']:
   key=action+'-'+direction;state=audit['selected'][gear].get(key)
   if not state:continue
   assert not state['mirrored'],key
   index=0 if action=='idle' else len(state['files'])//2
   path=state['files'][index];image=registered(read(path),state['pivot'],state['standingHeight'])
   record={'gear':gear,'key':key,'index':index,'frameCount':len(state['files']),'source':path,'manifest':state['manifest'],'pivot':state['pivot'],'standingHeight':state['standingHeight'],'precomposed':state['precomposed']}
   samples.append(record);tiles.append((f'{key} [{index}/{len(state["files"])-1}]',image,record))
  board=Image.new('RGBA',(1920,1000),(31,35,40,255));d=ImageDraw.Draw(board)
  for n,(label,image,record) in enumerate(tiles):
   x=n%6*320;y=n//6*500;d.text((x+8,y+8),label,fill='white');board.alpha_composite(image,(x,y+35))
   d.line((x+70,y+259,x+250,y+259),fill=(70,185,195))
   board.alpha_composite(image.crop((125,55,195,125)).resize((140,140),Image.Resampling.NEAREST),(x+90,y+350))
  board.save(P/f'{gear}-{direction}.png')
for path in ['character/bill-video-north-v5/source-selection.json','character/bill-video-north-v5/prepare.py']:
 inputs[path]=sha(ROOT/path)
report={'stateCounts':audit['stateCounts'],'frozenInputs':inputs,'loaderBlockSha256':hashlib.sha256(loader.encode()).hexdigest(),'samples':samples,'referenceScopes':{'north':'Prepared authored narrower-stance and matte reference; not pixel-identical original master. Original rear authority must be traced separately before source repair.','east':'Existing registered original side reference crop from master-relative-review.png.','west':'Original West source, sole-registered in master head audit.','south':'Existing registered original frontal reference crop from master-comparison.png.'},'headWindowScope':'Fixed standing head/collar diagnostic; crouched and swimming heads can fall outside it. Whole figures above remain authoritative.','visualReview':'pending eight boards','scope':'Current selected literal loader resolution, representative static samples. Common physical H148/p160224; no per-pose fitting or recoloring. Bare references do not prove helmet design. Precomposed equipment only is direct selected appearance; nonprecomposed samples require native fitter review. Not continuous cadence, contact, runtime reachability or full-set acceptance.','nativeRun':False,'fullVisualAcceptance':False}
(P/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'states':audit['stateCounts'],'samples':len(samples),'frozenInputs':len(inputs)}))
