"""Freeze ordered selected Veld specials and compare at one physical ruler."""
from pathlib import Path
import json,re,hashlib
from PIL import Image,ImageDraw
H=Path(__file__).resolve().parent;R=H.parents[1];B=R/'character/dr-veld-v2'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
selected={'bare':{},'helmet':{}}
def load(p,g):
 m=json.loads(p.read_text(encoding='utf-8'))
 for s in m['states']:
  files=[(R/f.removeprefix('res://') if f.startswith('res://') else p.parent/f).resolve() for f in s['frameFiles']]
  selected[g][s['id']]=dict(manifest=p.relative_to(R).as_posix(),manifestHash=sha(p),files=[f.relative_to(R).as_posix() for f in files],frameHashes=[sha(f) for f in files],pivot=m['pivot'],standingHeight=m['standingHeight'],durations=s['frameDurationsMs'],loop=s.get('loop',False))
c=json.loads((B/'catalog.json').read_text())
for g,key in [('bare','body'),('helmet','equipment')]:
 for p in c[key]:load(B/p,g)
loader=R/'scripts/grid_canvas.gd';block=loader.read_text(encoding='utf-8').split('if actor == "veld":',1)[1].split('elif actor == "branforth":',1)[0]
for line in block.splitlines():
 m=re.search(r'"res://([^"]+manifest.json)"',line)
 if m:load(R/m[1],'helmet' if 'load_equipment_manifest' in line else 'bare')
families=['recover-air','swim-distress','death-ground','death-water'];records={}
def registered(row,index):
 im=Image.open(R/row['files'][index]).convert('RGBA');scale=148/row['standingHeight'];im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
 plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,(round(128-row['pivot'][0]*scale),round(224-row['pivot'][1]*scale)));return plane
for family in families:
 sheet=Image.new('RGBA',(2048,8*430),'#202a30');draw=ImageDraw.Draw(sheet)
 for gi,g in enumerate(['bare','helmet']):
  for di,d in enumerate(['east','west','north','south']):
   key=family+'-'+d;row=selected[g][key];records[g+'/'+key]=row;items=[(selected[g]['idle-'+d],0,'selected idle'),(selected[g][('swim-' if family in ['swim-distress','death-water'] else 'idle-')+d],0,'selected swim' if family in ['swim-distress','death-water'] else 'idle repeated')]+[(row,i,key+' '+str(i)) for i in range(len(row['files']))]
   y=(gi*4+di)*430
   for j,(item,i,label) in enumerate(items):
    plane=registered(item,i);sheet.alpha_composite(plane,(j*256,y+20));sheet.alpha_composite(plane.resize((142,142),Image.Resampling.LANCZOS),(j*256+57,y+278));draw.text((j*256+4,y+4),g+' '+label,fill='white')
 sheet.convert('RGB').save(H/(family+'-master-comparison.png'))
report=dict(loaderHash=sha(loader),counts={g:len(rows) for g,rows in selected.items()},states=len(records),references=sum(len(x['files']) for x in records.values()),selected=selected,specials=records,scope='Ordered catalog and literal overrides; selected physical148/82ruler comparison. No full-set/native/controller/owner acceptance.')
(H/'inventory.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
html='<meta charset="utf-8"><title>Veld remaining specials audit</title><style>body{background:#202a30;color:#e5ebed;font:16px sans-serif;margin:24px}img{max-width:100%}</style><h1>Veld remaining specials — selected masters</h1><p>Each row uses selected directional idle and, for water states, selected swim. Pose height is preserved;148/82physical rulers. Ordered runtime source snapshot retained.</p>'+''.join('<h2>'+f+'</h2><a href="'+f+'-master-comparison.png"><img src="'+f+'-master-comparison.png"></a>' for f in families)
(H/'index.html').write_text(html,encoding='utf-8');print(f'{len(records)}selected special states/{report["references"]}refs compared; source/loader hashes retained.')
