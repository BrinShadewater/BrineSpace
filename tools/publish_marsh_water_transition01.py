"""Publish terminal finite player evidence and six exact whole APNG holds."""
from pathlib import Path
import json,hashlib,shutil,sys
from PIL import Image,ImageDraw,ImageSequence
ROOT=Path(__file__).resolve().parents[1];mode,side,revision=sys.argv[1:4];stem=f'{mode}-{side}-{revision}';B=ROOT/'character/marsh-water-transition-material-v1';O=B/(stem+'-actor-review');O.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=ROOT/f'output/marsh-animation-audit/water-{stem}-native-2026-10-03';r=read(a/'report.json')
assert r['failures']==0 and len(r['captures'])==6 and r['playerRestores']==6 and {q['slot'] for q in r['samples']}==set(range(6))
assert r['checks']==4+len(r['samples'])*3+6*4+2
assert (a/'native-exit.txt').read_text().strip()=='0';log=(a/'native.log').read_text();assert 'ERROR:' not in log and 'WARNING:' not in log
stable={}
for kind in ['inputs','owner']:
    before=read(a/f'{kind}-before.json');assert before==read(a/f'{kind}-after.json');stable[kind]=len(before)
request=read(B/f'sources/{stem}.request.json');recipe=read(B/f'{stem}-unselected/recipe.json')
assert sha(B/f'sources/{stem}.raw.png')==request['rawSha256']==sha(Path(request['originalGeneratedPath']))
for q in request['orderedReferences']+request['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
state=read(B/f'{stem}-unselected/manifest.json')['states'][0];paths=[ROOT/n.removeprefix('res://') for n in state['frameFiles']];figures=[Image.open(p).convert('RGBA') for p in paths]
old=[ROOT/q['path'] for q in request['sourceFrames'][-6:]]
for im in figures+[Image.open(p).convert('RGBA') for p in old]:
    b=im.getbbox();assert b[0]>=8 and b[2]<=216 and b[1]+103>=90 and b[3]+103<=325,'whole opaque native crop guard'
boards=[];parity=[]
for page in range(2):
    board=Image.new('RGB',(1248,400),'#293b40');d=ImageDraw.Draw(board)
    for j,slot in enumerate(range(page*3,page*3+3)):
        name=f'native-{slot:02}.png';shutil.copy2(a/name,O/name);im=Image.open(a/name).convert('RGB')
        for col in range(2):
            x=j*416+col*208;board.paste(im.crop((col*224+8,90,col*224+216,325)),(x,20));board.paste(im.crop((col*224+8,365,col*224+216,490)),(x,270));d.text((x+3,3),stem+' '+str(slot)+' / '+('OLD' if col==0 else 'WHOLE'),fill='white')
        parity.append({'capture':name,'captureSha256':sha(O/name),'source':paths[slot].relative_to(ROOT).as_posix(),'sourceSha256':sha(paths[slot])})
    name=f'native-pairs-{page:02}.png';board.save(O/name);boards.append(name)
apng=B/f'{stem}-unselected/{stem}-finite.apng';figures[0].save(apng,format='PNG',save_all=True,append_images=figures[1:],duration=state['frameDurationsMs'],loop=1,disposal=0,blend=0)
with Image.open(apng) as im:
    decoded=[f.copy().convert('RGBA') for f in ImageSequence.Iterator(im)];assert len(decoded)==6 and im.info.get('loop')==1
    for d,f in zip(decoded,figures):assert d.tobytes()==f.tobytes()
v={'normalAdmission':False,'fullGoalComplete':False,'nativeChecks':r['checks'],'samples':len(r['samples']),'captures':6,'playerRestores':6,'sameClockHolds':6,'finiteAPNGHolds':6,'inputsStableDuringInterval':stable['inputs'],'ownerFilesUnchanged':stable['owner'],'errors':0,'warnings':0,'failures':0,'exitCode':0,'nativeParity':parity,'boards':boards,'scope':r['scope'],'boardOperations':'Whole native actors retained at source size and65.28world height; opaque crop guard before screenshot crop, noresize. Six full native captures retained.'}
(O/'verification.json').write_text(json.dumps(v,indent=2)+'\n')
print(json.dumps({k:v[k] for k in ['nativeChecks','samples','captures','inputsStableDuringInterval','ownerFilesUnchanged']}))
