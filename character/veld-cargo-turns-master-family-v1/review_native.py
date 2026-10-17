from pathlib import Path
import json,hashlib,sys
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
pair=sys.argv[1] if len(sys.argv)>1 else 'south-west'
assert pair in ['south-west','north-west','north-east','east-south']
D=P/{'south-west':'candidate-v7','north-west':'north-west-candidate-v4','north-east':'north-east-candidate-v5','east-south':'east-south-candidate-v3'}[pair]
O=R/{'south-west':'output/veld-cargo-turns-master-family-v7-native-r3','north-west':'output/veld-cargo-turns-north-west-v4-native','north-east':'output/veld-cargo-turns-north-east-v5-native','east-south':'output/veld-cargo-turns-east-south-v3-native'}[pair]
validation=json.loads((O/'validation.json').read_text(encoding='utf-8'));assert validation['passed']
records=json.loads((O/'records.json').read_text(encoding='utf-8'));assert len(records)==104
bindings={};boards=[];movies=[];decoded=0
for gear in ['bare','helmet']:
    for action in [pair,'-'.join(reversed(pair.split('-')))]:
        row=[r for r in records if r['gear']==gear and r['action']==action];assert len(row)==26
        name=gear+'-'+action;board=Image.new('RGB',(1080,1220),'#202a30');draw=ImageDraw.Draw(board);frames=[]
        for i,record in enumerate(row):
            source=O/(record['name']+'-source.png');native=O/(record['name']+'-native.png')
            for path in [source,native]:bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
            im=Image.open(native).convert('RGB');frames.append(im);src=Image.open(source).convert('RGBA').resize((96,96),Image.Resampling.LANCZOS);x=i%6*180;y=i//6*244
            draw.text((x+3,y+3),str(round(record['time'],3))+'s slot'+str(record['sourceIndex']),fill='white')
            board.paste(src,(x+42,y+16),src);board.paste(im.crop((160,455,340,585)),(x,y+114))
        filename=name+'-native-review.png';board.save(D/filename);boards.append(filename)
        groups=[]
        for i,frame in enumerate(frames):
            duration=[33,33,34][i%3]
            if groups and frame.tobytes()==groups[-1]['image'].tobytes():groups[-1]['duration']+=duration;groups[-1]['indices'].append(i)
            else:groups.append({'image':frame,'duration':duration,'indices':[i]})
        moviepath=D/(name+'-native-review.apng');movies.append(moviepath.name)
        images=[g['image'] for g in groups];durations=[g['duration'] for g in groups]
        images[0].save(moviepath,format='PNG',save_all=True,append_images=images[1:],duration=durations,loop=0,disposal=0,blend=0,optimize=False)
        with Image.open(moviepath) as movie:
            assert movie.n_frames==len(groups)
            for i,group in enumerate(groups):
                movie.seek(i);assert abs(movie.info['duration']-group['duration'])<.001
                for index in group['indices']:assert movie.convert('RGB').tobytes()==frames[index].tobytes();decoded+=1
        assert sum(durations)==866
for name in ['native.log','validation.json','records.json','inputs-before.json','inputs-after.json','profile-before.json','profile-after.json']:
    path=O/name;bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
(D/'native-review-evidence.json').write_text(json.dumps({'boards':boards,'movies':movies,'sourceNativePairs':104,'decodedNativeSamplesExact':decoded,'validation':validation,'bindings':bindings,'visualReview':'pending','scope':'standalone actual player finite-clock 26samples x2directions x2gears. Original800ms runtime;866ms repeating preview includes terminal hold and viewer reset. No controller/world/cargo ownership/save/normal adoption/full-set acceptance.'},indent=2)+'\n',encoding='utf-8')
html='''<meta charset="utf-8"><title>Veld master South-West turn</title><style>body{background:#202a30;color:#e1e7eb;font:16px system-ui;margin:24px}img{max-width:100%}a{color:#9ccbea}p{max-width:75ch}</style><h1>Veld master South–West turn candidate</h1><p>Unselected paired source repair, compact original head proportions, coherent scanner/cylinder handedness and planted adjacent feet. Existing shared helmet construction retained; whole corrected West held pose reused at endpoint. Original800ms finite turn/reverse. Native previews show selected above/candidate below at47/93/148 standing rulers. These are prescribed standalone player samples, not normal-world gameplay or real-time cadence evidence.</p><img src="paired-turn-contact.png">'''
if pair=='north-west':html=html.replace('South–West','North–West')
if pair=='north-east':
    html=html.replace('South–West','North–East').replace('South-West','North-East').replace('corrected West held pose','corrected North held pose').replace('scanner/cylinder handedness','scanner/cylinder handedness through rear-to-right rotation')
if pair=='east-south':
    html=html.replace('South–West','East–South').replace('South-West','East-South').replace('Existing shared helmet construction retained; whole corrected West held pose reused at endpoint.','Revised angular helmet source follows side-to-front rotation; exact whole East and South held frames reused at endpoints.')
for name in movies:html+='<h2>'+name.replace('-native-review.apng','')+'</h2><img src="'+name+'">'
html+='<p>Shared cardinal/half-turn joins, complete source/library polish and actual controller/room cargo lifecycle remain open.</p>'
(D/'index.html').write_text(html,encoding='utf-8')
print('4chronologicalboards/104source-native presentations;104 exact native RGB decode bindings/866ms preview checks pass')
