from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
data=json.loads((p/'native/review.json').read_bytes());validation=json.loads((p/'native_probe-validation.json').read_bytes());assert data['failures']==0 and validation['realProfileUnchanged']
sourceReview=json.loads((p/'review.json').read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==h for k,h in sourceReview['sourceSha256'].items())
states=[]
for item in data['captures']:
    if item['state'] not in states:states.append(item['state'])
for state in states:
    rows=[v for v in data['captures'] if v['state']==state];assert [v['slot'] for v in rows]==list(range(5))
    board=Image.new('RGB',(1440,5*220),(48,59,63));d=ImageDraw.Draw(board)
    for row,item in enumerate(rows):
        native=Image.open(p/'native'/item['capture']).convert('RGB');assert native.size==(720,250)
        source=Image.open(r/item['source'].removeprefix('res://')).convert('RGBA');expected=Image.new('RGBA',(720,250),(48,59,63,255))
        for x,height in zip([120,310,480,620],[148,82,54,27]):
            sz=round(256*height/148);expected.alpha_composite(source.resize((sz,sz),Image.Resampling.BILINEAR),(round(x-128*height/148),round(225-224*height/148)))
        board.paste(native.crop((0,40,720,250)),(0,row*220+10));board.paste(expected.convert('RGB').crop((0,40,720,250)),(720,row*220+10))
        d.text((5,row*220),f'actual native {state} slot{item["slot"]} at{item["milliseconds"]}ms',fill='white');d.text((725,row*220),'matching source, same physical ruler (independent software sampler)',fill='white')
    board.save(p/('native-'+state+'-comparison.png'))
report={'checks':data['checks'],'failures':data['failures'],'clockSamples':data['clockSamples'],'sourceNativePairs':len(data['captures']),'nativeReportSha256':hashlib.sha256((p/'native/review.json').read_bytes()).hexdigest(),'sourceInventoryStableAfterNative':True,'profileUnchanged':True,'visualReviewPending':True,'selected':False,'sourceAcceptance':False,'scope':'Two bare candidate states standalone player;84prescribed20ms samples/10observed change captures. Source textures exact; software comparison is visual, not native RGB equivalence or continuous cadence. No helmet/normal loader/cargo room/Continue.'}
(p/'native-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print('354checks/0failures,84clock samples,10source/native pairs prepared; original profile and source inventory unchanged.')
