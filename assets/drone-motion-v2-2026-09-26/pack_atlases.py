from pathlib import Path
import json,math
from PIL import Image
ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
(ROOT/'atlases').mkdir(exist_ok=True)
def pack(paths,name):
    columns=8;rows=math.ceil(len(paths)/columns)
    im=Image.new('RGBA',(columns*256,rows*256))
    for i,p in enumerate(paths):im.paste(Image.open(ROOT/p).convert('RGBA'),((i%columns)*256,(i//columns)*256))
    path=ROOT/'atlases'/f'{name}.png';temp=path.with_name(path.stem+'.tmp.png');im.save(temp);temp.replace(path)
    return {'path':path.relative_to(ROOT).as_posix(),'columns':columns,'rows':rows,'frameCount':len(paths)}
for clip in data['states']:
    clip['atlas']=pack(clip['frameFiles'],clip['id'])
    if clip.get('effectFiles'):clip['effectAtlas']=pack(clip['effectFiles'],clip['id']+'-effects')
    if clip.get('cargoFiles'):clip['cargoAtlas']=pack(clip['cargoFiles'],clip['id']+'-cargo')
for name,clip in data['statusClips'].items():clip['atlas']=pack(clip['frameFiles'],'status-'+name)
temp=ROOT/'manifest.tmp.json';temp.write_text(json.dumps(data,indent=2),encoding='utf-8');temp.replace(ROOT/'manifest.json')
print('Packed',len(data['states'])+sum(bool(s.get('effectFiles'))+bool(s.get('cargoFiles')) for s in data['states'])+len(data['statusClips']),'atlases')
