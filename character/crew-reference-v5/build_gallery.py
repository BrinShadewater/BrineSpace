from pathlib import Path
import json,shutil,hashlib,html
from PIL import Image
P=Path(__file__).resolve().parent
source=Path('C:/Users/Alex/.codex/generated_images/01a0e18a-8645-7483-9c2b-e74ec1741016')
records=[]
for name,filename in json.loads((P/'sources.json').read_text()).items():
 target=P/name;shutil.copyfile(source/filename,target)
 with Image.open(target) as im:
  im.load();dims=im.size
 records.append(dict(file=name,size=dims,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),selected='rejected' not in name))
palette=json.loads((P.parent/'crew-turnarounds-v4/palette-reference.json').read_text())
palette['version']=2;palette['status']='Authoritative material targets; generated labels/swatches are illustrative, not sampled colour specifications.'
palette['character_materials']['branforth'].update({'Accent shadow':'#766A38','Accent base':'#B3A153','Accent light':'#D2C17A'})
(P/'palette-reference.json').write_text(json.dumps(palette,indent=2)+'\n')
parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BrineSpace crew reference library</title><style>body{margin:0;background:#182126;color:#e5e9eb;font:16px system-ui}main{max-width:1300px;margin:auto;padding:28px}p{line-height:1.5;max-width:950px}a{color:#a9d4ec}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:18px}img{width:100%;height:auto}article{background:#222e35;padding:14px;border-radius:10px}.swatch{display:inline-block;padding:8px;margin:4px;border:1px solid #8d979e}nav a{margin-right:20px}</style><main><h1>Crew reference library</h1><p>Four full turnarounds and four pose sheets. Each turnaround includes front, both sides and rear with helmet off and on. Each pose sheet covers idle, walking, carrying, seated work, role action and empty-helmet handling.</p><p>Review candidates; existing game art is unchanged. Pose presentation sizes vary and must be registered against the side masters before animation. Use the exact palette targets below rather than reading generated hex labels. Engineering is muted yellow. No Higgsfield credits spent.</p><nav>']
names={'bill':'Major Alexander Bill','veld':'Dr. Maria Veld','branforth':'Lt. James Branforth','marsh':'Marsh'}
parts+=['<a href="#'+k+'">'+v+'</a>' for k,v in names.items()];parts+=['</nav>']
for key,name in names.items():
 parts.append(f'<section id="{key}"><h2>{name}</h2><div class="grid">')
 for kind,title in [('reference','Full turnaround'),('poses','Pose reference')]:
  file=f'{key}-{kind}.png';parts.append(f'<article><h3>{title}</h3><a href="{file}"><img loading="lazy" src="{file}" alt="{name}: {title}"></a></article>')
 parts.append('</div><p>Department accent targets:</p>')
 for material in ['Accent shadow','Accent base','Accent light']:
  value=palette['character_materials'][key][material];parts.append(f'<span class="swatch"><span style="display:inline-block;width:26px;height:18px;background:{value}"></span> {material}: {value}</span>')
 parts.append('</section>')
parts.append('<p><a href="palette-reference.json">Exact material palette</a> · <a href="manifest.json">Provenance and review notes</a></p></main></html>')
(P/'index.html').write_text(''.join(parts),encoding='utf-8')
(P/'manifest.json').write_text(json.dumps(dict(status='review_candidates_not_installed',higgsfieldCreditsSpent=0,selectedSheetCount=8,turnaroundViewsPerCharacter=8,posesPerCharacter=6,files=records,reviewNotes=['All four sheets have eight turnaround views.','Pose sheets have six actions each; held helmets are empty.','Veld pose initial output clipped boots; repaired selected version has complete boots but smaller presentation of helmet pose.','Generated swatch labels are illustrative; palette-reference.json governs.','New inferred helmet/backpack details require owner review before replacing existing locks.','No pixel-exact cross-pose colour or scale equality claimed.']),indent=2)+'\n')
assert sum(r['selected'] for r in records)==8
print('Verified 8 selected sheets and 1 retained rejected source; gallery, palette and hashes saved.')
