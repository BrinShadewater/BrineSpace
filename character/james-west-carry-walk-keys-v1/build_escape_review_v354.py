import json
from pathlib import Path
from PIL import Image,ImageDraw
root=Path.cwd();review=root/'character/james-west-carry-walk-keys-v1/release-escape-playtest-v354';captures=root/'output/james-escape-playtest-v354/captures'
data=json.loads((captures/'review.json').read_text());assert data['failures']==0
(review/'lifecycle-review.json').write_text(json.dumps(data,indent=2)+'\n')
for case in data['cases']:
    rows=[x for x in data['captures'] if x['case']==case['case']]
    images=[Image.open(captures/x['file']).convert('RGB') for x in rows]
    durations=[max(1,round((rows[i+1]['time']-x['time'])*1000)) if i+1<len(rows) else 400 for i,x in enumerate(rows)]
    images[0].save(review/(case['case']+'-native.png'),save_all=True,append_images=images[1:],duration=durations,loop=0,disposal=0,blend=0)
for heading in ['north','east','south','west']:
    selected=[]
    for gear in ['bare','helmet']:
        rows=[x for x in data['captures'] if x['case']==f'{gear}-{heading}']
        recovery=[x for x in rows if x['state']=='recover-air'];assert recovery
        movement=[x for x in rows if x['state']!='recover-air']
        selected.append([rows[0],movement[len(movement)//2],recovery[0],recovery[len(recovery)//2],rows[-1]])
    first=Image.open(captures/selected[0][0]['file']);width,height=first.size
    board=Image.new('RGB',(width*5,(height+24)*2),(47,58,63));draw=ImageDraw.Draw(board)
    for y,row in enumerate(selected):
        for x,item in enumerate(row):
            board.paste(Image.open(captures/item['file']).convert('RGB'),(width*x,(height+24)*y+24))
            draw.text((width*x+4,(height+24)*y+5),f"{'bare' if y==0 else 'helmet'} {item['state']} {item['source'].get('index','')}",fill='white')
    board.save(review/f'{heading}-chronology.png')
print(json.dumps({'cases':len(data['cases']),'checks':data['checks'],'captures':len(data['captures']),'failures':0}))
