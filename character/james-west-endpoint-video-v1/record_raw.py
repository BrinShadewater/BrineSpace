from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
def atomic(path,new):
    old=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(tmp,path)
inputs=json.loads((p/'inputs.json').read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs['preCallSha256'].items())
job=json.loads((p/'generation.json').read_bytes());assert job['status']=='Success' and job['task_id']=='448164031005009'
path=p/'raw-review/review.json';review=json.loads(path.read_bytes());assert review['decodedFrames']==142
review.update(visualReviewPending=False,sourceAcceptance=False,selected=False,
 finding='All six chronology boards/142 raw frames and two actual endpoint boards/nine whole+nine upper presentations inspected. First/last conditioning reaches the intended terminal pose, but path makes a full spin through North/East/South, lifting feet and changing body geometry. Purple case detail appears mid/late and disappears at final pose. REJECTED as bridge; no extraction, paired helmet/native expansion or installation.',
 next='One coherent head/collar/shoulder crop source study bound to exact upper endpoints at common80-square registration, retaining existing body/case motion. Compare every source frame and both whole composites; avoid a head-only splice or unreviewed timing change.')
atomic(path,(json.dumps(review,indent=2)+'\n').encode())
section='''### James exact-endpoint video terminal source review — October 2, 2026

Job448164031005009 completed Success, source.mp4 downloaded; no live generation
or native process.142decoded24fps768square frames inspected on all six chronology
boards plus nine whole/nine enlarged-upper endpoint/sample presentations. Supplied
first/last input conditioning reaches intended unloadWest0 terminal silhouette,
but path spins through North/East/South, lifts feet and changes body geometry;
purple case marks appear mid/late and disappear at finish. REJECTED before alpha
extraction, paired helmet, native playback or normal admission. Input/helper/test
hashes unchanged; estimatedUSD0.28, billing unverified. No owner-profile access.

Helper endpoint option remains available after six offline checks; source failure
is not a payload or clock failure. Exact terminal pose does not establish correct
motion path. Normal cap/V9/riseV6/caseV7 unchanged; full James goal incomplete.
Next one coherent HEAD/COLLAR/SHOULDER crop source study using actual paired upper
endpoints at common80-square registration; preserve original lower-body/case motion.
It must articulate neck and shoulder together, not paste a detached head. Check
all raw crop frames and BOTH whole composites before helmet/native work. No repeated
whole-body spin prompt trial. Five guides and direct-video skill mirrors updated.
Evidence:character/james-west-endpoint-video-v1/raw-review/review.json,HANDOFF.md.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James exact endpoint-conditioned video submission');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    atomic(path,new)
lesson='''
First/last source conditioning is not motion-path control: James exact-endpoint
job448164031005009 reaches the requested finish yet spins through all cardinals,
lifts feet and invents case marks. All142raw frames inspected; rejected before
extraction/native admission. Keep exact input conditioning and all-frame review
as separate gates. A localized upper-body source trial must retain collar/shoulder
articulation and be reviewed in full-body context, not merely as an isolated head.
'''
for path in [r/'skills/brinespace-character-pipeline/references/direct-video.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/direct-video.md')]:
    old=path.read_bytes()
    if b'job448164031005009 reaches' not in old:atomic(path,old+lesson.encode())
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James endpoint source review

## Objective and acceptance
Full James master/style/camera/size/height/proportion/matte set, then cross-family
polish. Incomplete. Both source endpoints AND intermediate motion must match.

## Accepted decisions and constraints
Normal cap/V9/riseV6/caseV7 still selected. Reserved transfer untouched. Source
success/endpoint reach and tested helper do not certify animation acceptance.

## Current state
Maintained tools/minimax_video.py optional --last-image/Hailuo02; Fast default
unchanged. Six offline tests pass. Old helper snapshot preserves prior V2 lineage.
Here equal1024first/last inputs,prompt,hashes,terminal ledger/source.mp4,142frame
chronology and nine whole/upper sample comparisons. Source REJECTED, not installed.
Five guides/direct-video mirrors updated; no native/profile/commit/export writes.

## Verification
All142raw frames and both endpoint boards inspected. Terminal pose reached, but
full spin/feet lifting/purple case detail fail path/art contract. Inputs/helper/
test hashes unchanged. EstimatedUSD0.28,billing unknown. Job448164031005009 Success;
review packaging session5624 exited0, no live job/process.

## Next action
One coherent head/collar/shoulder crop source trial between actual upper endpoints
with fixed80square registration, retained original lower-body/case motion. Review
all raw frames and both full-body composites; no head-only splice or broad spin
retry. Then paired helmet and both runtime lifecycles if source passes. Remaining
cardinals/contexts/full master/cross-family polish open. Goal active, no blocker.
''',encoding='utf-8')
print('142-frame exact-endpoint source rejected;hashes stable;terminal handoff/five guides/direct-video mirrors updated.')
