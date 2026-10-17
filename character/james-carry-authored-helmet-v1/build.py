from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1];bareRoot=r/'character/james-carry-headcaps-v1';rect=(102,62,155,110)
names=['south','early-v2','middle-v2','late-v2','west'];bare=[];gear=[];bounds=[];sourceFiles=[]
for i,name in enumerate(names):
    bodyFile=bareRoot/'frames'/f'{i:03}.png';headFile=p/(name+'-helmet.png');body=Image.open(bodyFile).convert('RGBA');helmet=Image.open(headFile).convert('RGBA')
    aa=body.copy();bb=helmet.copy()
    for im in [aa,bb]:im.paste((0,0,0,0),rect)
    assert aa.tobytes()==bb.tobytes();bare.append(body);gear.append(helmet);bounds.append(helmet.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox());sourceFiles.extend([bodyFile,headFile])
    (p/'frames').mkdir(exist_ok=True);helmet.save(p/'frames'/f'{i:03}.png')
manifest=json.loads((bareRoot/'candidate-manifest.json').read_bytes());manifest['status']='candidate_unselected_paired_source_review_pending';manifest['name']='James authored carrying helmet provisional'
for state in manifest['states']:
    indices=range(5) if state['id']=='carry-turn-south-west' else reversed(range(5))
    state['frameFiles']=['res://'+(p/'frames'/f'{i:03}.png').relative_to(r).as_posix() for i in indices]
(p/'helmet-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
# Bare manifest retains exact existing tested full paths and timing.
(p/'bare-manifest.json').write_bytes((bareRoot/'candidate-manifest.json').read_bytes())
for suffix,region,scale in [('whole',(0,0,256,256),1),('head',(96,56,160,120),4)]:
    width=(region[2]-region[0])*scale;height=(region[3]-region[1])*scale;out=Image.new('RGBA',(width*5,(height+26)*2),(48,59,63,255));d=ImageDraw.Draw(out)
    for row,group in enumerate([bare,gear]):
        for i,im in enumerate(group):out.alpha_composite(im.crop(region).resize((width,height),Image.Resampling.NEAREST),(i*width,row*(height+26)+26));d.text((i*width+5,row*(height+26)+7),('bare ' if row==0 else 'helmet ')+names[i],fill='white')
    out.convert('RGB').save(p/('paired-'+suffix+'-chronology.png'))
station=[]
for body,helmet in zip(bare,gear):
    out=Image.new('RGBA',(1200,210),(48,59,63,255));d=ImageDraw.Draw(out)
    for mode,im in enumerate([body,helmet]):
        for j,height in enumerate([82,54,27]):
            size=round(256*height/148);x=mode*600+j*200+100;out.alpha_composite(im.resize((size,size),Image.Resampling.LANCZOS),(x-size//2,180-round(224*height/148)));d.text((x-70,16),('bare ' if mode==0 else 'helmet ')+str(height)+'px ruler',fill='white')
    station.append(out.convert('RGB'))
gallery=Image.new('RGB',(1200,1050))
for i,im in enumerate(station):gallery.paste(im,(0,i*210))
gallery.save(p/'paired-station-chronology.png')
for name,sequence in [('forward',station),('reverse',list(reversed(station)))]:
    file=p/(name+'-station-preview.apng');sequence[0].save(file,save_all=True,append_images=sequence[1:],duration=[100,200,200,200,600],loop=0);test=Image.open(file);assert test.n_frames==5
    for i,im in enumerate(sequence):test.seek(i);assert test.convert('RGB').tobytes()==im.tobytes();assert test.info['duration']==[100,200,200,200,600][i]
sources=sourceFiles+[p/'bare-manifest.json',p/'helmet-manifest.json',Path(__file__)]
report={'sourceSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in sources},'protectedOutsidePixelsPerPose':62992,'protectedOutsideExactAllFive':True,'headAdmissionRegion':rect,'helmetAlpha128Bounds':bounds,'bodyStandingRuler':148,'pivot':[128,224],'perPoseFit':False,'runtimeDurationMs':800,'previewDurationsMs':[100,200,200,200,600],'previewDecodeChecks':20,'visualReviewPending':True,'sourceAcceptance':False,'selected':False,'scope':'Two five-pose bare/helmet finite states, reused cardinal helmet masters and three new gear projections. Paired body outside head/collar exact. Source/native/actual cargo joins and owner/master acceptance not implied.'}
(p/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({'gearBounds':bounds,'pairedOutside':62992,'previewChecks':20}))
