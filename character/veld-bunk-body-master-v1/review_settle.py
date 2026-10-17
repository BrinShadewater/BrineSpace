from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,re
P=Path(__file__).resolve().parent;O=P.parents[1]/'output/veld-bunk-body-settle-v1'
records=json.loads((O/'records.json').read_text());assert len(records)==80
assert '14813 checks,0 failures' in (O/'native.log').read_text()
for rotation in range(4):
    for gear in ['bare','helmet']:
        record=next(r for r in records if r['rotation']==rotation and r['gear']==gear and r['stage']=='life_lie' and r['progress']==.51)
        changes=[s for s in record['samples'] if 'slot' in s]
        board=Image.new('RGB',(920,len(changes)*300),'#202a30');draw=ImageDraw.Draw(board)
        by_hash={}
        for row,s in enumerate(changes):
            name=f"{record['name']}-slot-{s['slot']:02d}"
            room=Image.open(O/f'{name}-room.png').convert('RGB').crop((253,285,653,585));board.paste(room,(0,row*300))
            source=Image.open(O/f'{name}-source.png').convert('RGBA');board.paste(source,(400,row*300),source)
            by_hash[hashlib.sha256(source.tobytes()).hexdigest()]=source
            draw.text((680,row*300+8),f"{gear} / rotation {rotation}\n{s['elapsed']:.2f}s",fill='white')
        board.save(P/f'native-settle-r{rotation}-{gear}.png')
        if rotation==0:
            frames=[]
            for s in record['samples']:
                source=by_hash[s['pixels']]
                x,y=[float(v) for v in re.findall(r'-?\d+(?:\.\d+)?',s['offset'])]
                frame=Image.new('RGB',(512,320),'#202a30')
                frame.paste(source,(round(256-128+x*148/65.28),round(280-224+y*148/65.28)),source)
                ImageDraw.Draw(frame).text((10,10),f"{gear}: supported settle / {s['elapsed']:.2f}s",fill='white');frames.append(frame)
            frames[0].save(P/f'supported-settle-{gear}.gif',save_all=True,append_images=frames[1:],duration=120,loop=0,disposal=2)
for gear in ['bare','helmet']:
    joins=[r for r in records if r['native'] and r['gear']==gear and not (r['stage']=='life_lie' and r['progress']==.51)]
    board=Image.new('RGB',(1040,len(joins)*280),'#202a30');draw=ImageDraw.Draw(board)
    for row,r in enumerate(joins):
        for col,side in enumerate(['live','slot-00']):
            name=r['name']+'-'+side
            room=Image.open(O/f'{name}-room.png').convert('RGB').crop((330,330,590,580));board.paste(room,(col*520,row*280+30))
            source=Image.open(O/f'{name}-source.png').convert('RGBA');board.paste(source,(col*520+260,row*280+8),source)
            draw.text((col*520+8,row*280+8),f"r{r['rotation']} / {r['stage']} {r['progress']} / {side}",fill='white')
    board.save(P/f'native-settle-joins-{gear}.png')
print('Eight full native settling boards, two paired entrance boards and two source-clock previews with actual recorded offsets')
