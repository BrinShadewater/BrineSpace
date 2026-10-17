from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-carry-east-start-master-v2'
v=json.loads((O/'validation.json').read_text(encoding='utf-8'));assert v['passed']
records=json.loads((O/'records.json').read_text(encoding='utf-8'));assert len(records)==48
boards=[];movies=[];bindings={};decoded=0
for gear in ['bare','helmet']:
    for action in ['start','stop']:
        row=[r for r in records if r['gear']==gear and r['action']==action];assert len(row)==12
        name=gear+'-'+action;board=Image.new('RGB',(1080,488),'#202a30');draw=ImageDraw.Draw(board);frames=[]
        for i,record in enumerate(row):
            source=O/(record['name']+'-source.png');native=O/(record['name']+'-native.png')
            for path in [source,native]:bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
            im=Image.open(native).convert('RGB');frames.append(im)
            src=Image.open(source).convert('RGBA').resize((96,96),Image.Resampling.LANCZOS);x=i%6*180;y=i//6*244
            draw.text((x+3,y+3),str(round(record['time'],3))+'s slot'+str(record['sourceIndex']),fill='white')
            board.paste(src,(x+42,y+16),src);board.paste(im.crop((160,455,340,585)),(x,y+114))
        filename=name+'-native-review.png';board.save(P/filename);boards.append(filename)
        path=P/(name+'-native-review.apng');movies.append(path.name)
        if path.exists() and not (P/'native-review-evidence.json').exists() and not (P/(name+'-first-coalesced-check.apng')).exists():
            (P/(name+'-first-coalesced-check.apng')).write_bytes(path.read_bytes())
        groups=[]
        for i,frame in enumerate(frames):
            duration=[33,33,34][i%3]
            if groups and frame.tobytes()==groups[-1]['image'].tobytes():
                groups[-1]['duration']+=duration;groups[-1]['indices'].append(i)
            else:groups.append({'image':frame,'duration':duration,'indices':[i]})
        images=[g['image'] for g in groups];durations=[g['duration'] for g in groups]
        images[0].save(path,format='PNG',save_all=True,append_images=images[1:],duration=durations,loop=0,disposal=0,blend=0,optimize=False)
        with Image.open(path) as movie:
            assert movie.n_frames==len(groups)
            for i,group in enumerate(groups):
                movie.seek(i);assert abs(movie.info['duration']-group['duration'])<.001
                for index in group['indices']:
                    assert movie.convert('RGB').tobytes()==frames[index].tobytes();decoded+=1
        assert sum(durations)==400
for name in ['native.log','validation.json','records.json','inputs-before.json','inputs-after.json','profile-before.json','profile-after.json']:
    path=O/name;bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
(P/'native-review-evidence.json').write_text(json.dumps({'boards':boards,'movies':movies,'sourceNativePairs':48,'decodedNativeFramesExact':decoded,'validation':v,'bindings':bindings,'visualReview':'pending','scope':'actual standalone crew-player finite-clock/48native presentations,12 samples x 2 actions x 2 gears. 320msfinite transitions end held;400ms repeating viewer is preview reset, not authored action loop. No actual world/controller/prop ownership/normal adoption/save/full-set acceptance.'},indent=2)+'\n',encoding='utf-8')
print('4 chronological boards /48 source-native pairs;48 lossless native decode checks pass')
