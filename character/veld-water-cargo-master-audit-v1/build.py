"""Current Veld cargo selection versus installed swim and accepted dry cargo."""
from pathlib import Path
import json,re,hashlib
from PIL import Image,ImageDraw
H=Path(__file__).resolve().parent;R=H.parents[1];selected={'bare':{},'helmet':{}}
def read(path,gear):
    p=R/path;m=json.loads(p.read_text())
    for s in m['states']:selected[gear][s['id']]=dict(manifest=path,profile={k:v for k,v in m.items() if k!='states'},state=s,files=[str((p.parent/f).resolve().relative_to(R)).replace('\\','/') for f in s['frameFiles']])
catalog=json.loads((R/'character/dr-veld-v2/catalog.json').read_text())
for gear,key in [('bare','body'),('helmet','equipment')]:
    for p in catalog[key]:read('character/dr-veld-v2/'+p,gear)
branch=(R/'scripts/grid_canvas.gd').read_text().split('if actor == "veld":',1)[1].split('elif actor == "branforth":',1)[0]
for method,path in re.findall(r'player\.(load_manifest|load_equipment_manifest)\((?:"diving-helmet", )?"res://([^"]+)"',branch):read(path,'bare' if method=='load_manifest' else 'helmet')
records={}
for gear in ['bare','helmet']:
    board=Image.new('RGBA',(1024,1120),'#202a30');draw=ImageDraw.Draw(board)
    for row,d in enumerate(['east','west','north','south']):
        legacy=selected[gear]['swim-carry-'+d];swim=selected[gear]['swim-'+d];dry=selected[gear]['carry-'+d]
        records[gear+'/'+d]=legacy
        for col,(entry,i,label) in enumerate([(legacy,0,'current cargo0'),(legacy,3,'current cargo3'),(swim,0,'selected swim master'),(dry,0,'accepted dry cargo')]):
            profile=entry['profile'];im=Image.open(R/entry['files'][i]).convert('RGBA');scale=148/profile.get('standingHeight',74);pivot=profile['pivot'];im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
            board.alpha_composite(im,(round(col*256+128-pivot[0]*scale),round(row*280+24+128-pivot[1]*scale)));draw.text((col*256+3,row*280+3),gear+' '+d+' '+label,fill='white')
        legacy['hashes']=[hashlib.sha256((R/p).read_bytes()).hexdigest() for p in legacy['files']]
    board.save(H/(gear+'-cargo-audit-v1.png'))
(H/'current-selection.json').write_text(json.dumps(dict(scope='Current literal loader/catalog selection; static master comparison, not full motion acceptance',loaderSha256=hashlib.sha256((R/'scripts/grid_canvas.gd').read_bytes()).hexdigest(),records=records),indent=2)+'\n')
print('8current cargo gearstates compared against selected swimming and dry cargo')
