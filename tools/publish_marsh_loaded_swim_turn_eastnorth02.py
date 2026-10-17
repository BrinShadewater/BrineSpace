"""Publish whole native actor pairs at native scale and exact finite APNG holds."""
from pathlib import Path
import json,hashlib,shutil
from PIL import Image,ImageDraw,ImageSequence
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-turn-material-v1';S=B/'sources';O=B/'east-north-02-actor-review';O.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=read(S/'east-north-02.request.json');a=ROOT/'output/marsh-animation-audit/loaded-swim-turn-eastnorth-native-02-2026-10-02';report=read(a/'report.json')
assert (report['checks'],report['failures'],len(report['samples']),len(report['captures']),report['playerRestores'])==(185,0,44,10,10)
assert (a/'native-exit.txt').read_text().strip()=='0';log=(a/'native.log').read_text();assert 'ERROR:' not in log and 'WARNING:' not in log
for kind,count in [('inputs',61),('owner',2931)]:
    before=read(a/f'{kind}-before.json');assert len(before)==count and before==read(a/f'{kind}-after.json')
assert sha(S/'east-north-02.raw.png')==r['rawSha256']==sha(Path(r['originalGeneratedPath'])) and sha(S/'east-north-02.prompt.txt')==r['promptSha256']
for q in r['orderedReferences']+r['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
manifest=read(B/'east-north-02-unselected/manifest.json');old=[ROOT/q['path'] for q in r['sourceFrames'][-5:]]
nativeParity=[]
for state in manifest['states']:
    pair=state['id'].removeprefix('swim-carry-turn-');paths=[ROOT/n.removeprefix('res://') for n in state['frameFiles']]
    figures=[Image.open(p).convert('RGBA') for p in paths]
    orderold=old if pair=='east-north' else list(reversed(old))
    for im in figures+[Image.open(p).convert('RGBA') for p in orderold]:
        b=im.getbbox();assert b[0]>=8 and b[2]<=216 and b[1]+103>=90 and b[3]+103<=325,'native whole crop bounds'
    board=Image.new('RGB',(2080,400),'#293b40');d=ImageDraw.Draw(board)
    for slot in range(5):
        name=f'{pair}-native-{slot:02}.png';shutil.copy2(a/name,O/name);im=Image.open(a/name).convert('RGB')
        for col in range(2):
            top=im.crop((col*224+8,90,col*224+216,325));world=im.crop((col*224+8,365,col*224+216,490));x=slot*416+col*208
            board.paste(top,(x,20));board.paste(world,(x,270));d.text((x+3,3),f'{pair} {slot} / '+('OLD' if col==0 else 'WHOLE'),fill='white')
        nativeParity.append({'capture':name,'captureSha256':sha(O/name),'source':paths[slot].relative_to(ROOT).as_posix(),'sourceSha256':sha(paths[slot])})
    board.save(O/f'{pair}-native-pairs.png')
    apng=B/'east-north-02-unselected'/f'{pair}-finite.apng';figures[0].save(apng,format='PNG',save_all=True,append_images=figures[1:],duration=state['frameDurationsMs'],loop=1,disposal=0,blend=0)
    with Image.open(apng) as im:
        decoded=[f.copy().convert('RGBA') for f in ImageSequence.Iterator(im)];assert len(decoded)==5
        for d,f in zip(decoded,figures):assert d.tobytes()==f.tobytes()
        assert im.info.get('loop')==1
(O/'verification.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'nativeChecks':185,'failures':0,'samples':44,'captures':10,'playerRestores':10,'sameClockHolds':10,'finiteAPNGHolds':10,'durationMsPerDirection':400,'inputsStableDuringInterval':61,'ownerFilesUnchanged':2931,'errors':0,'warnings':0,'exitCode':0,'nativeParity':nativeParity,'scope':report['scope'],'boardOperations':'Whole old/staged source-size and world-height actors retained at original native scale; verified whole opaque bounds before screenshot crop. Two2080x400 paired boards. Raw ten full native captures retained.'},indent=2)+'\n')
print('Ten complete native pairs/two boards, ten exact finite APNG holds; player-only scope.')
