from pathlib import Path
import hashlib,json,os,uuid,time,subprocess
p=Path(__file__).resolve().parent;r=p.parents[1];upper=p/'upper-bridge-v21';audit=r/'character/james-full-set-review-2026-10-02/cardinals-v22'
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def save(f,d):f.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
inputs=json.loads((upper/'inputs.json').read_bytes());assert all(sha(r/f)==v for f,v in inputs['preCallSha256'].items())
generation=json.loads((upper/'generation.json').read_text(encoding='utf-8-sig'));assert generation['terminal']
findings=['Raw and paired whole/body four-pose source boards reviewed.',
    'Case shifts too far forward relative to preceding and following sources, while torso remains close to broad standing profile. The source adds case translation rather than a convincing progressive upper-body rotation.',
    'Head/collar and V20 legs remain exact outside60934 guard; this does not certify case perspective or coherent chronology.',
    'Rejected as transition source. V20 lower-body study retained; no finite clip, native run or normal runtime adoption.']
review=json.loads((upper/'review.json').read_bytes());assert review['rawSha256']==sha(upper/'raw.png')
review.update(visualReviewPending=False,sourceAcceptance=False,selected=False,disposition='rejected_case_overshoot_insufficient_torso_progression',findings=findings)
save(upper/'review.json',review)
chain=json.loads((upper/'chain-review.json').read_bytes());assert all(sha(r/f)==v for f,v in chain['sourceSha256'].items())
chain.update(visualReviewPending=False,sourceAcceptance=False,selected=False,findings=findings,reviewedBoards=2);save(upper/'chain-review.json',chain)
save(upper/'generation-index.json',dict(generations=[dict(tool='builtin_image_gen',prompt='prompt.txt',raw='raw.png',rawSha256=review['rawSha256'],terminal=True,used=False,disposition=review['disposition'])],allTerminalAndCopied=True))
d=json.loads((audit/'review.json').read_bytes());assert all(sha(r/f)==v for f,v in d['sourceSha256'].items());assert len(d['records'])==64
d.update(visualReviewPending=False,reviewedBoards=4,displayedSlots=64,selectedActionPhaseSlots=48,
    findings=['Four bare cardinal idle/walk/repair/inspect boards reviewed at identical pivot/ruler. No silhouette-fitting or canvas-based height inference.',
    'East inspection midpoint appears cooler/purpler than its same-direction idle and inspection endpoints. Priority follow-up: inspect enlarged source and adjacent phases before changing artwork; first/mid/last cannot locate a flash.',
    'Repair poses use differing knee depth and torch work-plane orientations. Review complete tool phases and room/task context against owner decisions before treating those differences as defects.',
    'Walking widths and foot-contact bounds differ from idle. Posture/stride changes alone do not establish scale drift; full-cycle registered comparisons remain necessary.',
    'No helmet, continuous cadence, room/scheduler or owner acceptance established by these64 static slots. No source artwork changed.'],
    nextPriority='East inspection midpoint and adjacent-phase material/master comparison',normalChanged=False,nativeRun=False,fullGoalComplete=False)
save(audit/'review.json',d)
rasters=[f.relative_to(r).as_posix() for folder in (upper,audit) for f in folder.iterdir() if f.suffix=='.png']
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(x.encode() for x in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert len(attrs)==len(rasters)*3+1 and all(x==b'lfs' for x in attrs[2:-1:3])
section='''### James cardinal action comparison and upper bridge trial — October 2, 2026

V21 upper-body-only carrying edit terminal/copied/raw and paired whole/body boards
reviewed. Rejected: case moves too far forward while torso fails to progressively
rotate into walk0.60934 outside pixels/head/collar/V20 legs exact; that guard does
not establish rigid-case perspective or motion acceptance. V20 leg study retained;
no finite clip or normal/native adoption. Do not build a bridge from failed sources.
V22 four normal bare cardinal idle/walk/repair/inspect boards reviewed:64 displayed
slots,48 selected first/middle/last action-phase slots at exact declared pivot/148
ruler. East inspection midpoint appears cooler/purpler than same-direction idle
and inspection endpoints: next enlarged source/adjacent-phase comparison before
repair. Static samples cannot locate a flash or certify a full cycle. Repair tool
planes/knee depth differ; check all tool phases and task/room context against owner
choices before changing them. Walking stride/width differences alone are not size
defects; never fit bounding boxes to manufacture height consistency.
No helmet/room/scheduler/continuous owner acceptance this turn. All generation
lineage retained,LFS checked. Full goal remains incomplete; keep cargo joins open
while addressing other action-family consistency findings.
Evidence:character/james-full-set-review-2026-10-02/cardinals-v22/review.json;
prompts:character/james-west-carry-walk-keys-v1/upper-bridge-v21/generation-index.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
    r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
    for attempt in range(3):
        old=path.read_bytes();entry=section.encode()
        if entry.split(b'\n',1)[0] in old:break
        if path.name=='CURRENT_STATUS.md':
            at=old.index(b'### James carrying lower-body source study');new=old[:at]+entry+b'\n'+old[at:]
        else:new=old+b'\n'+entry
        temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new)
        try:assert path.read_bytes()==old;os.replace(temp,path);break
        except PermissionError:
            temp.unlink()
            if attempt==2:raise
            time.sleep(2)
for f in [p/'HANDOFF.md',audit.parent/'HANDOFF.md']:
    old=f.read_text(encoding='utf-8');marker='## V21/V22 latest review\n'
    if marker not in old:
        at=old.index('## Next action\n')
        old=old[:at]+marker+'''V21 upper-only bridge trial rejected after raw/two paired boards review: case
forward overshoot and inadequate torso progression.60934 protected pixels/frozen
inputs exact;all terminal/copied,no finite/native/normal adoption. V20 leg study
retained. V22 four bare cardinal action boards reviewed,64 displayed slots/48
selected first/mid/last phase slots. East inspection midpoint appears cooler/
purpler than same idle/endpoints: enlarge and review adjacent phases next.
Repair knee/tool-plane differences need full tool/task/owner-context review;
gait widths alone do not prove scale drift. All five guides/LFS updated. No source
art changes from this audit;helmet/cadence/room/scheduler remain unverified.

'''+old[at:]
        f.write_text(old,encoding='utf-8')
print(json.dumps(dict(rejectedUpperTrials=1,reviewedCardinalBoards=4,displayedSlots=64,selectedPhaseSlots=48,guides=5,lfsRasters=len(rasters),normalChanged=False,fullGoalComplete=False)))
