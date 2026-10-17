"""Lossless native 30fps finite-sequence previews, with all frames retained."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-sofa-normal-motion-v1'
report=json.loads((O/'validation.json').read_text());assert report['passed']
records=json.loads((O/'records.json').read_text());assert len(records)==196
bindings={};boards=[];clips=[]
for gear in ['bare','helmet']:
    for prop in ['neutral','tablet']:
        name=gear+'-'+prop;board=Image.new('RGB',(1190,1106),'#202a30');d=ImageDraw.Draw(board);frames=[]
        for tick in range(49):
            source=O/(name+'-tick-%02d-source.png'%tick);native=O/(name+'-tick-%02d-room.png'%tick)
            for path in [source,native]:bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
            room=Image.open(native).convert('RGB').crop((490,286,660,424))
            x=tick%7*170;y=tick//7*158;board.paste(room,(x,y+20));d.text((x+3,y+3),'%02d / %.3fs'%(tick,tick/30),fill='white')
            frame=Image.new('RGB',(446,300),'#202a30');frame.paste(room,(266,42));im=Image.open(source).convert('RGBA');frame.paste(im,(0,20),im)
            draw=ImageDraw.Draw(frame);draw.text((6,3),name+' native / %.3fs'%(tick/30),fill='white');draw.text((266,188),'Exact native room crop',fill='white');draw.text((6,282),'30fps recorded actor stepping; repeat resets viewer',fill='white');frames.append(frame)
        boardpath=P/(name+'-motion-contact-sheet.png');board.save(boardpath);boards.append(boardpath.name)
        path=P/(name+'-native-motion.png')
        durations=[33 if tick%3!=2 else 34 for tick in range(48)]+[800]
        frames[0].save(path,save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=0,blend=0);clips.append(path.name)
for name in ['native.log','validation.json','records.json','inputs-before.json','inputs-after.json','profile-before.json','profile-after.json']:
    p=O/name;bindings[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
evidence={'clips':clips,'boards':boards,'nativeSourcePairs':196,'fps':30,'finiteMotionSeconds':1.6,'viewerTerminalHoldMs':800,'loopMeaning':'preview reset only, authored death is finite','losslessColor':True,'bindings':bindings,'visualReview':'pending','scope':'all native presentations of four normally selected paired prop/gear finite sequences; prescribed world mortality, paused world and actor stepping; no natural world scheduler/hazard or title/new-process proof'}
(P/'motion-review-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
(P/'motion-review.html').write_text('<!doctype html><meta charset="utf-8"><title>Veld sofa native motion</title><style>body{background:#202a30;color:#e0e8ec;font:16px system-ui;margin:24px}img{max-width:100%}p{max-width:85ch}</style><h1>Veld — normally selected sofa falls</h1><p>Lossless 30fps native/source recording. Both prop states and both gear versions. Each preview holds the floor pose, then resets; the authored fall remains finite. Prescribed mortality and paused-world actor stepping.</p>'+''.join('<p><img src="'+clip+'"></p><img src="'+board+'">' for clip,board in zip(clips,boards)),encoding='utf-8')
print(json.dumps({'clips':4,'nativeSourcePairs':196,'color':'lossless APNG; no GIF palette approximation'}))
