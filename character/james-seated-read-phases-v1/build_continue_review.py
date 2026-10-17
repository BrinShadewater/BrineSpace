from pathlib import Path
from PIL import Image,ImageDraw
import json
P=Path(__file__).resolve().parent;e=json.loads((P/'continue-evidence.json').read_text());assert not e['failures']
for case in range(6):
    rows=[r for r in e['records'] if r['case']==case];at=next(i for i,r in enumerate(rows) if r['resumed'])
    selected=sorted(set([max(0,at-1)]+list(range(at,min(at+5,len(rows))))+list(range(max(at,len(rows)-6),len(rows)))))
    board=Image.new('RGB',(len(selected)*190,205),'#202a30');d=ImageDraw.Draw(board)
    for i,j in enumerate(selected):
        r=rows[j];im=Image.open(P/'continue-native'/Path(r['capture']).name).convert('RGB').crop((630,230,790,390));board.paste(im,(i*190,40))
        d.text((i*190+2,3),r['stage'].removeprefix('observation_')+' '+str(r['index']),fill='white')
        d.text((i*190+2,20),('restored ' if r['resumed'] else 'before ')+str(round(r['simTime'],2)),fill='white')
    board.save(P/f'continue-case{case}.png')
    frames=[];durations=[]
    for i,r in enumerate(rows):
        frames.append(Image.open(P/'continue-native'/Path(r['capture']).name).convert('RGB').crop((630,230,790,390)).resize((320,320),Image.Resampling.NEAREST))
        durations.append(max(20,round(((rows[i+1]['simTime'] if i+1<len(rows) else r['simTime']+.2)-r['simTime'])*1000)))
    frames[0].save(P/f'continue-case{case}.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=2)
for mode in range(2):
    panels=[Image.open(P/f'continue-case{case}.png') for case in range(mode*3,mode*3+3)]
    board=Image.new('RGB',(max(im.width for im in panels),3*235),'#202a30');d=ImageDraw.Draw(board)
    for i,im in enumerate(panels):
        d.text((3,i*235+3),f'Gear {mode}: '+['partial draw Continue','held Continue','interrupted stow Continue'][i],fill='white');board.paste(im,(0,i*235+25))
    board.save(P/f'continue-review{mode}.png')
print(json.dumps({'checks':e['checks'],'failures':e['failures'],'captures':e['captures'],'freshSceneCases':6,'visualScope':'Before/after Continue, first five restored source changes and final six rise poses for all six cases.'}))
