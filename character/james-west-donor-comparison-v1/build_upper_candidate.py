from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1]
report={'selected':False,'visualReviewPending':True,'newAuthoredPoses':0,'gears':{},'scope':'Existing coherent upper head/collar/shoulder donor regions placed at original native coordinates on original V9 four body/case intermediates. No scale/translation/grade or new raster painting; whole donor poses rejected for wider foot stance. Six80ms rows/exact endpoints retained. Not normal admission.'}
for gear in ['bare','helmet']:
    folder=r/'character/james-cargo-return-bridges-v1';m=json.loads((folder/f'{gear}-joined-manifest-v9.json').read_bytes());s=copy.deepcopy(m['states'][0])
    original_paths=[r/f[6:] if f.startswith('res://') else folder/f for f in s['frameFiles']]
    donor=r/'character/james-cargo-turn-south-west-v1';dm=json.loads((donor/(gear+'-manifest.json')).read_bytes());ds=next(st for st in dm['states'] if st['id']=='carry-turn-south-west')
    donors=[donor/ds['frameFiles'][4],donor/ds['frameFiles'][3],donor/ds['frameFiles'][3],original_paths[-1]]
    imlist=[Image.open(original_paths[0]).convert('RGBA')];paths=['res://'+original_paths[0].relative_to(r).as_posix()];details=[]
    for i,path in enumerate(donors):
        original=Image.open(original_paths[i+1]).convert('RGBA');source=Image.open(path).convert('RGBA');candidate=original.copy();candidate.paste(source.crop((104,64,162,134)),(104,64))
        oa=np.asarray(original);ca=np.asarray(candidate);protected=np.ones((256,256),bool);protected[64:134,104:162]=False;assert np.array_equal(oa[protected],ca[protected])
        dest=p/'upper-frames'/gear/f'{i:03d}.png';dest.parent.mkdir(parents=True,exist_ok=True);candidate.save(dest);paths.append('res://'+dest.relative_to(r).as_posix());imlist.append(candidate)
        details.append({'source':path.relative_to(r).as_posix(),'sourceSha256':hashlib.sha256(path.read_bytes()).hexdigest(),'original':original_paths[i+1].relative_to(r).as_posix(),'originalSha256':hashlib.sha256(original_paths[i+1].read_bytes()).hexdigest(),'protectedOriginalPixels':int(protected.sum())})
    paths.append('res://'+original_paths[-1].relative_to(r).as_posix());imlist.append(Image.open(original_paths[-1]).convert('RGBA'));s['frameFiles']=paths
    s['provenance']={'upperDonors':details,'coherentRegion':[104,64,162,134],'headOnlyOverlay':False,'newAuthoredPoses':0,'scaleOrTranslationOrGrade':False}
    m.update(name='James source-donor upper West bridge '+gear,status='unselected_upper_donor_source_trial',states=[s]);(p/(gear+'-upper-manifest.json')).write_text(json.dumps(m,indent=2)+'\n')
    board=Image.new('RGB',(1536,550),'#303b40');d=ImageDraw.Draw(board)
    for i,im in enumerate(imlist):
        bg=Image.new('RGBA',(256,256),'#303b40');bg.alpha_composite(im);board.paste(bg.convert('RGB'),(i*256,24));d.text((i*256+4,4),f'{gear} {i}',fill='white');board.paste(bg.convert('RGB').crop((96,56,160,120)).resize((256,256),Image.Resampling.NEAREST),(i*256,290))
    name=gear+'-upper-candidate.png';board.save(p/name);report['gears'][gear]={'donors':details,'board':name}
(p/'upper-review.json').write_text(json.dumps(report,indent=2)+'\n')
print('Paired source-donor upper trial preserves originalV9 body/foot/case outside coherent upper region; six original80ms rows.')
