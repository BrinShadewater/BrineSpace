from pathlib import Path
import json
from PIL import Image,ImageDraw

P=Path(__file__).resolve().parent
O=P.parents[1]/'output/veld-bunk-body-resume-v1'
assert json.loads((O/'validation.json').read_text())['passed']
records=json.loads((O/'records.json').read_text())
count=0
for record in records:
    slots=[s['tick'] for s in record['reference'] if 'rendered' in s]
    board=Image.new('RGB',(1040,len(slots)*280),'#202a30');draw=ImageDraw.Draw(board)
    for row,tick in enumerate(slots):
        for col,side in enumerate(['reference','resumed']):
            name=f"{record['name']}-{side}-tick-{tick:02d}"
            room=Image.open(O/f'{name}-room.png').convert('RGB').crop((330,330,590,580))
            board.paste(room,(col*520,row*280+30))
            draw.text((col*520+8,row*280+8),f'{side}: {record[side][tick]["stage"] or record[side][tick]["state"]} / {(tick+1)*20}ms',fill='white')
            source=Image.open(O/f'{name}-source.png').convert('RGBA')
            # Original canvas and pivot: no pose fitting or independent rescaling.
            if source.size==(184,184):
                padded=Image.new('RGBA',(256,272));padded.alpha_composite(source,(36,52));source=padded
            board.paste(source,(col*520+260,row*280+8),source)
            count+=1
    board.save(P/f"native-resume-{record['name']}.png")
print(f'{len(records)} paired future-motion boards; {count} native presentations with exact source frames')
