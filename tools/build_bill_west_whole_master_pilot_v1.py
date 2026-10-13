"""Uniform export and whole-frame registration of one built-in authored pose."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,shutil,sys
R=Path(__file__).resolve().parents[1];D=R/'character/bill-west-whole-master-pilot-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
raw=Path(sys.argv[1]);shutil.copy2(raw,D/'raw-000.png')
refs=json.loads((D/'references.json').read_text());assert all(sha(Path(r['path']))==r['sha256'] and sha(R/r['source'])==r['sourceSha256'] for r in refs)
old=Image.open(R/refs[0]['source']).convert('RGBA');new=Image.open(raw).convert('RGBA').resize((256,256),Image.Resampling.LANCZOS)
def bounds(im):
 y,x=np.where(np.asarray(im)[:,:,3]>127);return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
ob=bounds(old);nb=bounds(new);shift=ob[3]-nb[3];packed=Image.new('RGBA',(256,256));packed.alpha_composite(new,(0,shift));assert np.count_nonzero(np.asarray(packed)[:,:,3])==np.count_nonzero(np.asarray(new)[:,:,3]);new=packed;nb=bounds(new);new.save(D/'candidate-000.png')
om=np.asarray(old)[:,:,3]>127;nm=np.asarray(new)[:,:,3]>127
report={'wholeAuthoredPose':True,'slot':0,'normalAdmission':False,'rawSource':str(raw),'rawSHA256':sha(raw),'rawSize':Image.open(raw).size,'uniformExportSize':[256,256],'wholeShiftY':shift,'beforeBounds':ob,'candidateBounds':nb,'heightDelta':(nb[3]-nb[1])-(ob[3]-ob[1]),'widthDelta':(nb[2]-nb[0])-(ob[2]-ob[0]),'silhouetteIoU':float((om&nm).sum()/(om|nm).sum()),'originalInputHashes':{r['source']:r['sourceSha256'] for r in refs},'candidateSHA256':sha(D/'candidate-000.png'),'scope':'One whole source material/identity pilot, uniform export and whole Y only. Not full loop or runtime installation.'}
board=Image.new('RGBA',(1200,650),'#1f2328');draw=ImageDraw.Draw(board)
for col,(label,im) in enumerate([('Original West master',Image.open(D/'master-reference.png').convert('RGBA').resize((256,256),Image.Resampling.LANCZOS)),('Previous preferred walk000',old),('Whole master-style walk000',new)]):
 x=col*400;draw.text((x+15,12),label,fill='white');board.alpha_composite(im,(x+72,38));draw.line((x+50,262,x+335,262),fill='#46b9c3');board.alpha_composite(im.crop((100,60,170,125)).resize((210,195),Image.Resampling.NEAREST),(x+80,320));small=im.resize((112,112),Image.Resampling.LANCZOS);board.alpha_composite(small,(x+135,530));draw.text((x+10,625),'Fixed H148; bottom pose preserved; no part fitting',fill='white')
board.save(D/'comparison.png');(D/'review.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
