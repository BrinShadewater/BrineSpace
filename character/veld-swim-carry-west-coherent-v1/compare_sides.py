"""Equal physical-ruler east/west comparison and fresh ordered selection proof."""
from pathlib import Path
import json,re,hashlib
from PIL import Image,ImageDraw
H=Path(__file__).resolve().parent;R=H.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
selected={'bare':{},'helmet':{}}
def read(path,gear):
 p=R/path;m=json.loads(p.read_text())
 for s in m['states']:selected[gear][s['id']]=dict(manifest=path,files=[(p.parent/f).resolve() for f in s['frameFiles']])
catalog=json.loads((R/'character/dr-veld-v2/catalog.json').read_text())
for gear,key in [('bare','body'),('helmet','equipment')]:
 for p in catalog[key]:read('character/dr-veld-v2/'+p,gear)
branch=(R/'scripts/grid_canvas.gd').read_text().split('if actor == "veld":',1)[1].split('elif actor == "branforth":',1)[0]
for method,path in re.findall(r'player\.(load_manifest|load_equipment_manifest)\((?:"diving-helmet", )?"res://([^"]+)"',branch):read(path,'bare' if method=='load_manifest' else 'helmet')
base=json.loads((R/'character/veld-water-cargo-master-audit-v1/current-selection.json').read_text());proof={};frames={}
board=Image.new('RGBA',(1024,1280),'#202a30');d=ImageDraw.Draw(board)
for col,(gear,direction) in enumerate([('bare','east'),('bare','west'),('helmet','east'),('helmet','west')]):
 current=selected[gear]['swim-carry-'+direction];old=base['records'][gear+'/'+direction]
 assert current['manifest']==old['manifest'];assert [sha(p) for p in current['files']]==old['hashes']
 proof[gear+'/'+direction]=dict(manifest=current['manifest'],hashes=old['hashes'],selectedUnchanged=True)
 master=Image.open(selected[gear]['swim-'+direction]['files'][0]).convert('RGBA');board.alpha_composite(master,(col*256,0));d.text((col*256+3,5),gear+' '+direction+' selected swim',fill='white')
 family=R/f'character/veld-swim-carry-{direction}-coherent-v1';m=json.loads((family/f'{gear}-manifest.json').read_text())
 for i,f in enumerate(m['states'][0]['frameFiles']):
  p=family/f;im=Image.open(p).convert('RGBA');board.alpha_composite(im,(col*256,(i+1)*175));d.text((col*256+3,(i+1)*175+5),gear+' '+direction+' cargo '+str(i),fill='white');frames[p.relative_to(R).as_posix()]=sha(p)
board.save(H/'side-family-comparison-v1.png')
(H/'side-family-master-checks.json').write_text(json.dumps(dict(scope='Fresh ordered Veld cargo selection unchanged; equal148 physical-ruler comparison of24staged east/west refs against selected ordinary swim; not moving or world certification',currentSelected=proof,stagedFrameHashes=frames,loaderSha256=sha(R/'scripts/grid_canvas.gd')),indent=2)+'\n')
print('4 current cargo gearstates unchanged;24staged side refs compared at equal native ruler.')
