"""Read-only literal selected-source inventory; not a runtime or motion acceptance gate."""
from pathlib import Path
import hashlib,json,re
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
text=(R/'scripts/grid_canvas.gd').read_text(encoding='utf-8')
branch=text.split('if actor == "veld":',1)[1].split('elif actor == "branforth":',1)[0]
catalog=json.loads((R/'character/dr-veld-v2/catalog.json').read_text(encoding='utf-8'))
selected={'bare':{},'helmet':{}}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(path,gear):
 f=R/path;m=json.loads(f.read_text(encoding='utf-8'))
 for s in m['states']:
  selected[gear][s['id']]={'manifest':path,'pivot':m.get('pivot',[46,86]),'standingHeight':m.get('standingHeight',74),'durations':s['frameDurationsMs'],'loop':s['loop'],'files':[(f.parent/q).relative_to(R).as_posix() if not q.startswith('res://') else q[6:] for q in s['frameFiles']]}
for g,k in [('bare','body'),('helmet','equipment')]:
 for f in catalog[k]:load('character/dr-veld-v2/'+f,g)
for x in re.finditer(r'player\.(load_manifest|load_equipment_manifest)\((?:"diving-helmet", )?"res://([^"]+)"',branch):load(x[2],'bare' if x[1]=='load_manifest' else 'helmet')
life=['death-ground','death-water','sit-down','sit-idle','sit-rise','lie-down','sleep','get-up','inspect','eat','drink','read-seated']
report={g:{k:v for k,v in states.items() if any(k.startswith(a+'-') for a in life)} for g,states in selected.items()}
masters={}
for family in ['death-ground','death-water']:
 board=Image.new('RGBA',(960,8*300),'#202a30');draw=ImageDraw.Draw(board)
 for di,d in enumerate(['east','west','north','south']):
  for gi,g in enumerate(['bare','helmet']):
   row=di*2+gi;s=selected[g][family+'-'+d];master=selected[g][('idle' if family=='death-ground' else 'swim')+'-'+d]
   masters[g+'-'+family+'-'+d]=master
   pairs=[(master,0,'selected master'),(s,0,'entry'),(s,len(s['files'])//2,'middle'),(s,len(s['files'])-1,'terminal')]
   anchor=160 if family=='death-water' else 220
   for col,(m,i,label) in enumerate(pairs):
    im=Image.open(R/m['files'][i]).convert('RGBA');scale=148/m['standingHeight']
    im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    at=(col*240+120-round(m['pivot'][0]*scale),row*300+anchor-round(m['pivot'][1]*scale))
    board.alpha_composite(im,at);draw.text((col*240+4,row*300+2),d+' '+g+' '+label,fill='white')
 board.save(P/(family+'-masters.png'))
files={f for states in report.values() for s in states.values() for f in s['files']}|{s['files'][0] for s in masters.values()}
result={'scope':'catalog plus literal selected Veld overrides; runtime coherent joins and complete motion unproven','loaderSha256':sha(R/'scripts/grid_canvas.gd'),'selected':report,'masters':masters,'hashes':{f:sha(R/f) for f in sorted(files)}}
(P/'coverage.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
(P/'index.html').write_text('<meta charset="utf-8"><title>Veld death master audit</title><style>body{background:#202a30;color:#eee;font:16px sans-serif;margin:24px}img{max-width:100%}</style><h1>Veld selected death clips against current masters</h1><p>Literal selected sources at the same declared standing scale and pivot. Coverage and drift diagnosis; complete motion and native rendered selection remain separate. Older death clips retain mismatched materials/proportions/helmet hardware; staged east prone replacement is reviewed separately.</p><h2>Ground</h2><img src="death-ground-masters.png"><h2>Water</h2><img src="death-water-masters.png"><p><a href="../veld-death-water-east-coherent-v1/">East prone candidate</a></p>',encoding='utf-8')
print(f'Read-only life/death inventory:{sum(len(v) for v in report.values())} states;16 death/master rows;full motion/runtime acceptance unproven')
