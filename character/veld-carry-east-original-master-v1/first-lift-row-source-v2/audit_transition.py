from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[2];paths=sorted((P/'diagnostic-frames').glob('*.png'));assert len(paths)==6
master=Image.open(R/'character/veld-east-held-original-master-v1/frames/bare/000.png').convert('RGBA');frames=[Image.open(p).convert('RGBA') for p in paths]
def describe(im):
 a=np.array(im);y,x=np.where(a[:,:,3]>200);top=int(y.min());hx=np.where(a[top:top+16,:,3]>128)[1];tx=np.where(a[110:155,:,3]>200)[1];cloth=a[125:165,105:140];rgb=cloth[:,:,:3].astype(float);lum=rgb.mean(2);mask=(cloth[:,:,3]>200)&(np.ptp(rgb,axis=2)<18)&(lum>20)&(lum<160)
 floor=int(y.max());sx=np.where(a[floor,100:140,3]>200)[0]+100;far_y,far_x=np.where(a[200:225,143:185,3]>200)
 return {'height':int(y.max()-y.min()+1),'headWidth':int(hx.max()-hx.min()+1),'upperBodyWidth':int(tx.max()-tx.min()+1),'clothMedian':np.median(rgb[mask],axis=0).tolist(),'floor':floor,'nearSoleXs':sx.tolist(),'nearSoleMean':float(sx.mean()) if len(sx) else None,'distalFarBootBottom':int(far_y.max()+200) if len(far_y) else None}
rows=[{'pose':i,**describe(im)} for i,im in enumerate(frames)]
board=Image.new('RGB',(1792,800),(32,43,49));d=ImageDraw.Draw(board)
for i,(im,label) in enumerate([(master,'Original held')]+[(im,f'Pose{i}') for i,im in enumerate(frames)]):
 board.paste(im,(i*256,25),im);d.text((i*256+5,6),label,fill='white')
 crop=im.crop((98,185,182,232)).resize((252,141),Image.Resampling.NEAREST);board.paste(crop,(i*256+2,305),crop)
 crop=im.crop((101,75,167,163)).resize((198,264),Image.Resampling.NEAREST);board.paste(crop,(i*256+20,500),crop)
board.save(P/'whole-sequence-master-review.png')
frames[0].save(P/'source-preparation-review.png',save_all=True,append_images=frames[1:],duration=[70]*6,loop=1,disposal=0,blend=0)
replay=Image.open(P/'source-preparation-review.png');assert replay.n_frames==6
for i,im in enumerate(frames):replay.seek(i);assert np.array_equal(np.array(replay.convert('RGBA')),np.array(im));assert round(replay.info['duration'])==70
report={'originalMaster':describe(master),'rows':rows,'distinctFrameHashes':len({hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}),'reviewReplayChecks':12,'reviewReplayFailures':0,'scope':'Whole-source six-pose initial preparation diagnostic at prescribed70ms holds. Distinct file hashes alone do not prove authored motion progression; far heel/toe identity/contact, rigid near-foot, materials/proportions and native visual review still required. No completed start-stop/controller acceptance.'}
(P/'transition-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
