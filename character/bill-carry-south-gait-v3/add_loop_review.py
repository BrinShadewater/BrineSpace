"""Expose authored gait seam separately from finite held-to-walk replay."""
from pathlib import Path
P=Path(__file__).resolve().parent;E=P.parent/'bill-carry-start-south-v2'
old="let first=document.querySelector('#mode').value==='first',t=elapsed%(first?1.07:Math.max(...cases.map(c=>c.duration))+.7)-.25;if(first)t=Math.min(t,.32);"
new="let mode=document.querySelector('#mode').value,first=mode==='first',loop=mode==='loop',t=loop?.32+elapsed%.84:elapsed%(first?1.07:Math.max(...cases.map(c=>c.duration))+.7)-.25;if(first)t=Math.min(t,.32);"
segment="if(t>=0){for(const r of c.timeline){if(r.time>t)break;path=r.path}}"
extra="if(loop)path=`../bill-carry-south-gait-v3/frames/${c.gear}/carry-south/${String(Math.floor(elapsed%.84/.14)).padStart(3,'0')}.png`;"
for name in ['index.html','build_review.py']:
 p=E/name;s=p.read_text(encoding='utf-8')
 if '<option value="loop">Walking loop</option>' not in s:
  assert old in s and segment in s
  s=s.replace('<option value="full">First step and walk</option>','<option value="full">First step and walk</option><option value="loop">Walking loop</option>')
  s=s.replace(old,new).replace(segment,segment+extra)
  s=s.replace("textContent=t<0?'Held master'","textContent=loop?'Walking loop':t<0?'Held master'")
  s=s.replace('at a fixed review pivot.','at a fixed review pivot. Walking loop repeats the six authored gait poses on their 840ms clock to expose the end-to-start join.')
  p.write_text(s,encoding='utf-8')
print('Finite entry replay and authored loop seam are separate review modes')
