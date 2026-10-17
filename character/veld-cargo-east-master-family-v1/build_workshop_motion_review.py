"""Pair recorded native snapshots at their simulation clocks; not continuous video."""
from pathlib import Path
import json,sys,math
from PIL import Image,ImageDraw,ImageSequence
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output'/sys.argv[1];D=P/(sys.argv[1]+'-review')
j=json.loads((O/'journeys.json').read_text());evidence=[]
for helmet in [False,True]:
    pair=[next(x for x in j['journeys'] if x['helmet']==helmet and x['candidate']==candidate) for candidate in [False,True]]
    captures=[[r for r in x['records'] if 'capture' in r] for x in pair]
    last=max(x['records'][-1]['step'] for x in pair)
    steps=sorted({r['step'] for rows in captures for r in rows}|{last})
    images=[];holds=[];records=[]
    for n,step in enumerate(steps):
        board=Image.new('RGB',(810,520),'#202a30');draw=ImageDraw.Draw(board)
        draw.text((10,8),f'Native recorded pose comparison / {"helmet" if helmet else "bare"} / {step/60:.2f}s',fill='white')
        draw.text((10,26),'Selected baseline',fill='white');draw.text((415,26),'Staged coordinated master turns',fill='white')
        names=[]
        for side,rows in enumerate(captures):
            row=next(r for r in reversed(rows) if r['step']<=step);name=row['capture']+'-native.png';names.append(name)
            native=Image.open(O/name).convert('RGB').crop((250,220,655,695));board.paste(native,(side*405,45))
        duration=round((steps[n+1] if n+1<len(steps) else last+30)*1000/60)-round(step*1000/60)
        images.append(board);holds.append(duration);records.append({'step':step,'durationMs':duration,'captures':names})
    tag='helmet' if helmet else 'bare';path=D/(tag+'-native-comparison.apng')
    images[0].save(path,format='PNG',save_all=True,append_images=images[1:],duration=holds,loop=0,disposal=0,blend=0)
    with Image.open(path) as decoded:
        frames=[frame.copy().convert('RGB') for frame in ImageSequence.Iterator(decoded)]
        assert len(frames)==len(images)
        assert all(a.tobytes()==b.tobytes() for a,b in zip(frames,images))
    evidence.append({'file':path.name,'frames':len(images),'durationMs':sum(holds),'records':records,'decodedPixelsExact':True})
(D/'motion-review-evidence.json').write_text(json.dumps({'scope':'Native captured state/slot snapshots held at recorded60Hz simulation clock boundaries. Repeating viewer resets; not uninterrupted native cadence or real-time gameplay acceptance. Baseline holds final idle while longer candidate completes.','exports':evidence},indent=2)+'\n',encoding='utf-8')
print(json.dumps([{k:x[k] for k in ['file','frames','durationMs','decodedPixelsExact']} for x in evidence]))
