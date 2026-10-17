from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
def atomic(path,old,new):
    assert path.read_bytes()==old
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(tmp,path)
path=p/'adjacent-bare-v18-review.json';old=path.read_bytes();review=json.loads(old)
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in review['inputSha256'].items())
for version in [17,18]:
    guard=json.loads((p/f'package-upper-v{version}-validation.json').read_bytes())
    package=json.loads((p/f'upper-v{version}-package.json').read_bytes())
    assert guard['exitCode']==0 and guard['realProfileUnchanged'] and package['protectedOriginalPixels']==61476
    assert (p/f'package-upper-v{version}.gd.uid').exists()
    refs=json.loads((p/f'upper-crop-v{version}/references.json').read_bytes())
    assert all(hashlib.sha256((r/x['reference']).read_bytes()).hexdigest()==x['sha256'] for x in refs['references'])
review.update(visualReviewPending=False,selected=False,pairedHelmetGenerated=False,nativeActorMotionRun=False,
    verdict='Rejected after both raw outputs and12registered full-body/upper-crop presentations inspected. Warmer/larger face and badge drift; crown sequence148,148,149,150,149,149 overshoots endpoint149. Largest upper-region pixel step159455 against118680 normal; not perceptual motion proof, but matches visible source drift. Both outside regions exact, normal V9 unchanged. No helmet/full native expansion of failing bare sources.')
atomic(path,old,(json.dumps(review,indent=2)+'\n').encode())
video=r/'character/james-west-cargo-coherent-video-v1';ledger=json.loads((video/'generation.json').read_bytes())
assert ledger['task_id']=='448145326813657' and ledger['status']=='Processing'
section='''### James adjacent source trial and coherent-motion change — October 2, 2026

Built-in bare17/18 early/late upper-crop edits retain both1254raws/exact prompts.
Native packages retain61476original outside pixels each, crop96/56/uniform80/1254,
no grade/pose fitting. Two engine0 scratch intervals/owner unchanged/paired UIDs.
Raws and12registered full-body/crop views inspected; REJECTED: warmer/larger face,
badge drift, crown148,148,149,150,149,149 overshoots endpoint149. Pixel upper peak
159455vs118680normal corroborates drift, not anatomical/perceptual motion proof.
No helmet/native actor expansion. Reference hashes recorded after calls; no pre-
call freeze claimed. Normal V9 source hashes unchanged. Need coherent whole source,
not more independent head/shoulder patches or height normalization.

Read established direct-video skill; normal authorized MiniMax route authenticated.
One Fast2.3/6s/768P motion study submitted from original selected bare West unload0
whole pose, uniformly4x provider input on white; source/prompt/prelaunch hashes
preserved, no invented input raster or per-pose fitting. Existing pure camera/feet/
face/material constraints; small shoulder/case settle-return, not full cargo job.
Task448145326813657 confirmed Processing by real query; no blind resubmission.
Published estimateUS$0.19 rechecked official pricing; actual billing unverified.
Source video still needs review/extraction/master/adjacent endpoint comparison;
no source acceptance, new normal binding or full-set completion. Reserved motion-
transfer run untouched. Goal active/incomplete, no blocker/commit/export.
Evidence: character/james-cargo-return-bridges-v1/adjacent-bare-v18-review.json;
character/james-west-cargo-coherent-video-v1/inputs.json and generation.json.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        marker=b'### James paired enlarged-crop return trial';at=old.index(marker);new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    atomic(path,old,new)
path=r/'character/james-floor-case-west-v1/HANDOFF.md';old=path.read_bytes()
addition=b'\nAdjacent bare17/18 source trials rejected after12registered source/crop views:\nface/badge drift and crown overshoot150 vs terminal149; no helmet/native expansion.\nNext coherent whole motion study: character/james-west-cargo-coherent-video-v1,\ntask448145326813657 confirmed Processing; query saved task, never resubmit.\nSource/prompt/inputs fixed. Review raw whole clip before extraction/admission.\n'
if b'Adjacent bare17/18 source trials rejected' not in old:atomic(path,old,old+addition)
print('Adjacent source rejection/strategy change recorded in five guides and handoff; one verified live video task.')
