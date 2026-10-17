"""Fit one authored head component; retain all protected V5 body and helmet pixels."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label
import json,hashlib,numpy as np,re
P=Path(__file__).resolve().parent;R=P.parent;V=P/'body-source'
sourceReview=json.loads((V/'review.json').read_text(encoding='utf-8'))
headPath=R/'bill-swim-west-master-v6/sources/canonical-bare-head-v1.png'
inputs=[Path(__file__),headPath,R/'bill-swim-west-master-v6/sources/master-head-isolated-v1.png',R/'bill-swim-west-master-v6/sources/master-head-isolation-prompt-v1.txt',R/'bill-swim-west-master-v6/prepare_head.py',R/'bill-swim-west-master-v6/head-component-review.json',R/'bill-land-water-west-v9/sources/master-head-reference.png',R/'crew-side-masters-v1/bill-side-master-01.png',V/'review.json',V/'index.html',R/'bill-land-water-west-v11/bare/frames/land-swim-west/005.png',R/'bill-land-water-west-v11/helmet/frames/land-swim-west/005.png']+[V/g/'manifest.json' for g in ['bare','helmet']]+[V/g/f'frames/swim-west/{i:03}.png' for g in ['bare','helmet'] for i in range(6)]
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
before={f.relative_to(R).as_posix():sha(f) for f in inputs}
donor=Image.open(headPath).convert('RGBA');assert donor.size==(21,23)
frames={'bare':[],'helmet':[]};fits=[]
for i,rec in enumerate(sourceReview['frames']):
    old=Image.open(V/f'bare/frames/swim-west/{i:03}.png').convert('RGBA');b=np.array(old)
    x,y=rec['registeredCrown'];position=[x-11,y]
    polygon=[(x-18,y-3),(x+18,y-3),(x+18,y+8),(x+3,y+25),(x-18,y+25)]
    mask=Image.new('L',old.size);ImageDraw.Draw(mask).polygon(polygon,fill=255);erase=np.array(mask)>0
    clean=b.copy();clean[erase]=0;new=Image.fromarray(clean);new.alpha_composite(donor,position);a=np.array(new)
    yy,xx=np.indices(b.shape[:2]);rgb=b[:,:,:3].astype(float);rr,gg,bb=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
    # Original grey collar can cross the short donor neck. Restore authored armour only.
    foreground=(yy>=y+11)&(xx>=x+2)&(b[:,:,3]>0)&(gg>=rr*.8)&(bb>=rr*.8)&(rgb.mean(axis=2)>30)
    foreground&=erase
    a[foreground]=b[foreground]
    region=Image.new('L',old.size);region.paste(donor.getchannel('A'),position);allowed=erase|(np.array(region)>0)
    assert np.array_equal(a[~allowed],b[~allowed])
    assert np.array_equal(a[foreground],b[foreground])
    assert np.array_equal(a[yy>=y+27],b[yy>=y+27])
    opaque=np.array(donor)[:,:,3]==255
    local=a[position[1]:position[1]+23,position[0]:position[0]+21]
    localForeground=foreground[position[1]:position[1]+23,position[0]:position[0]+21]
    assert np.array_equal(local[opaque&~localForeground],np.array(donor)[opaque&~localForeground])
    labels,_=label(a[:,:,3]>180);counts=np.bincount(labels.ravel());assert np.count_nonzero(counts[1:]>40)==1
    frames['bare'].append(Image.fromarray(a))
    helmet=Image.open(V/f'helmet/frames/swim-west/{i:03}.png').convert('RGBA');frames['helmet'].append(helmet)
    fits.append(dict(index=i,name=rec['name'],registeredHipMarker=rec['registeredHipMarker'],sourceCrown=[x,y],donorPosition=position,donorSize=donor.size,donorScale=1,donorRotationDegrees=0,erasePolygon=polygon,bodyOutsideHeadUnionExact=True,originalGreyCollarForegroundExact=True,belowHeadRegionExact=True,opaqueDonorPixelsExactOutsideCollarForeground=True,oneConnectedFigureAboveAlpha180=True,helmetFrameExactMatteBodyBank=True,scope='Authored donor reused at one calibrated physical scale; original master identity/collar and moving acceptance still subject to visual review.'))
for gear,bank in frames.items():
    out=P/gear;files=[]
    for i,im in enumerate(bank):
        path=out/f'frames/swim-west/{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);im.save(path);files.append(path.relative_to(out).as_posix())
    m=json.loads((V/gear/'manifest.json').read_text(encoding='utf-8'));m['name']='Bill West matte hardware and shared-head study';m['status']='source_candidate_unselected';m['states'][0]['frameFiles']=files;m['states'][0]['provenance']='Hip-registered V5 body protected; shared master-derived head component in bare bank, helmet fitted from matte body bank. Candidate only.'
    (out/'manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
    bank[0].save(out/'source-swim.png',save_all=True,append_images=bank[1:],duration=[160]*6,loop=0,disposal=0,blend=0)
    with Image.open(out/'source-swim.png') as ap:
        assert ap.n_frames==6 and ap.info['loop']==0
        for i,im in enumerate(bank):ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes() and ap.info['duration']==160
board=Image.new('RGB',(2112,720),'#182932');d=ImageDraw.Draw(board)
for row,gear in enumerate(['bare','helmet']):
    for i,im in enumerate(frames[gear]):
        board.paste(im,(i*352,row*360+25),im);d.text((i*352+4,row*360+4),gear+' / '+fits[i]['name'],fill='white')
board.save(P/'full-stroke-review.png')
detail=Image.new('RGB',(2400,700),'#182932');d=ImageDraw.Draw(detail)
for row,gear in enumerate(['bare','helmet']):
    for i,im in enumerate(frames[gear]):
        x,y=fits[i]['sourceCrown'];crop=im.crop((x-45,y-10,x+55,y+65)).resize((400,300),Image.Resampling.NEAREST)
        detail.paste(crop,(i*400,row*350+30),crop);d.text((i*400+4,row*350+4),gear+' / '+fits[i]['name']+' same4x',fill='white')
detail.save(P/'neck-review.png')
join=Image.new('RGB',(1408,720),'#182932');d=ImageDraw.Draw(join)
for row,gear in enumerate(['bare','helmet']):
    near=Image.open(R/f'bill-land-water-west-v11/{gear}/frames/land-swim-west/005.png').convert('RGBA')
    for col,(title,im) in enumerate([('Entry near-prone V11',near),('Shared-head extend',frames[gear][0]),('Glide',frames[gear][5]),('Wrap extend',frames[gear][0])]):
        join.paste(im,(col*352,row*360+25),im);d.text((col*352+4,row*360+4),gear+' / '+title,fill='white')
join.save(P/'entry-wrap-review.png')
assert before=={f.relative_to(R).as_posix():sha(f) for f in inputs}
report=dict(inputSHA256=before,frozenInputsStable=len(before),frames=fits,canvas=[352,320],pivot=[160,224],standingHeight=148,bodySourceDensity=148/956,decodedAPNGFramesExact=12,loopMs=960,helmetFramesExactMatteBodyBank=6,normalSelected=False,nativeAcceptance=False,visualAcceptance='Pending whole body/head/collar/grade/motion review; donor is authored master-derived, not original exact pixel extraction.')
(P/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
html=(V/'index.html').read_text(encoding='utf-8').replace('Bill west master swim loop study','Bill west shared-head swim study')
html=re.sub(r'<title>.*?</title>','<title>Bill West shared-head swim study</title>',html)
html=re.sub(r'<h1>.*?</h1>','<h1>Bill west - matte hardware and shared head</h1>',html)
html=html.replace('<section>','<p>Hip marker fixed across all six. Six matte-finish sources with stable hips and a shared head. Collar, master fidelity and motion are still under review. Collar, master fidelity, hardware grade and motion remain provisional.</p><section>',1)
html=html.replace('<h2>Head and collar</h2>','<h2>Original and authored head component</h2><img src="../bill-swim-west-master-v6/head-component-review.png"><h2>Head and collar</h2>')
html=re.sub(r'<p>Hip marker.*?</p>','<p>A quieter matte finish across the six poses, with stable hips and a shared head. Colour, posture and smoothness are still under review.</p>',html)
html=html.replace('<h2>Master and complete stroke</h2>','<p><a href="../bill-land-water-west-v12/">Review the matching water entry</a></p><h2>Complete stroke</h2>')
html=html.replace('<h2>Original and authored head component</h2>','<h2>Original master and material pass</h2><img src="master-material-review.png"><h2>Previous and matte bare bank</h2><img src="bare-material-comparison.png"><h2>Previous and matte helmet bank</h2><img src="helmet-material-comparison.png"><h2>Original and authored head component</h2>')
(P/'index.html').write_text(html,encoding='utf-8')
print(json.dumps(dict(frozenInputs=len(before),bodyProtectedFrames=6,helmetExactFrames=6,APNGDecodedExact=12,sharedDonorSize=donor.size)))
