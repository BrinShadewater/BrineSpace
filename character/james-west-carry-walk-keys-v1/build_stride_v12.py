from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, json, numpy as np

p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'paired-v12';out.mkdir(exist_ok=True)
donor=r/'character/crew-runtime-matte-v1/branforth/manifest.json'
dm=json.loads(donor.read_bytes());stride=dm['strideDistanceCells']['walk-west']
assert stride==0.1796875
files=[donor,Path(__file__)]
for kind in ('bare','helmet'):
    f=p/'paired-v11'/(kind+'-manifest.json');m=json.loads(f.read_bytes());files.append(f)
    m['name']='James West carrying full49 distance-stride '+kind+' provisional'
    m['strideDistanceCells']={'carry-west':stride}
    m['status']='candidate_unselected_distance_stride_review'
    assert sum(m['states'][0]['frameDurationsMs'])==1680
    (out/(kind+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n')

# Reuse the existing literal ordered normal-loader audit definitions only.
ns={'__file__':str(r/'character/james-carry-authored-helmet-v1/audit_joins.py')}
exec((r/'character/james-carry-authored-helmet-v1/audit_joins.py').read_text().split('rows=[]')[0],ns)
items=[];records=[]
for gear in (False,True):
    mf=out/('helmet-manifest.json' if gear else 'bare-manifest.json');m=json.loads(mf.read_bytes())
    standing=r/('character/james-carry-authored-helmet-v1/frames/004.png' if gear else 'character/james-carry-headcaps-v1/frames/004.png')
    if not gear:
        provisional=r/'character/james-west-master-carry-v1/local-v3-carry-pose.png'
        assert Image.open(standing).convert('RGBA').tobytes()==Image.open(provisional).convert('RGBA').tobytes()
        files.append(provisional)
    row=[]
    for label,f in [('standing / turn endpoint',standing),('new walk phase0',r/m['states'][0]['frameFiles'][0][6:]),('new walk phase48',r/m['states'][0]['frameFiles'][48][6:])]:
        files.append(f);row.append((Image.open(f).convert('RGBA'),label));records.append({'gear':gear,'label':label,'source':f.relative_to(r).as_posix()})
    for state in ('carry-west','unload-west'):
        im,ref=ns['load'](gear,state,0);row.append((im,'normal '+state+' first'));records.append({'gear':gear,'label':state,'source':ref})
    items.append(row)
for name,region,scale in [('whole',(0,0,256,256),1),('contact',(80,104,176,184),2)]:
    w=(region[2]-region[0])*scale;h=(region[3]-region[1])*scale
    board=Image.new('RGBA',(5*w,2*(h+28)),(48,59,63,255));d=ImageDraw.Draw(board)
    for y,row in enumerate(items):
        for x,(im,label) in enumerate(row):
            board.alpha_composite(im.crop(region).resize((w,h),Image.Resampling.NEAREST),(x*w,y*(h+28)+28))
            d.text((x*w+4,y*(h+28)+8),('helmet ' if y else 'bare ')+label,fill='white')
    board.convert('RGB').save(out/('joins-'+name+'.png'))
files+=ns['files']
report={'strideDistanceCells':stride,'strideSource':'original_selected_walk_west',
        'inputSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in set(files)},
        'joinSources':records,'standingEqualsAuthoredTurnEndpoint':True,
        'normalChanged':False,'sourceAcceptance':False,'visualMotionAcceptance':False,
        'joinVisualReviewPending':True,'scope':'Same original49-body leg sequence uses original selected walk distance stride; paired candidate only. Standing reference provisional, normal cargo joins still require art review.'}
(out/'review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'stride':stride,'unchangedArt':True,'joinReferences':len(records)}))
