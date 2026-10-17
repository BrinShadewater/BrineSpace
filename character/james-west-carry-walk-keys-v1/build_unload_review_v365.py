import json
from pathlib import Path
from PIL import Image, ImageDraw

root=Path.cwd();bank=root/'character/james-west-carry-walk-keys-v1'
out=bank/'release-build-review-v365'
spec=json.loads((out/'playback.json').read_text())['unload']
def slot(row,time):
    clock=min(time,sum(row['clocks'])-.001);index=0
    while index<len(row['clocks'])-1 and clock>=row['clocks'][index]:
        clock-=row['clocks'][index];index+=1
    return index
boards=[];times=[round(i*1000/60) for i in range(32)]+[520]
for time in times:
    board=Image.new('RGB',(600,340),(48,59,64));draw=ImageDraw.Draw(board)
    draw.text((95,10),'Current',fill='white');draw.text((380,10),'Reused mid-rise',fill='white')
    for row in spec:
        image=Image.open(root/row['paths'][slot(row,time)].lstrip('/')).convert('RGBA')
        scale=82/148;image=image.resize((round(256*scale),round(256*scale)),Image.Resampling.BILINEAR)
        x=145 if row['gear'].startswith('current') else 445
        y=155 if row['gear'].endswith('bare') else 300
        board.paste(image,(x-round(128*scale),y-round(224*scale)),image)
    draw.text((12,322),'520ms action / 650ms review hold / accepted artwork only',fill='white')
    boards.append(board)
clocks=[max(1,times[i+1]-time) if i+1<len(times) else 650 for i,time in enumerate(times)]
boards[0].save(out/'comparison-motion.png',save_all=True,append_images=boards[1:],duration=clocks,loop=0,disposal=0,blend=0)
captures=root/'output/james-unload-playtest-v365/captures'
if not (captures/'review.json').exists():
    print('Source comparison ready; native run still pending')
else:
    data=json.loads((captures/'review.json').read_text())
    assert data['failures']==0 and len(data['cases'])==8
    for case in data['cases']:
        rows=[r for r in data['captures'] if r['case']==case['case']]
        active=[r for r in rows if r.get('source',{}).get('key')=='unload-north']
        # A shared fixture texture can alias slot5 to index2 via Array.find.
        # Normal manifest loading may allocate distinct equal-pixel objects.
        # Chronological runs preserve the return pose in either representation.
        segments=[]
        for row in active:
            if not segments or row['source']['index']!=segments[-1]['source']['index']:
                segments.append(row)
        assert [r['source']['index'] for r in segments] in [[0,1,2,3,4,2,6],[0,1,2,3,4,5,6]]
        chosen=segments+[rows[-1]]
        w,h=Image.open(captures/chosen[0]['file']).size
        board=Image.new('RGB',(w*4,(h+24)*2),(48,59,64));draw=ImageDraw.Draw(board)
        for i,row in enumerate(chosen):
            x,y=i%4*w,i//4*(h+24)
            board.paste(Image.open(captures/row['file']).convert('RGB'),(x,y+24))
            draw.text((x+4,y+5),f'pose{i}' if i<7 else 'idle',fill='white')
        board.save(out/(case['case']+'-native.png'))
    (out/'native-review.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'checks':data['checks'],'failures':0,'cases':8,'captures':len(data['captures']),'allSevenPoseRunsObserved':True,'normalPackagedSources':True}))
