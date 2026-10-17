"""Exact native travel replay and measured-window comparison; no art mutations."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[2];N=R/'output/veld-east-phase-probe-v1'
records=json.loads((N/'records.json').read_text(encoding='utf-8'))['records']
material=json.loads((P/'support-material-diagnostic-v2.json').read_text(encoding='utf-8'))
checks=0;results=[]
for trial,label in enumerate(['uniform','paced']):
    for gear in ['bare','helmet']:
        rows=[r for r in records if r['trial']==trial and r['gear']==gear]
        frames=[Image.open(N/(r['name']+'-native.png')).convert('RGBA') for r in rows]
        # Exact timestamped samples from player; durations between pose midpoints.
        boundaries=[round(r['time']*1000) for r in rows]
        durations=[max(1,b-a) for a,b in zip(boundaries,boundaries[1:])]+[30]
        target=P/f'{gear}-{label}-native-travel.png'
        frames[0].save(target,save_all=True,append_images=frames[1:],duration=durations,loop=1,disposal=0,blend=0)
        with Image.open(target) as replay:
            assert replay.n_frames==len(frames)
            for i in range(len(frames)):
                replay.seek(i);assert replay.convert('RGBA').tobytes()==frames[i].tobytes();assert abs(replay.info['duration']-durations[i])<.01;checks+=2
        # Full first cycle, source-registered crop of actual native148px display.
        board=Image.new('RGB',(1040,1310),'#202a30');draw=ImageDraw.Draw(board)
        draw.text((12,8),f'{gear} / {label} / actual native148px / all37 poses, first cycle',fill='white')
        for k,r in enumerate(rows[1:38]):
            root=120+r['travelWorld']*148/65.28
            im=Image.open(N/(r['name']+'-native.png')).crop((round(root-65),407,round(root+65),572))
            x=(k%8)*130;y=(k//8)*215+45
            board.paste(im,(x,y+22));draw.text((x+3,y),f"raw{r['rawSlot']}",fill='white')
        board.save(P/f'native-{gear}-{label}-full-cycle.png')
        support=Image.new('RGB',(900,720),'#202a30');d=ImageDraw.Draw(support)
        d.text((10,8),f'{gear} / {label} / actual native93px ground points (unshifted)',fill='white')
        selected=[]
        for win in material['windows'][:2]:
            for slot in range(win['frames'][0],win['frames'][1]+1):selected.append(next(r for r in rows[1:38] if r['rawSlot']==slot))
        for k,r in enumerate(selected):
            # Preserve screen X so stationary-foot evidence can be assessed.
            im=Image.open(N/(r['name']+'-native.png')).crop((100,275,390,335))
            x=(k%2)*450;y=(k//2)*90+45;support.paste(im,(x,y+16));d.text((x+4,y),f"raw{r['rawSlot']}",fill='white')
        support.save(P/f'native-{gear}-{label}-support-windows.png')
        spans=[]
        for cycle in range(2):
            for win in material['windows'][:2]:
                for key in ['toeCap','ankleStrap']:
                    points=[]
                    for landmark in win[key]['rows']:
                        r=next(r for r in rows if r['sample']>0 and (r['sample']-1)//37==cycle and r['rawSlot']==landmark['frame'])
                        points.append(120+r['travelWorld']*93/65.28+(landmark['nativeX']-128)*93/148)
                    spans.append({'cycle':cycle,'frames':win['frames'],'material':key,'actualPlayerRootPlusSourceLandmarkSpanAt93px':max(points)-min(points)})
        results.append({'gear':gear,'timing':label,'captureCount':len(rows),'replayMs':sum(durations),'supportSpans':spans})
# Boundary comparison retains actual root position and three-scale rendering.
board=Image.new('RGB',(1800,1240),'#202a30');d=ImageDraw.Draw(board)
for row,(gear,sample) in enumerate([('bare',37),('bare',38),('helmet',37),('helmet',38)]):
    for col,label in enumerate(['uniform','paced']):
        r=next(r for r in records if r['trial']==col and r['gear']==gear and r['sample']==sample)
        im=Image.open(N/(r['name']+'-native.png')).crop((0,330,900,620))
        board.paste(im,(col*900,row*310));d.text((col*900+10,row*310),f'{label} {gear} boundary raw{r["rawSlot"]}',fill='white')
board.save(P/'native-full-cycle-boundary-review.png')
report={'scope':'All37 poses/two cycles/both gears actually distance-driven. Exact timestamped native samples replayed, not continuous screen recording. Contact spans combine actual captured player root with raw-source matched material points; not independent rendered landmark tracking or full heel/toe contact proof.','nativeValidation':json.loads((N/'validation.json').read_text(encoding='utf-8')),'replayChecks':checks,'replayFailures':0,'comparisons':results,'visualReview':'Pending full-cycle/boundary/support-window boards.','strideOrGaitAccepted':False,'recordsSHA256':hashlib.sha256((N/'records.json').read_bytes()).hexdigest()}
(P/'native-phase-probe-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'replayChecks':checks,'replayFailures':0,'comparisons':[{'gear':r['gear'],'timing':r['timing'],'maxMeasuredWindowSpan93px':max(s['actualPlayerRootPlusSourceLandmarkSpanAt93px'] for s in r['supportSpans'])} for r in results]}))
