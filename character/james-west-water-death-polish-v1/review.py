from pathlib import Path
from PIL import Image,ImageDraw
import json
P=Path(__file__).resolve().parent;old=P.parent/'james-death-family-v1';frames=[];dur=[];rulers={}
for i in range(6):
    board=Image.new('RGB',(900,360),'#303b40');draw=ImageDraw.Draw(board)
    for row,mode in enumerate(['bare','helmet']):
        for col,(tag,folder) in enumerate([('old',old),('new',P)]):
            pack=json.loads((folder/(mode+'-manifest.json')).read_text());s=next(s for s in pack['states'] if s['id']=='death-water-west');im=Image.open(folder/s['frameFiles'][i]).convert('RGBA');small=im.resize((142,199),Image.Resampling.LANCZOS);at=(col*450+100,row*180-25);board.paste(small,at,small);draw.text((col*450+12,row*180+8),tag+' '+mode+' West water death '+str(i),fill='white')
            rulers.setdefault(tag+'-'+mode,[]).append(dict(pose=i,alphaBounds=im.getbbox(),rightmostBootPixel=im.getbbox()[2]-1))
            if col==1 and row==0:dur.append(int(s['frameDurationsMs'][i]))
    frames.append(board)
frames[0].save(P/'comparison.gif',save_all=True,append_images=frames[1:],duration=dur,loop=0,disposal=2,optimize=False)
frames[3].save(P/'comparison-midpoint.png');(P/'boot-registration-comparison.json').write_text(json.dumps(rulers,indent=2)+'\n')
print({tag:[p['rightmostBootPixel'] for p in rows] for tag,rows in rulers.items()})
for name in ['native-staged-behaviour','native-installed-behaviour']:
    folder=P/(name+'-captures')
    if not folder.exists():continue
    board=Image.new('RGB',(1200,440),'#303b40');draw=ImageDraw.Draw(board)
    for row,mode in enumerate(['bare','helmet']):
        for i,file in enumerate(sorted(folder.glob(mode+'-water-west-*.png'))):
            im=Image.open(file).convert('RGB');cx,cy=im.width//2,im.height//2;im=im.crop((cx-90,cy-85,cx+90,cy+100));at=(i*200,row*220+25);board.paste(im,at);draw.text((at[0]+4,at[1]-18),file.stem,fill='white')
    board.save(P/(name+'-contact.png'))
