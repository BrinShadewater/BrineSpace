from pathlib import Path
import json,re,hashlib
r=Path(__file__).resolve().parents[2];out=r/'character/james-full-set-review-2026-10-02';out.mkdir(exist_ok=True)
root=r/'character/chief-engineer-branforth-v2';catfile=root/'catalog.json';catalog=json.loads(catfile.read_bytes());grid=r/'scripts/grid_canvas.gd'
selected={'bare':{},'helmet':{}};files=[catfile,grid];load_order=[]
def load(f,kind):
 data=json.loads(f.read_bytes());files.append(f);load_order.append({'kind':kind,'manifest':f.relative_to(r).as_posix()})
 for state in data.get('states',[]):
  refs=[]
  for ref in state.get('frameFiles',[]):
   path=r/ref[6:] if ref.startswith('res://') else f.parent/ref
   refs.append(path.relative_to(r).as_posix())
  selected[kind][state['id']]={'manifest':f.relative_to(r).as_posix(),'id':state['id'],'frameCount':len(refs),'declaredFrameCount':state.get('frameCount'),'frameFiles':refs,'frameDurationsMs':state.get('frameDurationsMs',[]),'loop':state.get('loop'),'pivot':data.get('pivot'),'standingHeight':data.get('standingHeight'),'frameWidth':data.get('frameWidth'),'frameHeight':data.get('frameHeight'),'precomposed':data.get('precomposed',False),'strideDistanceCells':data.get('strideDistanceCells',{}).get(state['id'])}
for kind,key in [('bare','body'),('helmet','equipment')]:
 for path in catalog[key]:load(root/path,kind)
section=grid.read_text(encoding='utf-8').split('elif actor == "branforth":',1)[1].split('\n\t\tset(actor+',1)[0]
for match in re.finditer(r'player\.load_(equipment_manifest|manifest)\((?:"diving-helmet",\s*)?"(res://character/[^\"]+\.json)"',section):
 load(r/match[2][6:],'helmet' if match[1]=='equipment_manifest' else 'bare')
missing=[];bad_counts=[];bad_clocks=[];pairs=[]
for kind,bank in selected.items():
 for key,row in bank.items():
  missing.extend({'kind':kind,'state':key,'source':ref} for ref in row['frameFiles'] if not (r/ref).is_file())
  if row['declaredFrameCount'] is not None and row['declaredFrameCount']!=row['frameCount']:bad_counts.append({'kind':kind,'state':key})
  if len(row['frameDurationsMs']) not in (0,row['frameCount']):bad_clocks.append({'kind':kind,'state':key})
for key in sorted(selected['bare'].keys()&selected['helmet'].keys()):
 a,b=selected['bare'][key],selected['helmet'][key]
 pairs.append({'state':key,'sameFrameCount':a['frameCount']==b['frameCount'],'sameClock':a['frameDurationsMs']==b['frameDurationsMs'],'sameCanvasPivotRuler':all(a[k]==b[k] for k in ['frameWidth','frameHeight','pivot','standingHeight'])})
summary={'bareStates':len(selected['bare']),'helmetStates':len(selected['helmet']),
         'bareFrameReferences':sum(x['frameCount'] for x in selected['bare'].values()),'helmetFrameReferences':sum(x['frameCount'] for x in selected['helmet'].values()),
         'pairedStateIds':len(pairs),'bareOnlyStateIds':sorted(selected['bare'].keys()-selected['helmet'].keys()),'helmetOnlyStateIds':sorted(selected['helmet'].keys()-selected['bare'].keys()),
         'missingFrameSources':len(missing),'invalidDeclaredCounts':len(bad_counts),'invalidClockLengths':len(bad_clocks),'loadedManifests':len(load_order)}
report={'summary':summary,'states':selected,'orderedManifestLoads':load_order,'pairedContracts':pairs,'missingSources':missing,'badCounts':bad_counts,'badClockLengths':bad_clocks,
        'sourceSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in set(files)},
        'normalChanged':False,'visualAcceptance':False,'scope':'Read-only primary literal catalog/grid manifest selection, current worktree. Does not execute equipment composition or James cargo-player/controller special cues; those need separate actual runtime audit. Reference counts do not imply unique authored poses, direction completeness or art/motion acceptance.'}
(out/'source-inventory.json').write_text(json.dumps(report,indent=2)+'\n')
(out/'primary-state-ids.txt').write_text('\n'.join(sorted(selected['bare']))+'\n')
print(json.dumps(summary))
