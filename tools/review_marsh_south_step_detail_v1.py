"""Compare fixed-canvas whole-pose edits; never fit candidate occupied bounds."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-step-detail-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
oldpath=ROOT/'character/marsh-south-step-v1/candidate-05/003.png'
idlepath=ROOT/'character/marsh-south-idle-material-v1/candidate-01/000.png'
masterpath=ROOT/'character/marsh-motion-polish-v1/sources/south-standing-identity-01.png'
old=Image.open(oldpath).convert('RGBA');idle=Image.open(idlepath).convert('RGBA')
def opaque(im):return np.asarray(im)[:,:,3]>=128
def bounds(mask):return Image.fromarray((mask*255).astype('uint8')).getbbox()
records=[];candidates=[]
for version in ['01','02']:
    rawpath=BASE/f'candidate-{version}.raw.png';raw=Image.open(rawpath).convert('RGBA')
    assert raw.width==raw.height
    factor=184/raw.width
    im=raw.resize((184,184),Image.Resampling.LANCZOS)
    out=BASE/f'candidate-{version}-frame.png';im.save(out);candidates.append(im)
    a,b=opaque(old),opaque(im);bb=bounds(b);ob=bounds(a)
    records.append({'version':version,'rawPath':rawpath.relative_to(ROOT).as_posix(),'rawSha256':sha(rawpath),'framePath':out.relative_to(ROOT).as_posix(),'frameSha256':sha(out),'rawCanvas':list(raw.size),'rawOpaqueBounds':bounds(opaque(raw)),'fixedWholeCanvasFactor':factor,'opaqueBounds':bb,'originalOpaqueBounds':ob,'opaqueIoU':int((a&b).sum())/int((a|b).sum()),'heightRatio':(bb[3]-bb[1])/(ob[3]-ob[1]),'soleDisplacement':bb[3]-ob[3],'crownDisplacement':bb[1]-ob[1],'method':'One whole-canvas184/raw-width scale, no crop/pivot shift/pose fit/paint/splice/recolour/alpha repair.'})
master=Image.open(masterpath).convert('RGBA')
# Fixed original-master standing ruler, independent of any candidate pose bounds.
masterfactor=147/1232;master=master.resize((round(master.width*masterfactor),round(master.height*masterfactor)),Image.Resampling.LANCZOS)
board=Image.new('RGB',(5*184,214),'#293b40');d=ImageDraw.Draw(board)
for i,(name,im) in enumerate([('original master',master),('current own idle',idle),('selected phase3',old),('candidate01',candidates[0]),('candidate02',candidates[1])]):
    if i==0:board.paste(im,(i*184+31,25+round(172-1393*masterfactor)),im)
    else:board.paste(im,(i*184,25),im)
    d.text((i*184+3,5),name,fill='white')
board.save(BASE/'comparison-native.png');board.resize((1840,428),Image.Resampling.NEAREST).save(BASE/'comparison-2x.png')
neighbor=Image.new('RGB',(8*184,214),'#293b40');d=ImageDraw.Draw(neighbor)
sequence=[idle]+[Image.open(ROOT/f'character/marsh-south-step-v1/candidate-05/{i:03}.png').convert('RGBA') if i!=3 else candidates[1] for i in range(7)]
for i,im in enumerate(sequence):
    neighbor.paste(im,(184*i,25),im);d.text((184*i+3,5),'own idle' if i==0 else f'phase{i-1}'+(' candidate02' if i==4 else ' selected'),fill='white')
neighbor.save(BASE/'neighbors-candidate02.png')
(BASE/'fixed-canvas-comparison.json').write_text(json.dumps({'references':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in [oldpath,idlepath,masterpath]],'candidates':records,'masterDisplayScale':masterfactor,'masterStandingSourceRuler':1232,'normalAdmission':False,'fullGoalComplete':False,'visualReviewed':False},indent=2)+'\n')
print(json.dumps([{k:r[k] for k in ['version','opaqueBounds','heightRatio','opaqueIoU','soleDisplacement','crownDisplacement']} for r in records]))
