import json
from pathlib import Path
from PIL import Image, ImageDraw
root=Path.cwd();bank=root/'character/james-west-carry-walk-keys-v1'
review=bank/'release-hazard-playtest-v353';captures=root/'output/james-hazard-playtest-v353/captures'
data=json.loads((captures/'review.json').read_text())
assert data['failures']==0
(review/'lifecycle-review.json').write_text(json.dumps(data,indent=2)+'\n')
for case in data['cases']:
    rows=[x for x in data['captures'] if x['case']==case['case']]
    images=[Image.open(captures/x['file']).convert('RGB') for x in rows]
    durations=[max(1,round((rows[i+1]['time']-x['time'])*1000)) if i+1<len(rows) else 400 for i,x in enumerate(rows)]
    images[0].save(review/(case['case']+'-native.png'),save_all=True,append_images=images[1:],duration=durations,loop=0,disposal=0,blend=0)
for gear in ['bare','helmet']:
    for outcome in ['recovery','fatal']:
        selected=[]
        for direction in ['north','east','south','west']:
            rows=[x for x in data['captures'] if x['case']==f'{gear}-{direction}-{outcome}']
            initial=[x for x in rows if x['state']=='swim-distress']
            terminal=[x for x in rows if x['state']==('recover-air' if outcome=='recovery' else 'death-water')]
            assert initial and terminal
            selected.append([initial[0],initial[-1],terminal[0],terminal[len(terminal)//2],rows[-1]])
        first=Image.open(captures/selected[0][0]['file']);width,height=first.size
        board=Image.new('RGB',(width*5,(height+24)*4),(47,58,63));draw=ImageDraw.Draw(board)
        for y,row in enumerate(selected):
            for x,item in enumerate(row):
                board.paste(Image.open(captures/item['file']).convert('RGB'),(width*x,(height+24)*y+24))
                draw.text((width*x+4,(height+24)*y+5),f"{item['direction']} {item['state']} {item['source'].get('index','')}",fill='white')
        board.save(review/f'{gear}-{outcome}-chronology.png')
print(json.dumps({'cases':len(data['cases']),'failures':data['failures'],'playbacks':len(data['cases']),'boards':4}))
