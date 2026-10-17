from pathlib import Path
import json,collections
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;read=lambda p:json.loads(p.read_text());s=read(H/'scope-progress.json');packs=s['scopePacks']
for g in ['bare','helmet']:
 for folder in ['krusher-cargo-family-v4','krusher-cargo-settle-profile-v4','krusher-meal-family-v4']:
  path='res://character/'+folder+'/'+g+'-manifest.json'
  if path not in packs[g]:packs[g].append(path)
for path in ['res://character/krusher-meal-service-v4/bare-manifest.json','res://character/krusher-helmet-transition-v4/manifest.json']:
 if path not in packs['bare']:packs['bare'].append(path)
for g in ['bare','helmet']:
 paths=['res://character/krusher-rest-family-v5/'+g+'-manifest.json']
 paths+=['res://character/krusher-recovery-salvage-v3/'+f+'-'+g+'-manifest.json' for f in ['recovery','salvage']]
 paths+=['res://character/krusher-death-family-v3/'+f+'-'+g+'-manifest.json' for f in ['ground','water']]
 for path in paths:
  if path not in packs[g]:packs[g].append(path)
for g in ['bare','helmet']:
 paths=['res://character/krusher-water-family-v4/water-'+g+'-manifest.json']
 paths+=['res://character/krusher-water-cargo-turns-v4/'+f+'-'+g+'-manifest.json' for f in ['cargo','turn','cargo-turn']]
 paths+=['res://character/krusher-water-interruptions-v3/'+f+'-'+g+'-manifest.json' for f in ['cancel','distress']]
 for path in paths:
  if path not in packs[g]:packs[g].append(path)
index=read(R/'character/krusher-animation-package-v3/package.json');required=set(index['states']);coverage=read(R/'character/krusher-complete-animation-v1/source-coverage.json')['resolved'];assert required=={g+':'+sid for g,states in coverage.items() for sid in states};corrected=set()
for g,paths in packs.items():
 for path in paths:
  m=read(R/path[6:])
  for st in m['states']:
   key=g+':'+st['id']
   if key in required:corrected.add(key)
remaining=required-corrected;assert not corrected&remaining and corrected|remaining==required;s.update(correctedStateKeys=sorted(corrected),coveredStates=len(corrected),requiredStates=len(required),remainingStateKeys=sorted(remaining),remainingSourceFamilies=dict(collections.Counter(index['states'][key]['sourceManifest'] for key in sorted(remaining))))
(H/'scope-progress.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps({'corrected':len(corrected),'required':len(required),'remaining':len(remaining)}))
