from pathlib import Path
import json,hashlib,os,uuid,time,subprocess
p=Path(__file__).resolve().parent;r=p.parents[1];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for version in [60,61,62]:
    out=p/f'middle-window-v{version}';inputs=json.loads((out/'inputs.json').read_bytes());assert all(sha(r/f)==v for f,v in inputs['preLaunchSha256'].items())
    native=json.loads((out/'native-evidence.json').read_bytes());validation=json.loads((out/'native_probe-validation.json').read_bytes());assert native['checks']==47 and native['failures']==0 and native['captures']==3 and validation['exitCode']==0 and validation['realProfileUnchanged'] and not validation['profileDelta']
    (out/'review.json').write_text(json.dumps(dict(nativeChecks=47,nativeFailures=0,reviewedNativeCaptures=3 if version!=62 else 1,otherTwoCapturesExactReviewedV61=True if version==62 else False,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,scope='Six source slots, three consecutive40ms phases23/24/25, paired four-size native captures. Not full49 walking cycle or controller/room/Continue.',findings=['Broad grip admission returns old sleeve context; narrowing improves protection.','Residual sleeve-detail mismatch belongs to V52material source as well; local case protection does not establish whole-body consistency.']),indent=2)+'\n')
for slot in [0,2]:assert sha(p/f'middle-window-v62/native/middle-{slot:03d}.png')==sha(p/f'middle-window-v61/native/middle-{slot:03d}.png')
for phase,version,execution in [(23,58,'28d3d6b3-5994-4c36-9fcc-b3785bc42796'),(25,59,'0dac1dd6-3b2e-4405-b62a-58a1ba133d93')]:
    out=p/f'master-material-phase{phase}-v{version}';inputs=json.loads((out/'inputs.json').read_bytes())
    for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==v for f,v in inputs[group].items())
    d=json.loads((out/'package-review.json').read_bytes());d.update(visualReviewPending=False,reviewedPairedBoard=True,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,disposition='retained_adjacent_material_candidate_consistency_pending');(out/'package-review.json').write_text(json.dumps(d,indent=2)+'\n');(out/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution=execution,rawSha256=sha(out/'raw.png'),prompt='prompt.txt',inputs='inputs.json'),indent=2)+'\n')
old=p/'case-grip-material-phase24-v57/review.json';d=json.loads(old.read_bytes());d.update(disposition='superseded_broad_admission_returns_sleeve_context',sourceAcceptance=False,followup='narrow-grip-phase24-v62');old.write_text(json.dumps(d,indent=2)+'\n')
(p/'middle-window-v62/browser-evidence.json').write_text(json.dumps(dict(tab=5,url='http://127.0.0.1:8340/',sourceSlots=[0,1,2],observedElapsedMs=[0,50,83.4],complete=True,observedEndMs=133.4,sourceDurationMs=120,scope='Browser playback and final display verified; requestAnimationFrame presentation adds latency. Not uninterrupted artistic motion acceptance.',tabClosed=True,serverSession=73195,serverStopped=True),indent=2)+'\n')
section='''### James consecutive carrying window and grip admission review — October 2, 2026

V58phase23/V59phase25 material edits retained with raw/prompt/input hashes;
paired source boards reviewed. Three consecutive sources23/24/25 use original
40/40/40ms clocks. V60native47/0, three paired four-size captures reviewed. Native
comparison exposed old sleeve context returned by V57broad grip admission.
V61narrower trial47/0, three captures reviewed; V62three separate case/glove boxes
protect64348outside pixels to V52base, excluding more forearm context. No new
generation or color painting for these admission revisions. V57broad selection
superseded, all originals retained. V62native47/0, midpoint reviewed; other two
captures byte-exact to reviewed V61captures. All real-profile fingerprints unchanged.

Residual central sleeve detail differs from neighbours and also exists in V52base:
patch protection does not prove whole material consistency. All remain staged and
unselected, with whole-body proportion/contact/sole variation concerns open.
Only seven distinct repair phases0/12/23/24/25/36/48, not complete49source coverage.
Exact three-frame APNG decode proves pixels/clocks, not full motion acceptance.
Browser played120ms native-capture window, all3slots observed at0/50/83.4ms;
complete133.4ms due presentation latency. Final display inspected. Tab5closed and
local server73195stopped; no live handles. Full controller/rooms/Continue unproved.

Lesson: local generation preserves context from its edit target. Admit only actual
case/glove parts, not a broad wrist rectangle containing old sleeve/torso artwork.
Review neighbouring frames at actual sizes and locate residual differences in the
base source before blaming the patch. Native clock passes can reveal visual defects
but never override them. Next coherent sleeve/detail source repair, remaining gait
frames, complete motion and normal integration; full James set/polish incomplete.
Evidence:character/james-west-carry-walk-keys-v1/middle-window-v62/review.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
    old=f.read_bytes();entry=section.encode()
    if entry.split(b'\n',1)[0] in old:continue
    if f.name=='CURRENT_STATUS.md':
        at=old.index('### James middle carrying grip local material study'.encode());new=old[:at]+entry+b'\n'+old[at:]
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
folders=[p/f'middle-window-v{v}' for v in [60,61,62]]+[p/f'narrow-grip-phase24-v{v}' for v in [61,62]]+[p/'master-material-phase23-v58',p/'master-material-phase25-v59']
for out in folders:(out/'HANDOFF.md').write_text('# Project handoff\n\nObjective: full James master-matched library and consistency polish; incomplete.\n\n'+section+'\nChanged: adjacent material sources, narrowed admission derivatives, native/source/browser evidence, helpers and five guides. Normal source registry/controller unchanged. No commit/PR/export.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('ab') as f:f.write(b'\n'+section.encode())
rasters=[f.relative_to(r).as_posix() for folder in folders for f in folder.rglob('*') if f.suffix in ['.png','.apng']]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(f.encode() for f in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0');assert all(v==b'lfs' for v in attrs[2:-1:3])
print(json.dumps(dict(finalNativeChecks=47,failures=0,sourcePhases=7,guides=5,lfsRasters=len(rasters),normalChanged=False,fullGoalComplete=False)))
