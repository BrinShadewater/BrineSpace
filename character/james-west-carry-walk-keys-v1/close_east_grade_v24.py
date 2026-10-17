from pathlib import Path
import hashlib,json,os,uuid,time,subprocess
p=Path(__file__).resolve().parent;r=p.parents[1];audit=r/'character/james-full-set-review-2026-10-02/east-inspect-v23';out=r/'character/james-east-inspect-body-grade-v24'
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def save(f,d):f.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
d=json.loads((audit/'review.json').read_bytes());assert all(sha(r/f)==v for f,v in d['sourceSha256'].items())
d.update(visualReviewPending=False,reviewedBoards=2,reviewedSelectedPhases=9,
    findings=['Both enlarged nine-phase comparison boards reviewed. Hair violet cast and cooler suit shadows persist through multiple lift/read/stow phases relative to selected same-direction idle; not isolated to midpoint70.',
    'Prior East matte v3 review and shader inspected: accepted narrow correction addresses tablet, explicitly leaves full hair/face/suit color open. Preserve selected tablet repair.',
    '141 fixed head-region records contain140 distinct crops. This region is a diagnostic, not semantic head segmentation; changing gaze/pose means constant standing-head replacement is not established as appropriate.',
    'No full-cycle visual review, new runtime test or artwork change established by nine sampled phases. Fixed-region chroma medians alone are not a color acceptance metric.'])
save(audit/'review.json',d)
inputs=json.loads((out/'inputs.json').read_bytes());assert all(sha(r/f)==v for f,v in inputs['preCallSha256'].items())
g=json.loads((out/'generation.json').read_text(encoding='utf-8-sig'));assert g['terminal']
review=json.loads((out/'review.json').read_bytes());assert review['rawSha256']==sha(out/'raw.png')
review.update(visualReviewPending=False,sourceAcceptance=False,selected=False,retainedAsColorReference=True,
    disposition='color_reference_only_not_source_replacement',findings=[
    'Raw and native master/source/study comparison reviewed. Hair and suit read more neutral/matte; useful color/material direction.',
    '166 alpha128 silhouette pixels differ despite identical overall bounds. Generated frame also changes equipment visibility/detail and fabric rendering. Not an exact color-only original-pose repair.',
    'Retain as color reference, not one replacement phase in selected141-frame cycle. No source acceptance, native/normal adoption or full-cycle repair inferred.',
    'Next derive bounded native material correction preserving each original pose/alpha and selected tablet/helmet, skin and amber gear; review complete paired cycle and actual loader before adoption.'])
save(out/'review.json',review)
save(out/'generation-index.json',dict(generations=[dict(tool='builtin_image_gen',prompt='prompt.txt',raw='raw.png',rawSha256=review['rawSha256'],terminal=True,
    usedAsRuntimeSource=False,retainedAsColorReference=True,disposition=review['disposition'])],allTerminalAndCopied=True))
rasters=[f.relative_to(r).as_posix() for folder in (audit,out) for f in folder.iterdir() if f.suffix=='.png']
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(x.encode() for x in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert len(attrs)==len(rasters)*3+1 and all(x==b'lfs' for x in attrs[2:-1:3])
section='''### James East diagnostic body color diagnosis — October 2, 2026

V23 enlarged nine normal inspect-East phase comparisons reviewed across lift/read/
stow against selected East idle. Hair violet and cooler fabric shadows persist
over multiple phases, not just midpoint70. Prior selected matte-v3 correction and
review explicitly cover tablet material, leaving hair/face/suit colors open; keep
that accepted tablet repair.141 fixed head-region records/140 distinct crops are
diagnostics,not semantic masks or evidence that a constant master head preserves
tablet-facing gaze. Chroma medians alone are not visual acceptance.
V24 one built-in phase70 material study terminal/copied/raw/native comparison
reviewed. More neutral hair/matte suit retained as color reference only.166 alpha128
pixels differ despite identical bounds;equipment visibility/detail/fabric rendering
also change. Do not insert one generated phase into the141 source cycle or call it
an exact grade-only repair. Raw/prompt/frozen inputs retained,LFS checked.
Next bounded native material correction must preserve authored per-phase poses,
alpha, selected tablet/helmet, skin and amber gear; review whole paired cycle and
actual normal loader before adoption. No new native run or normal source change.
Cargo joins/full James cardinal/context/cross-family polish remain incomplete.
Evidence:character/james-full-set-review-2026-10-02/east-inspect-v23/review.json;
color study/prompts:character/james-east-inspect-body-grade-v24/generation-index.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
    r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
    for attempt in range(3):
        old=path.read_bytes();entry=section.encode()
        if entry.split(b'\n',1)[0] in old:break
        if path.name=='CURRENT_STATUS.md':
            at=old.index(b'### James cardinal action comparison and upper bridge trial');new=old[:at]+entry+b'\n'+old[at:]
        else:new=old+b'\n'+entry
        temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new)
        try:assert path.read_bytes()==old;os.replace(temp,path);break
        except PermissionError:
            temp.unlink()
            if attempt==2:raise
            time.sleep(2)
(out/'HANDOFF.md').write_text('''# Project handoff

## Objective and acceptance
Full James master-matched set and full cardinal/cross-family polish. Incomplete.

## Accepted decisions
Tablet diagnostics faces James; wrench holstered; torch repairs. Preserve poses,
alpha, selected tablet matte correction, skin/amber and helmet coverage.

## Current state
V23 nine sampled normal East inspection phases show sustained hair/fabric violet
drift vs idle. V24 generated phase70 neutral matte study is color reference only;
166 alpha128 differences and changed equipment/detail prevent source replacement.
All raw/prompt/source lineage retained. No normal source/controller changes.

## Verification
Two enlarged phase boards and raw/native study comparison reviewed. All frozen
inputs stable, terminal result copied, LFS and all five guides updated. No new
native run, continuous/full-cycle visual acceptance or owner acceptance.

## Next action
Bounded native material correction preserving original per-phase poses/alpha,
tablet/helmet,skin/amber; complete paired cycle/source/actual-loader review before
adoption. Keep cargo joins and full cardinal/context polish open.
''',encoding='utf-8')
for f in [p/'HANDOFF.md',audit.parent/'HANDOFF.md']:
    old=f.read_text(encoding='utf-8');marker='## V23/V24 East inspection material review\n'
    if marker not in old:
        at=old.index('## Next action\n');old=old[:at]+marker+'''Nine enlarged sampled phases reviewed: hair/fabric violet drift persists through
lift/read/stow. Previous matte-v3 covers tablet, body color still open. V24 neutral
matte phase70 color study retained as reference only,not source replacement:
166 alpha128 changes/equipment/detail drift. Raw/native comparison reviewed,
frozen inputs stable/all terminal/LFS checked/all five guides updated. No native/
normal adoption. Next bounded native material correction with original pose/alpha,
tablet/helmet/skin/amber protection,then full paired cycle and loader review.
Evidence:character/james-east-inspect-body-grade-v24/HANDOFF.md.

'''+old[at:];f.write_text(old,encoding='utf-8')
print(json.dumps(dict(reviewedPhaseBoards=2,sampledPhases=9,retainedColorStudies=1,sourceReplacement=False,guides=5,lfsRasters=len(rasters),normalChanged=False,fullGoalComplete=False)))
