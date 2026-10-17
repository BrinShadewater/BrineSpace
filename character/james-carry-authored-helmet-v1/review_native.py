from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
data=json.loads((p/'native/review.json').read_bytes());validation=json.loads((p/'native_probe-validation.json').read_bytes());inputs=json.loads((p/'native-inputs.json').read_bytes())
assert data['failures']==0 and validation['realProfileUnchanged'];assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==h for k,h in inputs['preLaunchSha256'].items())
groups=[]
for item in data['captures']:
    group=(item['equipment'],item['state'])
    if group not in groups:groups.append(group)
for equipment,state in groups:
    rows=[v for v in data['captures'] if v['state']==state and v['equipment']==equipment];assert [v['slot'] for v in rows]==list(range(5))
    label='helmet' if equipment else 'bare';board=Image.new('RGB',(1440,1100),(48,59,63));d=ImageDraw.Draw(board)
    for row,item in enumerate(rows):
        native=Image.open(p/'native'/item['capture']).convert('RGB');assert native.size==(720,250)
        source=Image.open(r/item['source'].removeprefix('res://')).convert('RGBA');expected=Image.new('RGBA',(720,250),(48,59,63,255))
        for x,height in zip([120,310,480,620],[148,82,54,27]):
            sz=round(256*height/148);expected.alpha_composite(source.resize((sz,sz),Image.Resampling.BILINEAR),(round(x-128*height/148),round(225-224*height/148)))
        board.paste(native.crop((0,40,720,250)),(0,row*220+10));board.paste(expected.convert('RGB').crop((0,40,720,250)),(720,row*220+10));d.text((5,row*220),f'actual native {label} {state} slot{item["slot"]} at{item["milliseconds"]}ms',fill='white');d.text((725,row*220),'matching source/ruler, independent software filtering',fill='white')
    board.save(p/('native-'+label+'-'+state+'-comparison.png'))
report={'checks':data['checks'],'failures':0,'clockSamples':data['clockSamples'],'sourceNativePairs':20,'comparisonBoards':4,'preLaunchInputsStable':True,'profileUnchanged':True,'visualReviewPending':True,'sourceAcceptance':False,'selected':False,'scope':'Paired standalone player,168prescribed20ms elapsed samples and20post-draw source-change captures, both directions/gears. Software source comparison not native RGB equivalence/continuous watched cadence; no normal loader, room/cargo dispatch/Continue.'}
(p/'native-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print('709/0paired native,168samples,20source/native pairs; frozen prelaunch sources/helpers/manifests and owner profile stable.')
