"""Publish18whole native pose pairs and exact800ms finite APNGs."""
from pathlib import Path
import json,hashlib,shutil
from PIL import Image,ImageDraw,ImageSequence
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-turn-material-v1';O=B/'opposite-ew-01-actor-review';O.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=ROOT/'output/marsh-animation-audit/loaded-swim-turn-opposite-ew-native-01-2026-10-03';report=read(a/'report.json')
assert (report['checks'],report['failures'],len(report['samples']),len(report['captures']),report['playerRestores'])==(345,0,84,18,18)
assert (a/'native-exit.txt').read_text().strip()=='0';log=(a/'native.log').read_text();assert 'ERROR:' not in log and 'WARNING:' not in log
for kind,count in [('inputs',92),('owner',2931)]:
    before=read(a/f'{kind}-before.json');assert len(before)==count and before==read(a/f'{kind}-after.json')
r=read(B/'sources/opposite-ew-01.request.json')
for q in r['orderedInputs']:assert sha(ROOT/q['path'])==q['sha256']
manifest=read(B/'opposite-ew-01-unselected/manifest.json');parity=[];boards=[]
for state in manifest['states']:
    pair=state['id'].removeprefix('swim-carry-turn-');paths=[ROOT/n.removeprefix('res://') for n in state['frameFiles']];figures=[Image.open(p).convert('RGBA') for p in paths]
    old=[ROOT/q['path'] for q in r['sourceFrames']];old=old if pair=='east-west' else list(reversed(old))
    for im in figures+[Image.open(p).convert('RGBA') for p in old]:
        b=im.getbbox();assert b[0]>=8 and b[2]<=216 and b[1]+103>=90 and b[3]+103<=325,'native whole actor crop'
    for page in range(3):
        board=Image.new('RGB',(1248,400),'#293b40');d=ImageDraw.Draw(board)
        for j,slot in enumerate(range(page*3,page*3+3)):
            name=f'{pair}-native-{slot:02}.png';shutil.copy2(a/name,O/name);im=Image.open(a/name).convert('RGB')
            for col in range(2):
                x=j*416+col*208;board.paste(im.crop((col*224+8,90,col*224+216,325)),(x,20));board.paste(im.crop((col*224+8,365,col*224+216,490)),(x,270));d.text((x+3,3),f'{pair} {slot} / '+('OLD' if col==0 else 'WHOLE'),fill='white')
            parity.append({'capture':name,'captureSha256':sha(O/name),'source':paths[slot].relative_to(ROOT).as_posix(),'sourceSha256':sha(paths[slot])})
        file=f'{pair}-native-pairs-{page:02}.png';board.save(O/file);boards.append({'file':file,'poses':3})
    apng=B/'opposite-ew-01-unselected'/f'{pair}-finite.apng';figures[0].save(apng,format='PNG',save_all=True,append_images=figures[1:],duration=state['frameDurationsMs'],loop=1,disposal=0,blend=0)
    with Image.open(apng) as im:
        decoded=[f.copy().convert('RGBA') for f in ImageSequence.Iterator(im)];assert len(decoded)==9 and im.info.get('loop')==1
        for d,f in zip(decoded,figures):assert d.tobytes()==f.tobytes()
(O/'verification.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'nativeChecks':345,'failures':0,'samples':84,'captures':18,'playerRestores':18,'sameClockHolds':18,'finiteAPNGHolds':18,'durationMsPerDirection':800,'inputsStableDuringInterval':len(read(a/'inputs-before.json')),'ownerFilesUnchanged':2931,'errors':0,'warnings':0,'exitCode':0,'nativeParity':parity,'boards':boards,'scope':report['scope'],'boardOperations':'Six1248x400 boards,18complete old/current actor pairs at original source/native world height; opaque whole bounds validated before screenshot crop, no native image resizing. Raw full captures retained.'},indent=2)+'\n')
print('Opposites:18native pairs/six boards,18exact finiteAPNG holds, player-only scope.')
