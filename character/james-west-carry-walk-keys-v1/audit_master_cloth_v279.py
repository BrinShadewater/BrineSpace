from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'master-cloth-audit-v279';out.mkdir(exist_ok=True);j=json.loads((p/'material-repair-progress.json').read_bytes());master=r/'character/james-west-master-carry-v1/registered-original-master.png';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
rows=[('Original master',master,[118,152,125,165])]
for phase,box in [(5,[134,150,141,160]),(10,[134,150,141,160]),(20,[131,148,138,160]),(25,[125,148,134,158]),(30,[119,149,127,155])]:
 study=next(row for row in j['thighConstructionStudies'] if row['phase']==phase)
 rows.append((f'Candidate{phase}',r/study['sources']['bare']['file'],box));rows.append((f'Old panel{phase}',r/j['states'][phase]['candidateSources']['bare']['file'],box))
board=Image.new('RGBA',(1408,384),(47,59,63,255));draw=ImageDraw.Draw(board);evidence=[]
for i,(label,f,box) in enumerate(rows):
 im=Image.open(f).convert('RGBA');patch=im.crop(tuple(box));a=np.asarray(patch);mask=a[:,:,3]>=250;rgb=a[:,:,:3][mask];luma=rgb@np.array([.2126,.7152,.0722]);marked=im.copy();ad=ImageDraw.Draw(marked);ad.rectangle((box[0],box[1],box[2]-1,box[3]-1),outline=(0,220,220,255));board.alpha_composite(marked.crop((104,136,152,184)).resize((120,120),Image.Resampling.NEAREST),(i*128,22));board.alpha_composite(patch.resize((112,176),Image.Resampling.NEAREST),(i*128,166));draw.text((i*128+3,3),label,fill='white');draw.text((i*128+3,348),f'med{np.median(luma):.1f}',fill='white')
 evidence.append(dict(label=label,file=f.relative_to(r).as_posix(),sha256=sha(f),clothSampleBox=box,opaqueSamples=int(mask.sum()),median=float(np.median(luma)),p95=float(np.percentile(luma,95)),rgbMedian=np.median(rgb,axis=0).tolist()))
board.save(out/'cloth-sample-review.png');(out/'inputs.json').write_text(json.dumps(dict(samples=evidence,scope='Selected tiny exposed-cloth diagnostic ROIs at native registration. Variable pose/illumination/seam content; not a grade or temporal acceptance. Nearest enlargement for review only; no raster grading or source edits.',normalChanged=False),indent=2)+'\n',encoding='utf-8');print(json.dumps([dict(label=row['label'],median=round(row['median'],2),p95=round(row['p95'],2)) for row in evidence]))
