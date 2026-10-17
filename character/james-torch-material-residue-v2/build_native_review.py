from pathlib import Path
from PIL import Image,ImageDraw
import json
P=Path(__file__).resolve().parent;e=json.loads((P/'validate-evidence.json').read_text());assert not e['failures']
for direction in ['east','north','south','west']:
    board=Image.new('RGB',(9*280,2*330),'#202a30');d=ImageDraw.Draw(board)
    for row,mode in enumerate(['bare','helmet']):
        rows=[r for r in e['records'] if r['mode']==mode and r['key'].endswith('-'+direction)]
        assert len(rows)==9
        for i,r in enumerate(rows):
            im=Image.open(P/'native'/Path(r['capture']).name).convert('RGB').crop((500,380,640,530)).resize((280,300),Image.Resampling.NEAREST)
            x=i*280;y=row*330;board.paste(im,(x,y+28));d.text((x+3,y+3),mode+' '+r['key']+' '+str(r['sourceIndex']),fill='white')
    board.save(P/f'native-{direction}.png')
print('72 prescribed native poses on four paired boards; no actual construction-order journey claim.')
