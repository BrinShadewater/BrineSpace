import json
from pathlib import Path
from PIL import Image,ImageDraw
root=Path.cwd();review=root/'character/james-west-carry-walk-keys-v1/release-expedition-playtest-v355';captures=root/'output/james-expedition-playtest-v355/captures'
data=json.loads((captures/'review.json').read_text());assert data['failures']==0 and len(data['cases'])==4
(review/'lifecycle-review.json').write_text(json.dumps(data,indent=2)+'\n')
for case in data['cases']:
    rows=[x for x in data['captures'] if x['case']==case['case']]
    images=[Image.open(captures/x['file']).convert('RGB') for x in rows]
    durations=[max(1,round((rows[i+1]['time']-x['time'])*1000)) if i+1<len(rows) else 400 for i,x in enumerate(rows)]
    images[0].save(review/(case['case']+'-native.png'),save_all=True,append_images=images[1:],duration=durations,loop=0,disposal=0,blend=0)
    selected=[]
    for phase in ['approach','pressurize','leave','outbound','salvage','pickup','return','entry','drain','exit','unload','complete']:
        group=[x for x in rows if x['tripPhase']==phase]
        assert group,(case['case'],phase)
        selected.append(group[len(group)//2])
    first=images[0];width,height=first.size
    board=Image.new('RGB',(width*4,(height+24)*3),(47,58,63));draw=ImageDraw.Draw(board)
    for i,item in enumerate(selected):
        x=i%4;y=i//4
        board.paste(Image.open(captures/item['file']).convert('RGB'),(width*x,(height+24)*y+24))
        draw.text((width*x+4,(height+24)*y+5),f"{item['tripPhase']} {item['state']} {item['direction']}",fill='white')
    board.save(review/(case['case']+'-chronology.png'))
print(json.dumps({'cases':len(data['cases']),'checks':data['checks'],'failures':0,'captures':len(data['captures'])}))
