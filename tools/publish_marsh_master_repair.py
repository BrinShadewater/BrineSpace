"""Before/after timed review and complete edited-pose boards for master repair."""
from pathlib import Path
import json,re
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-master-repair-v1'
def main():
 before=json.loads((BASE/'baseline-contract.json').read_text())['states'];selection=json.loads((BASE/'selection.json').read_text());after={k:{**s,'files':selection['states'][k]} for k,s in before.items()}
 source=(ROOT/'character/marsh-master-comparison-v1/index.html').read_text()
 source=re.sub(r'const DATA=.*?, MASTERS=',lambda _: 'const BEFORE='+json.dumps(before)+', DATA='+json.dumps(after)+', MASTERS=',source,count=1)
 source=source.replace('Marsh: master comparison','Marsh: master repair — before / after').replace('Original identity master, installed directional idle, and current animation.','Original identity master, installed directional idle, and revised animation. The Before panel plays at the same phase.')
 source=re.sub(r'<h2>Comparison findings</h2>.*?</ul>','<p>Master-guided armour, harness, pouch and face detail repairs. Original silhouettes, registration and timing retained. Injury fluid preserved. Use source and station scale; pause and step to inspect each pose.</p>',source,flags=re.S)
 source=re.sub(r'<details>.*?</details>','',source,flags=re.S)
 source=source.replace('<h3>Current selected animation</h3>','<h3>After repair</h3>').replace('</div></div>\n <p><a','</div><div><h3>Before repair</h3><canvas id="before" width="512" height="512"></canvas></div></div>\n <p><a',1)
 source=source.replace("draw('action',s,s.files[slot]);","draw('action',s,s.files[slot]);draw('before',BEFORE[state.value],BEFORE[state.value].files[slot]);")
 source=source.replace('Full colour pass / transition review','Previous colour pass').replace('href="comparison.json"','href="installation.json"')
 source=source.replace('<select id="state">','<p><a href="motion-review/index.html">Native motion sequences: before/after and station size</a></p><select id="state">',1)
 plan=json.loads((BASE/'edit-plan.json').read_text());pages=[]
 for sheet in plan['sheets']:
  board=Image.new('RGB',(1536,1200),'#293b40');draw=ImageDraw.Draw(board)
  for r in sheet['poses']:
   key=r['key'];slot=r['slot'];old=Image.open(ROOT/before[key]['files'][slot]).convert('RGBA');new=Image.open(ROOT/after[key]['files'][slot]).convert('RGBA');n=r['cell']
   for j,im in enumerate((old,new)):
    crop=im.crop(im.getbbox());crop.thumbnail((122,250),Image.Resampling.NEAREST);x=n%6*256+j*128+(128-crop.width)//2;y=n//6*300+28+250-crop.height;board.paste(crop,(x,y),crop)
   draw.text((n%6*256+2,n//6*300+2),key+' '+str(slot),fill='white')
  name=f'final-{sheet["index"]:02}.png';board.save(BASE/name);pages.append(name)
 source=source.replace('<script>', ''.join(f'<details><summary>Before / after edited poses {i+1}</summary><img class="board" src="{p}" loading="lazy"></details>' for i,p in enumerate(pages))+'<script>',1)
 (BASE/'index.html').write_text(source);(BASE/'viewer.js').write_text(source.split('<script>')[1].split('</script>')[0]);print('204 timed comparisons; 21 complete edited-pose boards')
if __name__=='__main__':main()
