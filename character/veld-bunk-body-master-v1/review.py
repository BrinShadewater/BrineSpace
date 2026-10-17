from pathlib import Path
from PIL import Image, ImageDraw
import json
P=Path(__file__).resolve().parent
O=P.parents[1]/'output/veld-bunk-body-master-v1'
for rotation in range(4):
    board=Image.new('RGB',(1820,1120),'#202a30');d=ImageDraw.Draw(board)
    for g,gear in enumerate(['bare','helmet']):
        for s,stage in enumerate(['life_lie','life_get_up']):
            y=(g*2+s)*280
            for pose in range(7):
                im=Image.open(O/f'rotation{rotation}-{gear}-{stage}-pose{pose}-room.png').convert('RGB').crop((330,330,590,580))
                board.paste(im,(pose*260,y+30));d.text((pose*260+6,y+8),f'R{rotation} {gear} '+('Lowering' if s==0 else 'Rising')+f' {pose+1}',fill='white')
    board.save(P/f'native-motion-rotation{rotation}.png')
board=Image.new('RGB',(2080,2240),'#202a30');d=ImageDraw.Draw(board)
for rotation in range(4):
    for g,gear in enumerate(['bare','helmet']):
        y=(rotation*2+g)*280
        for i,tag in enumerate(['pose0','pose1','pose2','pose2-terminal']):
            for restore in range(2):
                name=f'rotation{rotation}-{gear}-{tag}'+('-restored' if restore else '')
                im=Image.open(O/f'{name}-room.png').convert('RGB').crop((330,330,590,580));x=(i*2+restore)*260
                board.paste(im,(x,y+30));d.text((x+5,y+8),name,fill='white')
board.save(P/'native-supported-death.png')
for gear in ['bare','helmet']:
    m=json.loads((P/f'{gear}-manifest.json').read_text())
    for s in m['states']:
        if s['id']=='bunk-sleep-east':continue
        imgs=[]
        for f in s['frameFiles']:
            a=Image.open(P.parents[1]/f.removeprefix('res://')).convert('RGBA');bg=Image.new('RGB',a.size,'#202a30');bg.paste(a,mask=a.getchannel('A'));imgs.append(bg)
        imgs[0].save(P/f'{gear}-{s["id"]}.gif',save_all=True,append_images=imgs[1:],duration=[t*3 for t in s['frameDurationsMs']],loop=0)
html=['<!doctype html><meta charset="utf-8"><title>Veld master bunk body</title><style>body{background:#202a30;color:#e1e7eb;font:16px system-ui;margin:28px}img{max-width:100%;margin:12px}a{color:#8cc6e7}</style><h1>Veld — master bunk body</h1><p>Complete body poses matched to the selected standing master. Same stature, brown hair, warm skin, matte suit and science equipment. Preview runs at one-third speed. Both helmet versions retain the same bed contact. Staged for review.</p>']
for gear in ['bare','helmet']:
    html.append(f'<h2>{gear}</h2>')
    for key,label in [('bunk-enter-east','Lowering'),('bunk-exit-east','Rising'),('death-bunk-east','Supported arm relaxation')]:
        html.append(f'<p>{label}</p><img src="{gear}-{key}.gif" height="272"><img src="{gear}-{key}.gif" height="100">')
html.append('<p><a href="paired-source-review.png">Paired source poses</a> · <a href="bare-source-review.png">Same-size master comparison</a></p>')
for i in range(4):html.append(f'<p><a href="native-motion-rotation{i}.png">Actual room motion — rotation {i+1}</a></p>')
html.append('<p><a href="native-supported-death.png">Actual supported motion and restored contact</a></p>')
(P/'index.html').write_text('\n'.join(html),encoding='utf-8')
print('112 live native poses,64 supported/restored views,6 source-clock GIFs and review page')
