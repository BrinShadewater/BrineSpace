from pathlib import Path
import json,hashlib,sys
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];OUT=Path(sys.argv[1]).resolve()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def bounds(a):
 yy,xx=np.where(a);return [int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)] if len(xx) else None
q=json.loads((OUT/'generation-provenance-v1.json').read_text())
assert sha(Path(q['promptFile']))==q['promptSha256']==q['submittedPromptSha256']
assert sha(Path(q['savedPath']))==q['sha256']==sha(Path(q['originalPath']))
assert sha(Path(q['assessmentPath']))==q['assessmentSha256']
for ref in q['references']:assert sha(Path(ref['path']))==ref['sha256']
raw=Image.open(q['savedPath']).convert('RGBA');assert raw.width==raw.height
sheet=raw.resize((704,704),Image.Resampling.LANCZOS);sheet.save(OUT/'whole-sheet-normalized.png')
board=Image.new('RGBA',(1440,790),(31,35,40,255));d=ImageDraw.Draw(board);poses=[]
master=ROOT/'character/bill-west-master-head-audit-v1/master-sole-registered.png';authority=Image.open(master).convert('RGBA')
for col,p in enumerate(q['poses']):
 src=Path(p['sourcePath']);assert sha(src)==p['sourceSha256']
 original=Image.open(src).convert('RGBA');old=Image.new('RGBA',(352,352));old.alpha_composite(original,(32,0))
 cell=sheet.crop(p['cell']);candidate=cell.crop(p['originalCrop']);candidate.save(OUT/f"pose-{p['frame']:03}-candidate.png")
 new=Image.new('RGBA',(352,352));new.alpha_composite(candidate,(32,0))
 a=np.asarray(old)[:,:,3]>127;b=np.asarray(new)[:,:,3]>127;full=np.asarray(cell)[:,:,3]>127
 keep=np.zeros((352,352),dtype=bool);x,y,r,t=p['originalCrop'];keep[y:t,x:r]=True
 outside=int((full&~keep).sum());iou=float((a[115:]&b[115:]).sum()/(a[115:]|b[115:]).sum())
 record={'frame':p['frame'],'cell':p['cell'],'originalCrop':p['originalCrop'],'sourcePath':str(src),'sourceSha256':sha(src),'oldBounds':bounds(a),'candidateBounds':bounds(b),'opaquePixelsOutsideOriginalCanvas':outside,'bodyBelow115IoU':iou,'screeningPass':outside==0 and iou>=.9,'visualAcceptance':False}
 poses.append(record);x=col*360;d.text((x+5,10),f"Frame {p['frame']:03}: before / sheet candidate",fill='white')
 for y,im in [(35,old),(390,new)]:
  board.alpha_composite(im,(x,y));d.line((x+100,y+224,x+250,y+224),fill=(70,185,195))
 d.text((x+5,750),f"Body IoU {iou:.3f} | outside {outside}",fill='white')
board.save(OUT/'whole-figure-review.png')
heads=Image.new('RGBA',(1500,600),(31,35,40,255));hd=ImageDraw.Draw(heads)
for col,p in enumerate(q['poses']):
 old=Image.new('RGBA',(352,320));old.alpha_composite(Image.open(p['sourcePath']).convert('RGBA'),(32,0))
 new=Image.new('RGBA',(352,320));new.alpha_composite(Image.open(OUT/f"pose-{p['frame']:03}-candidate.png").convert('RGBA'),(32,0))
 for row,(name,im) in enumerate([('Before',old),('Sheet candidate',new)]):
  x=col*300;y=row*290;hd.text((x+10,y+10),f"{p['frame']:03} | {name}",fill='white');heads.alpha_composite(im.crop((120,55,200,135)).resize((240,240),Image.Resampling.NEAREST),(x+30,y+40))
hd.text((1210,10),'Physical master H148',fill='white');heads.alpha_composite(authority.crop((120,55,200,135)).resize((240,240),Image.Resampling.NEAREST),(1230,40));heads.save(OUT/'head-master-review.png')
report={'singleGenerationFourPoses':True,'rawSize':list(raw.size),'uniformNormalizationScale':704/raw.width,'masterComparisonPath':str(master),'masterComparisonSha256':sha(master),'poses':poses,'allScreeningPass':all(p['screeningPass'] for p in poses),'screeningMeaning':'Canvas/pose drift screen only, not identity, detail, contact or cadence acceptance.','normalAdmission':False,'nativeAcceptance':False,'fullVisualAcceptance':False}
(OUT/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
(OUT/'prompt-set.md').write_text('# Shared four-pose trial\n\nMethod: builtin imagegen; one generation, four posed cells.\n\n'+Path(q['promptFile']).read_text(encoding='utf-8')+'\n',encoding='utf-8')
(OUT/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Bill West shared head trial</title><style>body{background:#1f2328;color:#eee;font:17px sans-serif;margin:24px}img{max-width:100%}</style><h1>Bill West: shared four-pose head trial</h1><p>One fixed-sheet edit of phases25,31,32,37. Original canvas and source scale are preserved during extraction; body displacement or clipped poses are rejected. Source diagnostic only; no normal animation replacement.</p><h2>Whole figures and ground registration</h2><img src="whole-figure-review.png"><h2>Heads beside the original master</h2><img src="head-master-review.png"><p><a href="review.json">Pose screen</a> Â· <a href="prompt-set.md">Exact prompt, builtin imagegen</a></p>''',encoding='utf-8')
