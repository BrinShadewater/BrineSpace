from pathlib import Path
import hashlib,json,shutil
root=Path(__file__).resolve().parents[1];b=root/'character/marsh-retained-gesture-material-v1';o=root/'character/marsh-v2/supplemental/retained-gesture-return-v1';o.mkdir(exist_ok=True);cp=root/'character/marsh-v2/catalog.json';before=json.loads(cp.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def selected(cat):
 result={}
 for rel in cat['body']:
  mp=(cp.parent/rel).resolve();m=json.loads(mp.read_text())
  for state in m['states']:
   result[state['id']]={'sha':[sha(root/f.removeprefix('res://')) if f.startswith('res://') else sha((mp.parent/f).resolve()) for f in state['frameFiles']], 'timing':state.get('frameDurationsMs'), 'loop':state.get('loop')}
 return result
prior=selected(before);candidate=json.loads((b/'cardinal04-unselected/manifest.json').read_text());copied=[]
for d in ['east','west','north','south']:
 state=next(s for s in candidate['states'] if s['id']=='remove-helmet-'+d)
 for i,f in enumerate(state['frameFiles']):
  src=root/f.removeprefix('res://');dst=o/f'{d}-{i:02}.png';assert not dst.exists();shutil.copy2(src,dst);assert sha(src)==sha(dst);copied.append({'from':src.relative_to(root).as_posix(),'path':dst.relative_to(root).as_posix(),'sha256':sha(dst)})
 for s in candidate['states']:
  if s['id'].endswith('-'+d):s['frameFiles']=['res://'+(o/f'{d}-{i:02}.png').relative_to(root).as_posix() for i in range(6)]
candidate['scope']='Selected master-matched latent generic gesture art. Original six150ms finite timing; Marsh helmet behavior stays disabled. Cadence polish/full-set acceptance remain open.'
(o/'manifest.json').write_text(json.dumps(candidate,indent=2)+'\n');relative=o.relative_to(cp.parent).as_posix()+'/manifest.json';assert relative not in before['body'];after=json.loads(json.dumps(before));after['body'].append(relative);post=selected(after);changed=[k for k in prior if prior[k]!=post[k]];assert set(changed)=={s['id'] for s in candidate['states']};assert len(post)==len(prior)
receipt={'catalogBeforeSha256':sha(cp),'catalogBefore':before,'candidateManifestSha256':sha(b/'cardinal04-unselected/manifest.json'),'copiedWholeFrames':copied,'changedStateIds':sorted(changed),'normalSelectedStateCount':len(post),'unchangedOtherStates':len(post)-len(changed),'normalAdmission':True,'fullGoalComplete':False,'ownerVisualAcceptance':False,'cadencePolishOpen':True}
cp.write_text(json.dumps(after,indent=2)+'\n');receipt['catalogAfterSha256']=sha(cp);(o/'admission.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(f'{len(post)}normal states, exactly8changed;{len(post)-8}others preserved,24whole copied slots, helmet behavior unchanged')
