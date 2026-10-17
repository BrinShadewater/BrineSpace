from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'interior-detail-phase2-v77';out.mkdir(exist_ok=True)
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
base_file=p/'master-material-phase2-v69/bare-head-protected.png';source_file=p/'detail-phase2-v75/bare-head-protected.png'
base=np.asarray(Image.open(base_file).convert('RGBA'));source=np.asarray(Image.open(source_file).convert('RGBA'))
# Admit existing authored textile pixels only. No repaint, warp, grade or alpha edit.
boxes=[(134,115,148,132),(117,118,130,130),(120,151,136,163),(136,153,143,166),(123,187,136,198),(139,184,148,197)]
requested=np.zeros((256,256),bool)
for x0,y0,x1,y1 in boxes:requested[y0:y1,x0:x1]=True
interior=base[:,:,3]>=250
for dy in range(-2,3):
    for dx in range(-2,3):interior &= np.roll(np.roll(base[:,:,3]>=250,dy,axis=0),dx,axis=1)
mask=requested & interior & (source[:,:,3]>=250)
mask[130:156,90:139]=False # Original case/front grip/cuff region.
mask[:115]=False;mask[200:]=False
candidate=base.copy();candidate[mask,:3]=source[mask,:3]
assert np.array_equal(candidate[:,:,3],base[:,:,3])
assert np.array_equal(candidate[~mask],base[~mask])
assert np.array_equal(candidate[:115],base[:115]) and np.array_equal(candidate[200:],base[200:])
assert np.array_equal(candidate[130:156,90:139],base[130:156,90:139])
Image.fromarray(candidate).save(out/'bare-head-protected.png')
cap_file=p/'master-material-phase2-v69/helmet-head-protected.png';helmet_base=np.asarray(Image.open(cap_file).convert('RGBA'))
helmet=helmet_base.copy();helmet[mask,:3]=source[mask,:3]
assert np.array_equal(helmet[~mask],helmet_base[~mask])
assert np.array_equal(helmet[110:],candidate[110:])
Image.fromarray(helmet).save(out/'helmet-head-protected.png')
Image.fromarray((mask.astype(np.uint8)*255)).save(out/'admission-mask.png')
board=Image.new('RGBA',(1024,560),(47,58,63,255));draw=ImageDraw.Draw(board)
for row,mode in enumerate(['bare','helmet']):
    fs=[('before V69',p/f'master-material-phase2-v69/{mode}-head-protected.png'),('whole detail V75',p/f'detail-phase2-v75/{mode}-head-protected.png'),('interior admission V77',out/f'{mode}-head-protected.png'),('original stride2',p/f'master-head-review-v16/{mode}-002.png')]
    for col,(label,f) in enumerate(fs):
        board.alpha_composite(Image.open(f).convert('RGBA'),(col*256,row*280+24));draw.text((col*256+5,row*280+5),mode+' '+label,fill='white')
board.save(out/'paired-detail-admission-review.png')
board.resize((2048,1120),Image.Resampling.NEAREST).save(out/'enlarged-detail-admission-review.png')
ys,xs=np.where(candidate[:,:,3]>=128)
report=dict(sourceSha256={f.relative_to(r).as_posix():sha(f) for f in [base_file,source_file,cap_file]},boxes=boxes,admittedPixelCount=int(mask.sum()),unchangedOutsidePixels=int((~mask).sum()),changedPixels=int(np.any(candidate!=base,axis=2).sum()),alphaPlaneExact=True,outerTwoPixelRingProtected=True,headShoulderTop115Exact=True,bootsBelow200Exact=True,caseGripRegionExact=True,pairedBodyBelow110Exact=True,alpha128Bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],authoring='Existing V75generated textile source admitted only inside selected opaque V69panels. No new generation, invented painting, grading or geometry transform.',sourceAcceptance=False,normalChanged=False,fullGoalComplete=False)
(out/'package-review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['admittedPixelCount','unchangedOutsidePixels','changedPixels','alphaPlaneExact','alpha128Bounds','sourceAcceptance']}))
