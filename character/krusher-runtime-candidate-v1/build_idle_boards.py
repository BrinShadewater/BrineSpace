from pathlib import Path
import json,math
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;N=P/'review/motion';r=json.loads((N/'report.json').read_text());font=ImageFont.truetype(str(P.parent.parent/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),18)
for direction in ['south','east','north','west']:
    samples=[s for s in r['samples'] if s['cycle']==0 and s['state']=='idle-'+direction]
    board=Image.new('RGB',(1200,50+math.ceil(len(samples)/10)*135),'#303437');d=ImageDraw.Draw(board);d.text((12,10),'KRUSHER / IDLE '+direction.upper()+' / NATIVE 92 PX CAPTURES / ALL POSES',font=font,fill='white')
    for i,sample in enumerate(samples):
        # Exact native display pixels; no resizing of the sprite crop.
        crop=Image.open(N/sample['capture']).crop((238,510,330,602));x=i%10*120+14;y=i//10*135+45;board.paste(crop,(x,y));d.text((x,y+95),str(sample['index']),font=font,fill='white')
    board.save(P/'review'/('idle-'+direction+'-native-board.png'))
print('Four full idle boards saved, 289 chronological native source poses.')
