"""Review actual normal-loader captures; never borrow staged test acceptance."""
from pathlib import Path
import json, hashlib, re
from PIL import Image, ImageDraw

P=Path(__file__).resolve().parent
R=P.parents[1]
O=R/'output/veld-sofa-partial-south-normal-continue-v1'
validation=json.loads((O/'validation.json').read_text(encoding='utf-8'))
assert validation['passed'] and validation['runtimePassed']
assert validation['targetedInputsUnchanged'] and not validation['realProfileChanges']
records=json.loads((O/'records.json').read_text(encoding='utf-8'))
assert len(records)==24 and len({r['name'] for r in records})==24
log=(O/'native.log').read_text(encoding='utf-8')
assert '0 failures;24 fresh disk restores' in log
bindings={};boards=[];pairs=0
for gear in ['bare','helmet']:
    for movement in ['sit','rise']:
        board=Image.new('RGB',(1080,988),'#202a30');draw=ImageDraw.Draw(board)
        for pose in range(6):
            name=f'{gear}-{movement}-pose{pose}'
            record=next(r for r in records if r['name']==name)
            for row,stage in enumerate(['living','before','after']):
                label=name+'-'+stage
                source=O/(label+'-source.png');room=O/(label+'-room.png')
                for path in [source,room]:
                    bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
                im=Image.open(source).convert('RGBA')
                assert im.size in [(256,256),(256,272)],(label,im.size)
                canvas=Image.new('RGBA',(256,272));canvas.alpha_composite(im)
                small=canvas.resize((128,136),Image.Resampling.LANCZOS)
                x=pose*180;y=row*320
                board.paste(small,(x+26,y+18),small)
                native=Image.open(room).convert('RGB')
                assert native.width>=660 and native.height>=424
                board.paste(native.crop((490,286,660,424)),(x+5,y+165))
                draw.text((x+5,y+3),stage+' pose'+str(pose)+' / '+str(record['saveElapsed'])+'s',fill='white')
                pairs+=1
        filename=gear+'-'+movement+'-normal-continue-review.png'
        board.save(P/filename);boards.append(filename)
for name in ['native.log','validation.json','records.json','inputs-before.json','inputs-after.json','profile-before.json','profile-after.json']:
    path=O/name;bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
evidence={'boards':boards,'sourceNativePairs':pairs,'freshWorldDiskRestores':24,
    'futureActorTicks':7200,'validation':validation,'bindings':bindings,
    'visualReview':'pending','scope':'Normal selected loader, no candidate injection; actual world mortality, ordinary RunSave disk/fresh-main and prescribed sofa activity with paid survivor. Does not prove natural chooser/traffic/hazard cadence, Title/new-process or full-library visual acceptance.'}
(P/'normal-continue-review-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
print('4 normal-loader boards / 72 source-native pairs retained; visual review pending')
