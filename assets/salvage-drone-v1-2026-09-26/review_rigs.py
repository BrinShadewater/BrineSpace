from build_full import R,SPECS,rig
from PIL import Image,ImageDraw
import json
order=['north','northeast','east','southeast','south','southwest','west','northwest']
board=Image.new('RGBA',(1440,1100),'#17272e');draw=ImageDraw.Draw(board)
closed=Image.new('RGBA',(1440,850),'#17272e');cd=ImageDraw.Draw(closed);rows=[]
for i,h in enumerate(order):
 base,body,cargo,mask,lamp,meta=rig(h,SPECS[h]);x=i%4*360;y=i//4*550
 draw.text((x+12,y+12),h.upper(),fill='white');board.alpha_composite(base.resize((350,350),Image.Resampling.LANCZOS),(x+5,y+30))
 p=base.resize((174,174),Image.Resampling.LANCZOS);board.alpha_composite(p,(x+3,y+370));draw.rectangle((x+182,y+370,x+359,y+549),fill='#c2c5bd');board.alpha_composite(p,(x+183,y+370))
 c=body(1,0);c.alpha_composite(cargo());y=i//4*425;closed.alpha_composite(c.resize((360,360),Image.Resampling.LANCZOS),(x,y+25));cd.text((x+12,y+8),h.upper()+' / CLOSED',fill='white')
 rows.append({'heading':h,'sourceScale':meta['scale'],'bounds':base.getbbox(),'axis':meta['axis']})
board.save(R/'review/directions.png');closed.save(R/'review/closed-directions.png');(R/'review/registration.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
print('Eight open/closed rigs reviewed at common display scale.')
