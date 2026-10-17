from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-north-east-helmet-aligned-v3';records=json.loads((O/'records.json').read_text());report=json.loads((O/'validation.json').read_text());assert report['passed'];checks=0;boards=[];movies=[]
for gear in ['bare','helmet']:
    group=[r for r in records if r['gear']==gear and r['action']=='north-east'];selected=[];seen=set()
    for r in group:
        if r['slot'] not in seen:seen.add(r['slot']);selected.append(r)
    assert len(selected)==6;board=Image.new('RGB',(1520,960),'#202a30');draw=ImageDraw.Draw(board)
    for i,r in enumerate(selected):
        im=Image.open(O/(r['name']+'-native.png')).convert('RGB').crop((0,312,760,600));x=(i%2)*760;y=(i//2)*320;board.paste(im,(x,y+25));draw.text((x+5,y+5),f'{gear} turn source{i}:47/93/148',fill='white')
    dest=P/(gear+'-native-source-poses.png');board.save(dest);boards.append({'file':dest.name,'gear':gear,'poses':6,'records':[r['name'] for r in selected]})
    for action in ['north-east','east-north']:
        frames=[Image.open(O/(r['name']+'-native.png')).convert('RGBA') for r in records if r['gear']==gear and r['action']==action];assert len(frames)==27
        path=P/(gear+'-'+action+'-native.apng');frames[0].save(path,format='PNG',save_all=True,append_images=frames[1:],duration=[1000/30]*len(frames),loop=1,disposal=0,blend=0)
        with Image.open(path) as movie:
            # Pillow legitimately merges identical adjacent native holds.
            decoded=[]
            for i in range(movie.n_frames):
                movie.seek(i);repeat=round(float(movie.info['duration'])/(1000/30));decoded.extend([movie.convert('RGBA').tobytes()]*repeat)
            assert len(decoded)==27
            for i,source in enumerate(frames):assert decoded[i]==source.tobytes();checks+=1
        movies.append(path.name)
(P/'native-review-evidence.json').write_text(json.dumps({'validation':report,'exactDecodedNativeSamples':checks,'boards':boards,'movies':movies,'visualReview':'pending','scope':'All12distinct paired source poses in native47/93/148boards; four finite motion comparisons108actual native captures. Not gather motion, East family join, gait contact, controller/world/save acceptance.'},indent=2)+'\n')
html='<!doctype html><meta charset="utf-8"><title>Veld original North–East pivot</title><style>body{background:#182229;color:#e5e9e8;font:18px system-ui;max-width:1500px;margin:30px auto;padding:20px}img{max-width:100%;display:block}a{color:#a5d5e9}</style><h1>Veld original North–East pivot study</h1><p>Exact original-guided body and endpoints, corrected intermediate helmet correspondence. North endpoint exactly matches reviewed gathered stance. Gather movement and East cargo-family join remain open; this is a staged turn study.</p><p>Intermediate helmet correspondence study: native visual review pending.</p>'
for gear in ['bare','helmet']:
    html+=f'<h2>{gear}: all six poses at game size</h2><img src="{gear}-native-source-poses.png" alt="{gear} six native turn poses">'
    for action in ['north-east','east-north']:html+=f'<h3>{gear} {action}: previous helmet fit above, yaw candidate below</h3><img src="{gear}-{action}-native.apng" alt="{gear} finite {action} native comparison">'
(P/'index.html').write_text(html);print(f'12distinct pose boards;{checks}native samples decode exact;four motion comparisons')
