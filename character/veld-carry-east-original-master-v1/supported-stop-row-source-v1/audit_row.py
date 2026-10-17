from pathlib import Path
from PIL import Image,ImageDraw
from scipy import ndimage
import json,numpy as np,hashlib
P=Path(__file__).resolve().parent;R=P.parents[2]
raw=Image.open(P/'raw-supported-stop-v1.png').convert('RGBA');assert raw.size==(1536,1024)
cells=[raw.crop(((i%3)*512,(i//3)*512,(i%3+1)*512,(i//3+1)*512)) for i in range(6)]
def main_geometry(im):
 a=np.array(im);labels,k=ndimage.label(a[:,:,3]>200);counts=np.bincount(labels.ravel());counts[0]=0;mask=labels==int(counts.argmax());y,x=np.where(mask);assert len(x)>100
 top=int(y.min());bottom=int(y.max());hx=np.where(mask[top:top+16])[1]
 return {'height':bottom-top+1,'top':top,'bottom':bottom,'headBandWidth':int(hx.max()-hx.min()+1),'headBandAxis':float((hx.min()+hx.max())/2),'mask':mask}
anchor=main_geometry(cells[5]);scale=148/anchor['height'];side=round(512*scale);anchor_im=cells[5].resize((side,side),Image.Resampling.LANCZOS);g=main_geometry(anchor_im);dx=round(123.5-g['headBandAxis']);dy=223-g['bottom']
frames=[];rows=[];board=Image.new('RGB',(1536,700),(32,43,49));d=ImageDraw.Draw(board)
manifest=json.loads((P.parent/'bare-key-manifest.json').read_text());master=Image.open(R/manifest['states'][1]['frameFiles'][0][6:]).convert('RGBA')
for i,im in enumerate(cells):
 out=Image.new('RGBA',(256,256));out.alpha_composite(im.resize((side,side),Image.Resampling.LANCZOS),(dx,dy));dest=P/f'frames/{i:03}.png';dest.parent.mkdir(exist_ok=True);out.save(dest);frames.append(out)
 geo=main_geometry(out);a=np.array(out);top=geo['top'];mask=geo['mask'];tx=np.where(mask[top+34:top+79])[1]
 outside=(a[:,:,3]>5)&~ndimage.binary_dilation(mask,iterations=3)
 rows.append({'cell':i,'height':geo['height'],'headBandWidth':geo['headBandWidth'],'headBandAxis':geo['headBandAxis'],'top':top,'floor':geo['bottom'],'upperBandWidth':int(tx.max()-tx.min()+1),'partialAlphaOutsideDilatedBodyPixels':int(outside.sum()),'alphaMax':int(a[:,:,3].max())})
 board.paste(out,(i*256,25),out);d.text((i*256+3,4),f"cell{i} H{geo['height']} head{geo['headBandWidth']}",fill='white');crop=out.crop((75,65,180,231)).resize((210,332),Image.Resampling.NEAREST);board.paste(crop,(i*256+3,330),crop)
board.save(P/'registered-six-pose-review.png')
comparison=Image.new('RGB',(1024,750),(32,43,49));d=ImageDraw.Draw(comparison)
for i,(label,im) in enumerate([('Original master',master),('Exact walking entry',Image.open(P/'walking-entry-reference.png').convert('RGBA')),('Generated entry',frames[0]),('Generated standing',frames[5])]):
 comparison.paste(im,(i*256,25),im);d.text((i*256+3,3),label,fill='white');crop=im.crop((95,70,175,165)).resize((240,285),Image.Resampling.NEAREST);comparison.paste(crop,(i*256+3,335),crop)
comparison.save(P/'original-anchor-comparison.png')
frozen=json.loads((R/'output/veld-east-grounded-flat-probe-v1/inputs-after.json').read_text());assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in frozen.items())
report={'grid':[3,2],'rawSize':list(raw.size),'globalRulerFromGeneratedStanding':{'heightRaw':anchor['height'],'scale':scale,'uniformCellSize':[side,side],'fixedOffset':[dx,dy]},'rows':rows,'scope':'All six whole cells retained including generated partial-alpha glow. One whole-sheet standing ruler used for all cells; no per-pose recenter/density, alpha/colour/body edits. Measurements alpha>200 largest body component; semitransparent exterior separately counted. Native rendering not run.','priorNativeInputsUnchanged':len(frozen)}
(P/'AUDIT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
