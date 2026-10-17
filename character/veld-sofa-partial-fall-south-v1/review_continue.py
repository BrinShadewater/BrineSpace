from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-sofa-partial-south-continue-v1'
assert json.loads((O/'validation.json').read_text())['passed']
records=json.loads((O/'records.json').read_text());assert len(records)==24
bindings={};boards=[];pairs=0
for gear in ['bare','helmet']:
    for movement in ['sit','rise']:
        board=Image.new('RGB',(1080,988),'#202a30');draw=ImageDraw.Draw(board)
        for pose in range(6):
            name=f'{gear}-{movement}-pose{pose}';record=next(r for r in records if r['name']==name)
            for row,stage in enumerate(['living','before','after']):
                label=name+'-'+stage;source=O/(label+'-source.png');room=O/(label+'-room.png')
                for path in [source,room]:bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
                im=Image.open(source).convert('RGBA');canvas=Image.new('RGBA',(256,272));canvas.alpha_composite(im)
                small=canvas.resize((128,136),Image.Resampling.LANCZOS);x=pose*180;y=row*320
                board.paste(small,(x+26,y+18),small);board.paste(Image.open(room).convert('RGB').crop((490,286,660,424)),(x+5,y+165))
                draw.text((x+5,y+3),stage+' pose'+str(pose)+' / '+str(record['saveElapsed'])+'s',fill='white');pairs+=1
        filename=gear+'-'+movement+'-continue-review.png';board.save(P/filename);boards.append(filename)
for name in ['native.log','validation.json','records.json','inputs-before.json','inputs-after.json','profile-before.json','profile-after.json']:
    path=O/name;bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
(P/'continue-review-evidence.json').write_text(json.dumps({'boards':boards,'sourceNativePairs':pairs,'freshWorldDiskRestores':24,'futureActorTicks':7200,'checks':79775,'bindings':bindings,'visualReview':'pending','scope':'candidate injection on fresh normal scene; actual world mortality with paid survivor, ordinary RunSave disk/fresh-main and15020msreference+resumed steps percase; all6poses/both movements/gears. Prescribed sofa/paused-world, not title/new-process/natural hazards or normal partial admission'},indent=2)+'\n',encoding='utf-8')
print('4boards/72source-native pairs,24fresh restores/7200futureticks retained')
