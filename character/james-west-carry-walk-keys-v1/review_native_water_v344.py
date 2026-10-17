from pathlib import Path
from PIL import Image,ImageDraw
import json
p=Path(__file__).resolve().parent;o=p/'water-native-review-v344'
v=json.loads((o/'native_probe-validation.json').read_bytes());assert v['exitCode']==0 and v['realProfileUnchanged'] and not v['timedOut']
d=json.loads((o/'native-review.json').read_bytes());assert d['failures']==0
boards=[]
for gear in ['bare','helmet']:
    for source in ['west','east','north','south']:
        targets=[x for x in ['west','east','north','south'] if x!=source]
        board=Image.new('RGB',(880,780),(48,59,64));draw=ImageDraw.Draw(board)
        for row,target in enumerate(targets):
            prefix=gear+'-'+source+'-'+target
            samples=[x for x in d['captures'] if x['file'].startswith(prefix+'-')]
            poses=[x for x in samples if x['file'] not in [prefix+'-stop.png',prefix+'-complete.png']]
            chosen=[next(x for x in samples if x['file']==prefix+'-stop.png'),poses[0],poses[len(poses)//2],next(x for x in samples if x['file']==prefix+'-complete.png')]
            for col,x in enumerate(chosen):
                im=Image.open(o/x['file']).convert('RGB');assert im.width>0 and im.height>0
                draw.text((col*220+5,row*260+5),prefix+' / '+['stop','entry','middle','complete'][col],fill='white')
                board.paste(im,(col*220+5,row*260+25))
        name=gear+'-'+source+'-native-comparison.png';board.save(o/name);boards.append(name)
(o/'visual-index.json').write_text(json.dumps({'boards':boards,'captures':len(d['captures']),'actuallyViewed':False,'scope':'Real native drawing at recorded prescribed stationary clocks; montage samples do not establish continuous motion.'},indent=2)+'\n',encoding='utf-8')
print(f'Built {len(boards)} native comparison boards from {len(d["captures"])} captures.')
