from pathlib import Path
from PIL import Image,ImageDraw
import json
P=Path(__file__).resolve().parent
e=json.loads((P/'interrupt-evidence.json').read_text())
for case in range(12):
    records=[r for r in e['records'] if r['case']==case]
    records=[r for i,r in enumerate(records) if r['interrupted'] or i==len(records)-1 or records[i+1]['interrupted']]
    board=Image.new('RGB',(len(records)*220,230),'#202a30');d=ImageDraw.Draw(board)
    frames=[];durations=[]
    for i,r in enumerate(records):
        im=Image.open(P/'interrupt-native'/Path(r['capture']).name).convert('RGB').crop((630,230,790,390))
        board.paste(im,(i*220,40));d.text((i*220+3,3),r['stage'].removeprefix('observation_')+' '+str(r['index']),fill='white')
        d.text((i*220+3,20),str(round(r['simTime'],3))+'s',fill='white')
        frames.append(im.resize((320,320),Image.Resampling.NEAREST))
        durations.append(max(20,round(((records[i+1]['simTime'] if i+1<len(records) else r['simTime']+.2)-r['simTime'])*1000)))
    board.save(P/f'interrupt-case{case:02d}.png')
    frames[0].save(P/f'interrupt-case{case:02d}.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=2)
for group in range(3):
    panels=[Image.open(P/f'interrupt-case{case:02d}.png') for case in range(group*4,group*4+4)]
    board=Image.new('RGB',(max(im.width for im in panels),4*255),'#202a30');d=ImageDraw.Draw(board)
    for i,im in enumerate(panels):
        case=group*4+i;d.text((3,i*255+3),f'Case {case}: gear {case//6}, '+('partial draw' if case%6<4 else 'held reading'),fill='white')
        board.paste(im,(0,i*255+25))
    board.save(P/f'interrupt-review{group}.png')
print(json.dumps({'checks':e['checks'],'failures':e['failures'],'captures':e['captures'],'boards':12}))
