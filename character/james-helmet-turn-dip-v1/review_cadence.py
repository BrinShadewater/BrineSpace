from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;o=p/'cadence';data=json.loads((o/'evidence.json').read_bytes())
pages=[];count=0;decoded=0
for case in data['cases']:
    samples=[s for s in case['samples'] if 'capture' in s];n=len(samples)
    board=Image.new('RGB',(2400,((n+3)//4)*184),'#303b40');d=ImageDraw.Draw(board);frames=[];durations=[]
    for i,s in enumerate(samples):
        im=Image.open(o/s['capture']).convert('RGB');assert im.size==(1200,320)
        x=i%4*600;y=i//4*184;board.paste(im.resize((600,160),Image.Resampling.LANCZOS),(x,y+24));d.text((x+4,y+4),f'{s["elapsed"]:.4f}s / source{s["indices"]}',fill='white')
        frames.append(im);duration=round((samples[i+1]['elapsed']-s['elapsed'])*1000) if i+1<n else 20
        assert duration>0;durations.append(duration);count+=1
    name=case['key']+'-cadence-contact.png';board.save(o/name);pages.append(name)
    preview=o/(case['key']+'-cadence-preview.png')
    frames[0].save(preview,save_all=True,append_images=frames[1:],duration=durations,loop=0)
    with Image.open(preview) as im:
        assert im.n_frames==len(frames)
        for i,f in enumerate(frames):
            im.seek(i);assert im.convert('RGB').tobytes()==f.tobytes();assert abs(im.info['duration']-durations[i])<.01;decoded+=1
report={'checks':data['checks'],'failures':data['failures'],'pairedNativePresentations':count,'pages':pages,'decodedPreviewRGBDurationChecks':decoded,'visualReviewPending':True,'continuousPlaybackWatched':False,'scope':data['scope'],'samplingIntervalMs':20,'elapsedCaptures':'Only source changes and last20ms before departure captured; all simulation samples bound by source hash/index.'}
(o/'review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
