from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
s=(ROOT/'tools/run_bill_death_ground_helmet_south_candidate_validation.py').read_text(encoding='utf-8').replace('bill-death-ground-helmet-south-candidate-native-v1','bill-death-ground-family-candidate-native-v1').replace('test_bill_death_ground_helmet_south_candidates.gd','test_bill_death_ground_family_candidates.gd').replace('BILL DEATH GROUND HELMET SOUTH','BILL DEATH GROUND FAMILY')
(ROOT/'tools/run_bill_death_ground_family_candidate_validation.py').write_text(s,encoding='utf-8')
s=(P.parent/'bill-death-ground-helmet-south-coherent-v1/index.html').read_text(encoding='utf-8').replace('Bill south helmet ground collapse candidate','Bill paired cardinal dry collapse family').replace('Bill — south helmet ground collapse','Bill — paired cardinal dry collapse candidates')
s=s.replace('<select id="size">','<select id="gear"><option value="manifest.json">Bare</option><option value="helmet-manifest.json">Helmet</option></select><select id="facing"><option>east</option><option>west</option><option>north</option><option>south</option></select><select id="size">')
s=s.replace("fetch('manifest.json').then", "gear.onchange=()=>location.href='?gear='+gear.value+'&direction='+facing.value;facing.onchange=gear.onchange;const query=new URLSearchParams(location.search);gear.value=query.get('gear')||'manifest.json';facing.value=query.get('direction')||'east';fetch(gear.value).then")
s=s.replace('const s=m.states[0]',"const s=m.states.find(s=>s.id==='death-ground-'+facing.value)").replace('im.src=f','im.src=f.startsWith(\'res://\')?\'/\'+f.slice(6):f')
(P/'index.html').write_text(s,encoding='utf-8')
