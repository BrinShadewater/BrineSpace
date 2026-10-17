"""Freeze the current James loader's resolved coverage, including final overrides."""
from pathlib import Path
import collections,hashlib,json,re
P=Path(__file__).resolve().parent;R=P.parent.parent
loader=R/'scripts/grid_canvas.gd';text=loader.read_text();lines=text.splitlines();start=next(i for i,line in enumerate(lines) if 'elif actor == "branforth":' in line)
end=next(i for i in range(start+1,len(lines)) if lines[i].startswith('\t\telif actor') or lines[i].startswith('\t\treplacement_crew_players') or lines[i].startswith('func '))
section='\n'.join(lines[start:end]);catpath=R/'character/chief-engineer-branforth-v2/catalog.json';cat=json.loads(catpath.read_text());packs=[]
for gear,key in [('bare','body'),('helmet','equipment')]:
 for rel in cat[key]:packs.append((gear,'res://'+(catpath.parent/rel).relative_to(R).as_posix()))
for match in re.finditer(r'player\.(load_manifest|load_equipment_manifest)\((?:"diving-helmet",\s*)?"(res://[^"\n]+\.json)"',section):packs.append(('bare' if match[1]=='load_manifest' else 'helmet',match[2]))
resolved={g:{} for g in ['bare','helmet']};sources=[]
for gear,path in packs:
 q=R/path.removeprefix('res://');m=json.loads(q.read_text());sources.append({'gear':gear,'manifest':path,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()})
 for state in m['states']:resolved[gear][state['id']]={'manifest':path,'state':state,'profile':{k:v for k,v in m.items() if k!='states'}}
allpaths=set(re.findall(r'"(res://character/(?:james|chief-engineer-branforth)[^"\n]+\.json)"',text));selected={p for g,p in packs};extras=sorted(allpaths-selected)
data={'scope':'Complete animation coverage of currently resolved James utility-body library. Krusher computer role uses his existing tablet states. Roster/perk/gameplay design outside animation goal.','sourceLoader':'res://scripts/grid_canvas.gd','sourceLoaderHash':hashlib.sha256(loader.read_bytes()).hexdigest(),'sourceLines':[start+1,end],'loadOrder':sources,'resolved':resolved,'additionalLiteralManifestsToAudit':extras}
(P/'source-coverage.json').write_text(json.dumps(data,indent=2)+'\n')
for gear,states in resolved.items():print(json.dumps({'gear':gear,'states':len(states),'references':sum(len(row['state']['frameFiles']) for row in states.values()),'families':dict(collections.Counter(key.split('-')[0] for key in states))}))
print(json.dumps({'orderedManifests':len(packs),'extraLiteralManifestsToAudit':len(extras)}))
