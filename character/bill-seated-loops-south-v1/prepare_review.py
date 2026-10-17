from pathlib import Path
P=Path(__file__).resolve().parent
s=(P.parent/'bill-seated-idle-north-v1/build_review.py').read_text(encoding='utf-8').replace('north','south')
s=s.replace('Selected for runtime; native south lounge furniture and interrupted rises verified.','Staged south breathing/reading loops; real observation sofa contact and tablet entry/exit review pending. Runtime unchanged.')
s=s.replace('<p><a href="../bill-seated-south-family-v1/furniture-review.html">Native lounge furniture review</a></p>','')
s=s.replace('<option value="loop">Seated breathing</option>','<option value="loop">Seated breathing</option><option value="reading">Seated reading</option>')
s=s.replace("if(route.value==='loop')return l;","if(route.value==='loop')return l;if(route.value==='reading')return p.find(s=>s.id==='read-seated-south');")
s=s.replace('seated south breathing','south seated breathing and reading').replace('value="reading">','value="reading" selected>')
(P/'build_review.py').write_text(s,encoding='utf-8')
