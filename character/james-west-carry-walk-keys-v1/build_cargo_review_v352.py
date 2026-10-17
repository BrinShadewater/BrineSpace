import json
from pathlib import Path
from PIL import Image,ImageDraw
r=Path.cwd();p=r/'character/james-west-carry-walk-keys-v1/release-cargo-playtest-v352';src=r/'output/james-cargo-playtest-v352/captures';d=json.loads((src/'review.json').read_text());assert d['failures']==0
(p/'lifecycle-review.json').write_text(json.dumps(d,indent=2))
for case in d['cases']:
    rows=[x for x in d['captures'] if x['case']==case['case']]
    images=[Image.open(src/x['file']).convert('RGB') for x in rows]
    durations=[max(1,round((rows[i+1]['time']-x['time'])*1000)) if i+1<len(rows) else 400 for i,x in enumerate(rows)]
    images[0].save(p/(case['case']+'-native.png'),save_all=True,append_images=images[1:],duration=durations,loop=0,disposal=0,blend=0)
for rotation in range(4):
    cells=[];labels=[]
    for gear in ['bare','helmet']:
        rows=[x for x in d['captures'] if x['case']==f'{gear}-rotation-{rotation}']
        def phase(stage,fraction):
            group=[x for x in rows if x['stage']==stage]
            assert group,stage
            return group[round((len(group)-1)*fraction)]
        picked=[phase('workshop_inspect',.5),phase('workshop_pickup',.5),phase('workshop_carry',.5),phase('workshop_unload',0),phase('workshop_unload',.5),phase('workshop_unload',1),rows[-1]]
        cells.append([Image.open(src/x['file']).convert('RGB') for x in picked]);labels.append([f"{gear} {x['state']} / {x['direction']}" for x in picked])
    width=max(im.width for row in cells for im in row);height=max(im.height for row in cells for im in row)
    board=Image.new('RGB',(width*7,(height+24)*2),(47,58,63));draw=ImageDraw.Draw(board)
    for row in range(2):
        for col in range(7):
            board.paste(cells[row][col],(width*col,(height+24)*row+24));draw.text((width*col+4,(height+24)*row+5),labels[row][col],fill='white')
    board.save(p/f'rotation-{rotation}-chronology.png')
    # The controller names its arrival turn workshop_unload too: inspect the
    # actual unload source separately rather than mistaking turn samples for it.
    board=Image.new('RGB',(width*5,(height+24)*2),(47,58,63));draw=ImageDraw.Draw(board)
    for row,gear in enumerate(['bare','helmet']):
        rows=[x for x in d['captures'] if x['case']==f'{gear}-rotation-{rotation}' and x['source'].get('key')=='unload-north']
        assert rows
        picked=[rows[round((len(rows)-1)*fraction)] for fraction in [0,.25,.5,.75,1]]
        for col,x in enumerate(picked):
            board.paste(Image.open(src/x['file']).convert('RGB'),(width*col,(height+24)*row+24));draw.text((width*col+4,(height+24)*row+5),f"{gear} unload source {x['source']['index']}",fill='white')
    board.save(p/f'rotation-{rotation}-unload-source.png')
print('Built eight lossless native APNG playbacks and four lifecycle chronology boards')
