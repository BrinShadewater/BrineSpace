from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np
P=Path(__file__).resolve().parent
source=json.loads((P/'SOURCE_REVIEW.json').read_text());rows=[]
for item in source['frames']:
 i=item['frame'];a=np.array(Image.open(P/f'frames/bare/{i:03}.png').convert('RGBA'))
 yy,xx=np.where(a[210:,:,3]>200);yy+=210;front=yy[xx<133];rear=yy[xx>=133]
 rows.append({'sourceSlot':i,'frontLowerAlphaY':int(front.max()) if len(front) else None,'rearLowerAlphaY':int(rear.max()) if len(rear) else None})
for start in range(0,len(rows),24):
 board=Image.new('RGB',(1200,780),'#202a30');d=ImageDraw.Draw(board)
 for j,row in enumerate(rows[start:start+24]):
  i=row['sourceSlot'];im=Image.open(P/f'frames/bare/{i:03}.png');x=j%6*200;y=j//6*195
  crop=im.crop((95,190,185,237)).resize((180,94),Image.Resampling.NEAREST);board.paste(crop,(x,y+32),crop)
  d.line((x,y+98,x+180,y+98),fill='#ce7f70');d.text((x+3,y+4),f"{i} front{row['frontLowerAlphaY']} rear{row['rearLowerAlphaY']}",fill='white')
 board.save(P/f'feet-chronology-{start//24:02}.png')
report={'groundLineY':223,'limits':'Fixed foreground bands alpha>200,y>=210,x<133(front)/x>=133(rear). Diagnostic only: not labelled feet, world depth, pressure or collision. All source frames retained.','frontRange':[min(x['frontLowerAlphaY'] for x in rows if x['frontLowerAlphaY'] is not None),max(x['frontLowerAlphaY'] for x in rows if x['frontLowerAlphaY'] is not None)],'rearRange':[min(x['rearLowerAlphaY'] for x in rows if x['rearLowerAlphaY'] is not None),max(x['rearLowerAlphaY'] for x in rows if x['rearLowerAlphaY'] is not None)],'rows':rows}
(P/'CONTACT_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n');print({k:report[k] for k in ['frontRange','rearRange']})
