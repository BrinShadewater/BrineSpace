from pathlib import Path
import hashlib,json,math
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-north-original-motion-v1';D=P/'motion-review-v1';D.mkdir(exist_ok=True)
validation=json.loads((O/'validation.json').read_text());assert validation['passed']
data=json.loads((O/'records.json').read_text());records=data['records'];assert len(records)==180
bindings={};boards=[];decoded=0
for gear in ['bare','helmet']:
    rows=[r for r in records if r['gear']==gear];selected=[];seen=set();frames=[]
    for row in rows:
        for kind in ['native','source']:
            file=O/(row['name']+'-'+kind+'.png');bindings[file.relative_to(R).as_posix()]=hashlib.sha256(file.read_bytes()).hexdigest()
        frames.append(Image.open(O/(row['name']+'-native.png')).convert('RGB'))
        key=(row['action'],row['slot'])
        if key not in seen:selected.append(row);seen.add(key)
    path=D/(gear+'-continuous-native.apng')
    holds=[round((rows[i+1]['time']-r['time'])*1000) if i+1<len(rows) else 33 for i,r in enumerate(rows)]
    frames[0].save(path,format='PNG',save_all=True,append_images=frames[1:],duration=holds,loop=0,disposal=0,blend=0,optimize=False)
    with Image.open(path) as movie:
        assert movie.n_frames==len(frames)
        for i,frame in enumerate(frames):movie.seek(i);assert movie.convert('RGB').tobytes()==frame.tobytes();decoded+=1
    board=Image.new('RGB',(1440,500*math.ceil(len(selected)/4)),'#202a30');d=ImageDraw.Draw(board)
    for i,row in enumerate(selected):
        x=i%4*360;y=i//4*500;d.text((x+4,y+4),row['action']+' '+str(row['slot'])+' / '+str(round(row['time'],3))+'s',fill='white')
        native=Image.open(O/(row['name']+'-native.png')).convert('RGB');src=Image.open(O/(row['name']+'-source.png')).convert('RGBA').resize((96,96),Image.Resampling.LANCZOS)
        board.paste(src,(x+130,y+20),src);board.paste(native.crop((0,160,360,550)),(x,y+110))
    name=gear+'-all-movement-source-poses.png';board.save(D/name);boards.append({'gear':gear,'board':name,'distinctStateSourcePoses':len(selected),'records':[r['name'] for r in selected]})
(D/'review-evidence.json').write_text(json.dumps({'validation':validation,'samples':len(records),'decodedNativeFramesExact':decoded,'boards':boards,'bindings':bindings,'visualReview':'pending','scope':'Prescribed physical position trace using actual distance-driven sprite player, three carry cycles. Native47/93/148 presentations. No VeldNpc/controller/contact lock/world gameplay acceptance.'},indent=2)+'\n')
(D/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Veld North continuous movement</title><style>body{background:#202a30;color:#dce5e8;font:18px system-ui;margin:28px}img{max-width:100%}</style><h1>Veld North continuous movement</h1><p>One start, three carry strides and one stop on a continuous movement trace. The walking poses follow distance travelled. Bare and helmet views use the same body family. This is a sprite movement study; actual station routes and controller review remain open.</p><p><strong>Contact issue found:</strong> the planted boot slides during its support phase. This gait stays staged while foot placement is corrected against the original master.</p><p>Repeating previews reset after the final held pose.</p><h2>Bare</h2><img src="bare-continuous-native.apng"><h2>Helmet</h2><img src="helmet-continuous-native.apng"><h2>Every movement pose</h2><img src="bare-all-movement-source-poses.png"><img src="helmet-all-movement-source-poses.png">''')
print(f'{len(records)}continuous native samples decoded exactly;{sum(b["distinctStateSourcePoses"] for b in boards)}distinct movement poses retained.')
