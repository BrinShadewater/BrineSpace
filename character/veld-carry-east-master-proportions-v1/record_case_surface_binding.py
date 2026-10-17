from pathlib import Path
import hashlib,json,os,time,shutil,urllib.request
P=Path(__file__).resolve().parent;R=P.parents[1];O=P/'whole-pose-join-v4/material-review/case-review-v2'
for v,e,refs in [('23','912c7ca0-912c-41d1-a1d4-682af6c10aa9',['case-surface-edit-target.png']),('24','34475d13-0af8-48d8-95a1-87bc2b0bd0ec',['case-passing-edit-target.png','raw-case-surface-v23.png'])]:
 raw=P/f'raw-case-surface-v{v}.png'
 refdata=[{'path':p,'sha256':hashlib.sha256((P/p).read_bytes()).hexdigest()} for p in refs]
 (P/f'references-case-surface-v{v}.json').write_text(json.dumps(refdata,indent=2)+'\n',encoding='utf-8')
 (P/f'execution-case-surface-v{v}.json').write_text(json.dumps({'tool':'builtin image_gen','execution':e,'workspaceSource':raw.name,'sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'prompt':f'prompt-case-surface-v{v}.txt','references':f'references-case-surface-v{v}.json','status':'reviewed_localized_rigid_equipment_source','usage':'Generated RGB only within exposed lid/right casing native masks; original pose/anatomy/alpha/grip/clasp retained.','scope':'Staged source only; no helmet/native/normal selection.'},indent=2)+'\n',encoding='utf-8')
evidence=json.loads((O/'review-evidence.json').read_text());evidence['visualReview']='Seven whole/case comparison columns and six masks inspected. Generated close-ups23/24 have smooth hard shell; consumed lid/right panels closer in tone and free of prominent quilted pattern. Original clasp/grip still differ slightly between authored poses; final whole-case/detail/cadence acceptance pending. Two changed paused browser poses and playing snapshot inspected.'
evidence['browserReview']=json.loads((O/'browser-review/samples.json').read_text());evidence['previewVerification']=[]
for name in ['index.html','cycle.png','case-master-comparison.png']:
 with urllib.request.urlopen('http://127.0.0.1:8791/character/veld-carry-east-master-proportions-v1/whole-pose-join-v4/material-review/case-review-v2/'+name) as response:
  exact=response.read()==(O/name).read_bytes();assert response.status==200 and exact;evidence['previewVerification'].append({'file':name,'status':200,'exactBytes':exact})
for b in evidence['bindings']:
 assert hashlib.sha256((P/b['originalPose']).read_bytes()).hexdigest()==b['registration']['sourceSHA256']
evidence['status']='reviewed_surface_binding_staged';(O/'review-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
block='''## Veld East authored case-surface binding — October 2, 2026

Full-body case edits21/22 retain unwanted pattern and change outside-case pixels;
rejected, raw/prompt/reference hashes retained. Exact original case close-ups23/24
produce smooth graphite hard shells. bind_authored_case_surfaces.py extracts only
generated RGB in native lid/right-panel masks for phases2/4, using original pose
registration and unchanged shared case curve. No generated anatomy or alpha used.
41checks0fail: exact alpha/outside masks/clasp, glove exclusion, other4poses exact
to prior candidate,6exact140ms APNGframes/840ms. Phase2/4masked mean61.10/61.34
becomes55.65/56.74 (other poses53.04-54.41). All7whole/case comparisons and6masks
inspected; both authored close-ups inspected. Smooth panels closer to master;
original clasp/grip variation and final whole-case/cadence acceptance remain.
Actual browser two changed paused poses plus playing snapshot inspected/saved;
page advances,3HTTPfiles200/exact. No native/normal-selection/owner-save changes.

Lesson: isolate a rigid equipment-material edit in an exact source crop when a
whole-character edit changes unrelated pixels. Consume only exposed equipment
surfaces, explicitly protect hands/clasp/alpha, retain original whole-pose ruler
and clock. Generated smooth material does not prove case geometry or motion.
Next inspect remaining case/clasp detail, pair original shared East helmet,
package and native30Hz two-cycle review; full cargo/world/Continue/polish open.
Review: character/veld-carry-east-master-proportions-v1/whole-pose-join-v4/material-review/case-review-v2/.

'''
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for path in paths:
 for attempt in range(5):
  with path.open('rb') as f:head=f.read(65536)
  if block.splitlines()[0].encode() in head:break
  before=path.stat();tmp=path.with_name(path.name+'.veld-surfaces.tmp')
  with tmp.open('wb') as dest,path.open('rb') as src:
   dest.write(block.encode());shutil.copyfileobj(src,dest,1024*1024)
  after=path.stat()
  if (before.st_mtime_ns,before.st_size)!=(after.st_mtime_ns,after.st_size):tmp.unlink();continue
  try:os.replace(tmp,path);break
  except PermissionError:tmp.unlink(missing_ok=True);time.sleep(.5)
 else:raise RuntimeError(f'Concurrent update prevented {path}')
with (P/'SOURCE_REVIEW.md').open('a',encoding='utf-8') as f:f.write('\n'+block)
for path in [P/'HANDOFF.md',R/'character/veld-cargo-turns-master-family-v1/HANDOFF.md']:
 source=path.read_text(encoding='utf-8');start=source.index('## Next action');source=source[:start]+block+'''## Next action
Inspect remaining case/clasp detail, then original shared East helmet pairing,
staged package and native30Hz two-cycle proof. Preserve complete registered anatomy,
source density and six140ms clock. East actions/South/North cargo/master matching,
actual world ownership/interruption/Continue, guarded adoption and full-set polish
remain open. The full Veld goal remains active and incomplete.
''';path.write_text(source,encoding='utf-8')
print(json.dumps({'surfaceChecks':41,'failures':0,'authoredCloseups':2,'protectedBodyPoses':6,'unchangedOtherPoses':4,'httpExactFiles':3,'maintainedReferences':5,'handoffs':2,'scope':'staged equipment surfaces; full goal incomplete'}))
