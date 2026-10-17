from pathlib import Path
import json,hashlib,os,uuid,time,subprocess
import numpy as np
from PIL import Image
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'sleeve-phase24-v63';window=p/'middle-window-v63';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
inputs=json.loads((out/'inputs.json').read_bytes())
for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==v for f,v in inputs[group].items())
assert sha(out/'prompt.txt')==inputs['promptSha256']
frozen=json.loads((window/'inputs.json').read_bytes());assert all(sha(r/f)==v for f,v in frozen['preLaunchSha256'].items())
native=json.loads((window/'native-evidence.json').read_bytes());validation=json.loads((window/'native_probe-validation.json').read_bytes());assert native['checks']==47 and native['failures']==0 and validation['exitCode']==0 and validation['realProfileUnchanged'] and not validation['profileDelta']
for slot in [0,2]:assert sha(window/f'native/middle-{slot:03d}.png')==sha(p/f'middle-window-v62/native/middle-{slot:03d}.png')
samples={}
for label,f in [('before',p/'narrow-grip-phase24-v62/bare-candidate.png'),('after',out/'bare-candidate.png'),('previous',p/'master-material-phase23-v58/bare-head-protected.png'),('next',p/'master-material-phase25-v59/bare-head-protected.png')]:
    rgb=np.asarray(Image.open(f).convert('RGBA'))[112:128,128:146,:3];samples[label]=np.quantile(rgb@np.array([.2126,.7152,.0722]),[.25,.5,.75,.95]).round(2).tolist()
d=json.loads((out/'review.json').read_bytes());d.update(visualReviewPending=False,reviewedSourceBoards=2,reviewedNativeMidpoint=True,otherNativeEndpointsExactReviewedV62=True,nativeChecks=47,nativeFailures=0,disposition='retain_local_sleeve_repair_for_full_motion_review',sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,diagnosticLumaQuartilesAnd95=samples,findings=['Subdued sleeve highlights closer to actual neighbouring frame materials; original quilting remains readable.','65088outside pixels exact to preceding V62candidate, tophead/helmet and pixels below138 exact; does not certify untouched original-master proportions.','Local brightness95th percentile159.15to150.77 versus neighbouring147.87/145.50; diagnostic only, not visual acceptance gate.','Native120ms three-frame source window47/0; not complete49source motion/controller/room/Continue acceptance.']);d['artifactSha256']={f.name:sha(f) for f in out.glob('*.png')};(out/'review.json').write_text(json.dumps(d,indent=2)+'\n')
(out/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution='6fbbd471-9558-4da5-802c-065d9011b81e',rawSha256=sha(out/'raw.png'),prompt='prompt.txt',inputs='inputs.json',normalChanged=False),indent=2)+'\n')
mapping={0:p/'master-material-v49',12:p/'master-material-phase12-v51',23:p/'master-material-phase23-v58',24:out,25:p/'master-material-phase25-v59',36:p/'master-material-phase36-v53',48:p/'master-material-phase48-v55'}
records=[]
for phase in range(49):
    row=dict(phase=phase,repairCandidateAvailable=phase in mapping,sourceAcceptance=False)
    if phase in mapping:
        folder=mapping[phase];suffix='-candidate.png' if phase==24 else '-head-protected.png'
        row['candidateSources']={mode:dict(file=(folder/(mode+suffix)).relative_to(r).as_posix(),sha256=sha(folder/(mode+suffix))) for mode in ['bare','helmet']}
        row['reviewStatus']='provisional_material_candidate_geometry_contact_motion_pending'
    records.append(row)
(p/'material-repair-progress.json').write_text(json.dumps(dict(totalOriginalFrames=49,candidatePhases=7,remainingSourcePhases=[x for x in range(49) if x not in mapping],normalChanged=False,sourceAcceptance=False,fullGoalComplete=False,scope='Authored material-source progress only; all candidates still require whole-family master/contact/motion acceptance.',states=records),indent=2)+'\n')
section='''### James middle carrying sleeve highlight repair — October 2, 2026

V63builtin local48square sleeve edit uses actual V62middle pose as target and
immediately preceding/following V58/V59poses plus original master as material
references. Raw/prompt/precall hashes retained. Full square normalized once48;
only two sleeve rectangles admitted,448pixels;65088outside pixels exact to V62base.
Head/helmet, case front/grip below138 and legs protected; paired body below110 exact.
Two sleeve/contact source boards and native midpoint reviewed. Highlights more
subdued, quilting remains visible. Diagnostic local95thpercentile159.15to150.77,
neighbours147.87/145.50; distributions support comparison, never certify fidelity.

Rebuilt same consecutive23/24/25window at40/40/40ms. Native47/0, three captures;
midpoint reviewed, endpoints byte-exact to reviewed V62captures. Owner profile
unchanged under scratchAPPDATA. APNG three decoded poses/clocks exact. No new
browser continuous-motion claim. No normal selection/controller/art changes.
New material-repair-progress.json lists all49source slots: seven have provisional
paired repair candidates,42still need sources; all source-acceptance flags false.
Full body/gear/case geometry, sole-row variation and full-motion/context remain open.

Lesson: direct reference to immediately neighbouring sleeves improves a local
material repair without changing pose. Protect prior case/head/leg repairs, measure
actual emitted pixels and inspect the whole figure; neither isolated brightness
nor an exact pivot proves original anatomy or continuous consistency. Next extend
coherent finish across remaining gait frames, complete motion/normal integration
and full James master/cross-family consistency polish. Goal incomplete.
Evidence:character/james-west-carry-walk-keys-v1/sleeve-phase24-v63/review.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
    old=f.read_bytes();entry=section.encode()
    if entry.split(b'\n',1)[0] in old:continue
    if f.name=='CURRENT_STATUS.md':
        at=old.index('### James consecutive carrying window and grip admission review'.encode());new=old[:at]+entry+b'\n'+old[at:]
    else:new=old+b'\n'+entry
    tmp=f.with_name(f.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    try:
        for attempt in range(5):
            assert f.read_bytes()==old
            try:os.replace(tmp,f);break
            except PermissionError:
                if attempt==4:raise
                time.sleep(1)
    finally:
        if tmp.exists():tmp.unlink()
for folder in [out,window]:(folder/'HANDOFF.md').write_text('# Project handoff\n\nObjective: full James master-matched animation library and polish; incomplete.\n\n'+section+'\nChanged: V63local source/candidate pair and source/native evidence, helpers, progress ledger and five guides. No normal code/art changes, commit/PR/export. Generation/engine runs terminal; no active handles.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('ab') as f:f.write(b'\n'+section.encode())
rasters=[f.relative_to(r).as_posix() for folder in [out,window] for f in folder.rglob('*') if f.suffix in ['.png','.apng']]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(f.encode() for f in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0');assert all(v==b'lfs' for v in attrs[2:-1:3])
print(json.dumps(dict(nativeChecks=47,failures=0,outsidePixelsExact=65088,candidatePhases=7,remainingPhases=42,guides=5,lfsRasters=len(rasters),normalChanged=False)))
