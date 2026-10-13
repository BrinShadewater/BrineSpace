"""Retain complete rejected far-half figures; no cycle or native admission."""
from pathlib import Path
import hashlib,json,shutil
import numpy as np
from PIL import Image,ImageDraw
from rebuild_bill_art import binary
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-carry-material-v1';S=BASE/'sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
gid='exec-2557b186-1649-4014-be99-f397cd83811a';original=Path('C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96')/(gid+'.png');rawpath=S/'half-02.raw.png';shutil.copy2(original,rawpath)
p=S/'half-02.request.json';r=json.loads(p.read_text());assert sha(S/'half-02.prompt.txt')==r['promptSha256']
for q in r['orderedReferences']+r['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
r.update(status='Retained rejected: contact/passing both near support; crate front projection/latch count differs from near-half',generationId=gid,originalGeneratedPath=str(original),rawSha256=sha(rawpath));p.write_text(json.dumps(r,indent=2)+'\n')
raw=Image.open(rawpath).convert('RGBA');a=np.array(raw);xs=np.flatnonzero(np.sum(a[:,:,3]>=128,axis=0)>=2);groups=np.split(xs,np.flatnonzero(np.diff(xs)>8)+1);assert len(groups)==3
edges=[0]+[round((groups[i].max()+groups[i+1].min())/2) for i in range(2)]+[raw.width];cuts=[(edges[i],0,edges[i+1],raw.height) for i in range(3)];cells=[binary(raw.crop(c)) for c in cuts];nb=cells[-1].getbbox();scale=147/(nb[3]-nb[1]);out=BASE/'far-half-02-rejected';out.mkdir(exist_ok=True);names=['wrong-near-contact.png','wrong-near-passing.png','ruler.png'];records=[];frames=[]
for i,c in enumerate(cells):
    dense=binary(c.resize((round(c.width*scale),round(c.height*scale)),Image.Resampling.BOX));b=dense.getbbox();offset=(92-round((b[0]+b[2])/2),172-b[3]);f=Image.new('RGBA',(184,184));f.alpha_composite(dense,offset);assert np.count_nonzero(np.array(f)[:,:,3])==np.count_nonzero(np.array(dense)[:,:,3]);f.save(out/names[i]);fb=f.getbbox();frames.append(f);records.append({'file':names[i],'sourceCell':cuts[i],'wholeTranslation':offset,'bounds':fb,'size':[fb[2]-fb[0],fb[3]-fb[1]],'sha256':sha(out/names[i])})
(out/'recipe.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'rawSha256':sha(rawpath),'commonNeutralScale':scale,'neutralOccupiedTargetHeight':147,'records':records,'operations':'Three complete alpha128 cells,one neutral BOX scale,whole translations to bbox172,no clipped opaque pixels. No mirror/patch/recolour/per-pose fitting.','visualReview':'Both raw contact/passing repeat foreground thigh forward/right and near support. Crate now shows two latches/front face instead of previous single-latch side projection. Rejected correction; no assembled accepted cycle/native claim.'},indent=2)+'\n')
g=json.loads((S/'guide-provenance.json').read_text());idle=Image.open(ROOT/g['primarySourceFrames'][0]['path']).convert('RGBA');board=Image.new('RGB',(4*368,430),'#293b40');draw=ImageDraw.Draw(board)
for i,f in enumerate([idle]+frames):
    large=f.resize((368,368),Image.Resampling.NEAREST);board.paste(large,(i*368,45),large);draw.text((i*368+4,5),(['Selected East idle']+names)[i],fill='white')
board.save(out/'comparison.png');print(json.dumps({'scale':scale,'sizes':[r['size'] for r in records],'normalAdmission':False,'rejected':True}))
