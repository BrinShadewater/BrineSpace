from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-carry-west-master-proportions-v1'
assert json.loads((O/'validation.json').read_text(encoding='utf-8'))['passed']
records=json.loads((O/'records.json').read_text(encoding='utf-8'));assert len(records)==104
boards=[];bindings={};decoded=0
for gear in ['bare','helmet']:
    row=[x for x in records if x['gear']==gear];assert len(row)==52
    frames=[]
    for part in range(2):
        board=Image.new('RGB',(1080,1220),'#202a30');draw=ImageDraw.Draw(board)
        for tile,record in enumerate(row[part*26:(part+1)*26]):
            name=record['name'];native=O/(name+'-native.png');source=O/(name+'-source.png')
            for path in [native,source]:bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
            im=Image.open(native).convert('RGB');frames.append(im)
            src=Image.open(source).convert('RGBA').resize((96,96),Image.Resampling.LANCZOS)
            x=tile%6*180;y=tile//6*244
            draw.text((x+3,y+3),str(round(record['time'],3))+'s slot'+str(record['sourceIndex']),fill='white')
            board.paste(src,(x+42,y+16),src)
            board.paste(im.crop((160,455,340,585)),(x,y+114))
        filename=gear+'-native-motion-'+str(part+1)+'.png';board.save(P/filename);boards.append(filename)
    durations=[33 if n%3!=2 else 34 for n in range(52)]
    path=P/(gear+'-native-motion.apng')
    frames[0].save(path,format='PNG',save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=0,blend=0,optimize=False)
    with Image.open(path) as movie:
        assert movie.n_frames==52
        for i,frame in enumerate(frames):
            movie.seek(i);assert movie.convert('RGB').tobytes()==frame.tobytes();decoded+=1
for name in ['native.log','validation.json','records.json','inputs-before.json','inputs-after.json','profile-before.json','profile-after.json']:
    path=O/name;bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
(P/'motion-review-evidence.json').write_text(json.dumps({'boards':boards,'sourceNativePairs':104,'decodedNativeFramesExact':decoded,'bindings':bindings,'visualReview':'pending','scope':'Standalone real crew-player distance-driven clock,52native samples/both gear at30Hzsimulated time/1.7s,104exact native APNG frames. Review at47/93/148standing sizes. No real-world actor/controller/furniture/save/native continuous-cadence acceptance.'},indent=2)+'\n',encoding='utf-8')
html='''<!doctype html><meta charset="utf-8"><title>Veld West carry master proportions</title><style>body{background:#202a30;color:#e1e7eb;font:16px system-ui;margin:24px}img{max-width:100%}p{max-width:75ch}</style><h1>Veld West carry — master proportions candidate</h1><p>Unselected correction. Each native preview shows selected artwork above and candidate below, at 47, 93 and 148px standing rulers. Two cycles sampled through the actual crew-player distance clock; preview is lossless native capture, not a normal-world gameplay recording. The source head/face/bun now matches original side-master proportions. One pooled material pass, unchanged shared helmet. Original840msstride retained. Joins and world adoption remain under review.</p><h2>Source / shared helmet / original master</h2><img src="paired-master-contact.png"><h2>Bare native comparison</h2><img src="bare-native-motion.apng"><h2>Helmet native comparison</h2><img src="helmet-native-motion.apng"><h2>Cargo joins</h2><img src="cargo-join-review.png">'''
(P/'index.html').write_text(html,encoding='utf-8')
print('4chronological boards/104source-native pairs;104lossless native decode checks pass')
