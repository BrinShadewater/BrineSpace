from pathlib import Path
import json,copy
H=Path(__file__).resolve().parent;R=H.parents[1];read=lambda p:json.loads(p.read_text());P=R/'character/krusher-animation-package-v8';index=read(P/'package.json');sourceidx=read(R/'character/krusher-head-fit-v7/source-bank-index.json');meta={};derived={}
canonroot=R/'character/krusher-james-canonical-v9';canon=read(canonroot/'revision.json')['records'];priorroot=R/'character/krusher-james-canonical-v6';prior={(q['gear'],q['state'],q['index']):q for q in read(priorroot/'revision.json')['records']}
fits={(q['state'],q['frame']):q for q in read(R/'character/krusher-james-motion-fit-v2/verification.json')['records']};helm={(q['state'],q['frame']):q for q in read(R/'character/krusher-james-helmet-fit-v2/verification.json')['records']};cm={}
for q in canon:
 g=q['gear'];key=q['state'];d=key.rsplit('-',1)[1];i=q['index'];body=None
 if key.startswith('interact-'):
  folder=R/'character'/('krusher-tablet-'+d+('-helmet' if g=='helmet' else '')+'-v1');row=read(folder/'verification.json')['records'][i];body=row['source']
 else:row=(fits if g=='bare' else helm)[key,i];body=row['source']
 details={'headSource':'res://character/krusher-head-fit-v5/sources/clean-bare-'+d+'-native.png','paste':q['headPaste'],'bodyAxis':[0,1]}
 if g=='helmet' and d=='north':details={}
 info={'gear':g,'state':key,'frame':i,'direction':d,'originalBody':body,'details':details,'mask':str((priorroot/prior[g,key,i]['mask']).relative_to(R)) if g=='helmet' and d!='north' else None,'canonical':True}
 meta[(canonroot/q['output']).relative_to(R).as_posix()]=info;cm[g,key,i]=info
for folder in set(path[6:].rsplit('/',1)[0] for paths in sourceidx['candidatePacks'].values() for path in paths):
 root=R/folder
 if root==canonroot or not (root/'revision.json').exists():continue
 rev=read(root/'revision.json');base=root.name.rsplit('-v',1)[0];oldroot=R/'character'/(base+'-v'+('2' if base.endswith('water-cargo-turns') else '1'));oldrows=read(oldroot/'provenance.json')['records'] if (oldroot/'provenance.json').exists() else []
 for path,q in rev.get('derivedSources',{}).items():derived[(root/path).relative_to(R).as_posix()]=q
 for q in rev.get('records',[]):
  if q['output'].startswith('res://'):continue
  details=q.get('details',{});g=q['gear'];sid=q['state'];direction=details.get('view',q.get('view',sid.rsplit('-',1)[-1]));body=q.get('originalBody')
  if body:body=body.removeprefix('res://')
  if not body:
   match=next((o for o in oldrows if o.get('output')==q['output']),None)
   if match is None:match=next((o for o in oldrows if o.get('gear')==g and o.get('state')==sid and o.get('frame')==q.get('frame')),None)
   if match is None and 'newSourceIndex' in details:match=next((o for o in oldrows if o.get('newSourceIndex')==details['newSourceIndex']),None)
   if match is None and 'pose' in details:match=next((o for o in oldrows if o.get('pose')==details['pose']),None)
   if match:body=match['source'].removeprefix('res://')
  info={'gear':g,'state':sid,'frame':q.get('frame',0),'direction':direction,'originalBody':body,'details':details,'mask':str((root/q['mask']).relative_to(R)) if q.get('mask') else None,'root':root.relative_to(R).as_posix()}
  endpoint=details.get('canonicalEndpoint');cg=details.get('canonicalGearEndpoint')
  if endpoint or cg or 'canonicalTabletPose' in details:
   cg=cg or g;d=endpoint or ('east' if cg!=g else direction);key=('interact-' if 'canonicalTabletPose' in details else 'idle-')+d;i=details.get('canonicalTabletPose',0)
   if (cg,key,i) in cm:
    info=copy.deepcopy(cm[cg,key,i]);info['paddedCanonical']=True;info['aliasState']=sid
  meta[(root/q['output']).relative_to(R).as_posix()]=info
palette=read(R/'character/krusher-coherent-bank-v2/palette-validation.json')['records'];byoutput={}
for q in palette:
 info=meta.get(q['source'])
 if info:byoutput.setdefault('character/krusher-coherent-bank-v2/'+q['output'],[]).append(info)
selected={};missing=[]
for full,q in index['states'].items():
 gear,key=full.split(':',1);mp=P/q['manifest'];m=read(mp);s=next(s for s in m['states'] if s['id']==key)
 for i,(f,src) in enumerate(zip(s['frameFiles'],q['sourceFrames'])):
  packed=(mp.parent/f).resolve().relative_to(P.resolve()).as_posix()
  if packed in selected:continue
  candidates=byoutput.get(src,[])
  if not candidates:missing.append({'state':full,'frame':i,'source':src,'problem':'no metadata'});continue
  candidates=sorted(candidates,key=lambda info:(not bool(info['details'].get('headSource')),not info.get('canonical',False),info['state']))
  info=copy.deepcopy(candidates[0]);hashead=bool(info['details'].get('headSource'))
  rear=info['gear']=='helmet' and (info['direction'] in ['north','ne','nw'] or info['state'].endswith('north'))
  if not hashead and not rear:missing.append({'state':full,'frame':i,'source':src,'problem':'no head anatomy','candidates':candidates[:2]});continue
  info.update({'source':packed,'example':full,'exampleFrame':i,'canvas':[m['frameWidth'],m['frameHeight']],'pivot':m['pivot'],'noVisibleHead':not hashead});selected[packed]=info
(H/'bank-mapping.json').write_text(json.dumps({'records':selected,'derivedSources':derived,'missing':missing},indent=2)+'\n');print(json.dumps({'selectedUniquePNG':len(index['files']),'mapped':len(selected),'missing':len(missing),'examples':missing[:4]}))
if missing:raise SystemExit(1)
