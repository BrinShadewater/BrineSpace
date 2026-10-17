from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
BASE=Path(__file__).resolve().parent;R=BASE.parents[1];P=BASE/'paired-package-v1';O=R/'output/veld-carry-east-master-proportions-native-v2'
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
html="""<!doctype html><meta charset="utf-8"><title>Veld East paired master carry</title><style>body{background:#202a30;color:#e1e7eb;font:16px system-ui;margin:24px}img{max-width:100%}p{max-width:75ch}</style><h1>Veld East carry — master helmet pairing</h1><p>Staged correction. Actual sprite-player captures compare selected art above and candidate below at 47, 93 and 148px standing rulers. Two cycles sampled using the distance clock. Recorded captures support source and alignment review; full world motion and adoption remain pending.</p><h2>Paired sources and helmet fit</h2><img src="paired-master-contact.png"><h2>Bare engine comparison</h2><img src="bare-native-motion.apng"><h2>Helmet engine comparison</h2><img src="helmet-native-motion.apng">"""
(P/'index.html').write_text(html,encoding='utf-8')
print('4 chronological boards / 104 source-native pairs; 104 lossless decoded native frames verified')
