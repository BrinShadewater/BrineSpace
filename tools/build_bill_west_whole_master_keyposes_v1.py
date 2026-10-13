from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,shutil
R=Path(__file__).resolve().parents[1];D=R/'character/bill-west-whole-master-pilot-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
raws={12:'exec-d692dd47-5fec-4fb9-bb08-e366b42dc9e6.png',24:'exec-d5cb1d1f-f23f-41f7-95c4-a5db27bdb9a5.png',36:'exec-aa4bb720-23b1-451f-8ffb-d1f67022f4ea.png'};G=Path('C:/Users/Alex/.codex/generated_images/01a0ef89-cf35-77f0-9b57-2a08e6ea987f')
def bounds(a):
 y,x=np.where(a[:,:,3]>127);return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
records=[json.loads((D/'review.json').read_text())]
for slot,rawname in raws.items():
 P=D/f'pose-{slot:03}';raw=G/rawname;shutil.copy2(raw,P/'raw-preferred.png');refs=json.loads((P/'references.json').read_text());old=Image.open(R/refs[0]['source']).convert('RGBA');a=Image.open(raw).convert('RGBA').resize((256,256),Image.Resampling.LANCZOS);ob=bounds(np.asarray(old));nb=bounds(np.asarray(a));shift=ob[3]-nb[3];b=Image.new('RGBA',(256,256));b.alpha_composite(a,(0,shift));assert np.count_nonzero(np.asarray(a)[:,:,3])==np.count_nonzero(np.asarray(b)[:,:,3]);nb=bounds(np.asarray(b));b.save(D/f'candidate-{slot:03}.png');om=np.asarray(old)[:,:,3]>127;nm=np.asarray(b)[:,:,3]>127
 record={'slot':slot,'rawSHA256':sha(raw),'rawSize':Image.open(raw).size,'beforeBounds':ob,'candidateBounds':nb,'wholeShiftY':shift,'heightDelta':(nb[3]-nb[1])-(ob[3]-ob[1]),'widthDelta':(nb[2]-nb[0])-(ob[2]-ob[0]),'silhouetteIoU':float((om&nm).sum()/(om|nm).sum()),'candidateSHA256':sha(D/f'candidate-{slot:03}.png'),'beforeSource':refs[0]['source'],'beforeSHA256':refs[0]['sourceSha256'],'preferredGenerationRevision':2 if slot in [12,36] else 1}
 (P/'provenance.json').write_text(json.dumps(record,indent=2)+'\n');records.append(record)
board=Image.new('RGBA',(1600,870),'#1f2328');draw=ImageDraw.Draw(board)
for col,record in enumerate(records):
 slot=record['slot'];oldpath=record.get('beforeSource','character/bill-west-master-head-repair-v1/bare-walk-000-candidate.png')
 for row,(label,im) in enumerate([('Previous preferred',Image.open(R/oldpath).convert('RGBA')),('Whole master edit',Image.open(D/f'candidate-{slot:03}.png').convert('RGBA'))]):
  x=col*400;y=row*430;draw.text((x+12,y+6),f'{slot:03} {label}',fill='white');board.alpha_composite(im,(x+72,y+25));board.alpha_composite(im.crop((100,60,170,125)).resize((140,130),Image.Resampling.NEAREST),(x+55,y+290));board.alpha_composite(im.resize((100,100),Image.Resampling.LANCZOS),(x+255,y+310))
board.save(D/'keyposes-comparison.png');(D/'keyposes-review.json').write_text(json.dumps({'records':records,'preferredWholePoses':4,'rejectedGenerations':2,'normalAdmission':False,'scope':'Four landmarks only; not a48phase loop or natural/native contact acceptance.'},indent=2)+'\n');print(json.dumps([{'slot':r['slot'],'heightDelta':r['heightDelta'],'widthDelta':r['widthDelta'],'shift':r['wholeShiftY'],'iou':r['silhouetteIoU']} for r in records]))
