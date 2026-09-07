"""Compare saved pre-cleanup strips with the exported pack; no visual invention."""
from pathlib import Path
import json
import statistics
import numpy as np
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parent
BEFORE=ROOT/'qa/before-cleanup'
CURRENT=json.loads((ROOT/'final/manifest.json').read_text())
OLD=json.loads((BEFORE/'manifest.json').read_text())

def split(path):
    im=Image.open(path).convert('RGBA')
    return [im.crop((i*92,0,(i+1)*92,92)) for i in range(6)]

def head_width(frame):
    mask=np.array(frame.getchannel('A'))>0
    ys,xs=np.where(mask)
    height=ys.max()-ys.min()+1
    head=mask[ys.min():ys.min()+max(1,round(height*.17))]
    _,xs=np.where(head)
    return int(xs.max()-xs.min()+1)

def sample(frames,timing,time):
    t=time%sum(timing)
    for i,ms in enumerate(timing):
        if t<ms: return frames[i]
        t-=ms
    return frames[-1]

def main():
    selected=['walk-south','walk-east','run-east','repair-east']
    old={e['id']:e for e in OLD['states']}
    new={e['id']:e for e in CURRENT['states']}
    strips={}
    metrics={}
    old_colors=set(); new_colors=set()
    for state in new:
        a=split(BEFORE/f'{state}-strip.png')
        b=split(ROOT/'final'/f'{state}-strip.png')
        strips[state]=(a,b)
        wa=list(map(head_width,a)); wb=list(map(head_width,b))
        metrics[state]={'headWidthRangeBefore':max(wa)-min(wa),'headWidthRangeAfter':max(wb)-min(wb),
                        'medianHeadWidthBefore':statistics.median(wa),'medianHeadWidthAfter':statistics.median(wb)}
        for frames,colors in [(a,old_colors),(b,new_colors)]:
            for frame in frames:
                arr=np.array(frame); colors.update(map(tuple,arr[arr[:,:,3]>0,:3].tolist()))
    report={'opaqueColorsBefore':len(old_colors),'opaqueColorsAfter':len(new_colors),
            'states':metrics,'note':'Head bounding-box measurements are geometric diagnostics, not a quality score.'}
    (ROOT/'qa/before-after-metrics.json').write_text(json.dumps(report,indent=2)+'\n')
    sequence=[]
    for tick in range(60):
        canvas=Image.new('RGB',(552,4*300+30),(37,43,47))
        draw=ImageDraw.Draw(canvas)
        draw.text((100,8),'BEFORE',fill='white'); draw.text((380,8),'CLEANUP',fill='white')
        for row,state in enumerate(selected):
            for column,entry in enumerate([old[state],new[state]]):
                frame=sample(strips[state][column],entry['frameDurationsMs'],tick*50)
                enlarged=frame.resize((276,276),Image.Resampling.NEAREST)
                x=column*276; y=30+row*300
                draw.text((x+10,y+2),state,fill=(150,186,181))
                canvas.paste(enlarged,(x,y+20),enlarged)
        sequence.append(canvas)
    sequence[0].save(ROOT/'qa/before-after.gif',save_all=True,append_images=sequence[1:],duration=50,loop=0,disposal=2)
    # Still comparison retains exact frame zero for artifact inspection.
    sequence[0].save(ROOT/'qa/before-after.png')
    print(json.dumps({'beforeColors':len(old_colors),'afterColors':len(new_colors),'headMetrics':metrics},indent=2))

if __name__=='__main__': main()
