"""Preserve every recorded native frame in lossless finite-sequence previews."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-sofa-partial-south-motion-v1'
report=json.loads((O/'validation.json').read_text());assert report['passed']
records=json.loads((O/'records.json').read_text());assert len(records)==1176
bindings={};boards=[];clips=[]
for gear in ['bare','helmet']:
    for movement in ['sit','rise']:
        for pose in range(6):
            name=f'{gear}-{movement}-pose{pose}';case=[r for r in records if r['name']==name]
            assert [r['tick'] for r in case]==list(range(49))
            board=Image.new('RGB',(1190,1106),'#202a30');draw=ImageDraw.Draw(board);frames=[]
            for tick in range(49):
                stem=name+'-tick-%02d'%tick;source=O/(stem+'-source.png');native=O/(stem+'-room.png')
                for path in [source,native]:bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
                room=Image.open(native).convert('RGB').crop((490,286,660,424))
                x=tick%7*170;y=tick//7*158;board.paste(room,(x,y+20));draw.text((x+3,y+3),'%02d / %.3fs'%(tick,tick/30),fill='white')
                frame=Image.new('RGB',(446,300),'#202a30');frame.paste(room,(266,42));im=Image.open(source).convert('RGBA');frame.paste(im,(0,20),im)
                d=ImageDraw.Draw(frame);d.text((6,3),name+' / %.3fs'%(tick/30),fill='white');d.text((266,188),'Exact native room crop',fill='white');d.text((6,282),'30fps actor stepping; repeat resets viewer only',fill='white');frames.append(frame)
            filename=name+'-motion-contact-sheet.png';board.save(P/filename);boards.append(filename)
            filename=name+'-native-motion.png';durations=[33 if tick%3!=2 else 34 for tick in range(48)]+[800]
            frames[0].save(P/filename,save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=0,blend=0);clips.append(filename)
for name in ['native.log','validation.json','records.json','inputs-before.json','inputs-after.json','profile-before.json','profile-after.json']:
    path=O/name;bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
evidence={'clips':clips,'boards':boards,'nativeSourcePairs':1176,'fps':30,'finiteMotionSeconds':1.6,'viewerTerminalHoldMs':800,'loopMeaning':'preview resets; authored fall remains finite','losslessColor':True,'bindings':bindings,'visualReview':'pending','scope':'all24staged paired partial sit/rise deaths with49recorded actor-stepped presentations each; actual world mortality/default sofa, not natural cadence/new-process or normal selection'}
(P/'motion-review-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
(P/'motion-review.html').write_text('<!doctype html><meta charset="utf-8"><title>Veld partial sofa native motion</title><style>body{background:#202a30;color:#e0e8ec;font:16px system-ui;margin:24px}img{max-width:100%}p{max-width:85ch}</style><h1>Veld — partial sit/rise falls</h1><p>All six partial entrances, both movements and both equipment versions. Lossless native/source30fps recording. Preview repeats reset the viewer only; the authored fall is finite. Staged sources; continuous review and normal admission pending.</p>'+''.join('<p>'+clip+'<br><img src="'+clip+'"></p><img src="'+board+'">' for clip,board in zip(clips,boards)),encoding='utf-8')
print('24lossless previews/contact sheets;1176source-native frames retained')
