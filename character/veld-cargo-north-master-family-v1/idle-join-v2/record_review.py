from pathlib import Path
import json, os, shutil, time

P = Path(__file__).resolve().parent
R = P.parents[2]
W = R / 'output/veld-workshop-north-idle-join-v4'
world = json.loads((W / 'validation.json').read_text(encoding='utf-8'))
assert world['passed']
journeys = json.loads((W / 'journeys.json').read_text(encoding='utf-8'))
native = json.loads((P / 'native-review-evidence.json').read_text(encoding='utf-8'))
native['visualReview'] = 'Four chronological boards, all72 source/native pairs reviewed. Original master terminal has different stance/detail from generated rise; contact/material/full cadence polish remains.'
(P / 'native-review-evidence.json').write_text(json.dumps(native, indent=2)+'\n', encoding='utf-8')
evidence = {'worldValidation':world, 'checks':journeys['checks'], 'failures':journeys['failures'], 'visualReview':{'boards':['bare-world-endpoint-departure-review.png','helmet-world-endpoint-departure-review.png'], 'captureInterval':'v3 retained despite six wrong actor-kind assertions; same artwork/renderer as v4', 'views':14, 'observations':['Original whole master terminal and static idle exactly match.', 'Case visibly remains at release location as actor departs8/24/48world units.', 'Final rise/stance/material and first walking step remain polish.']}, 'scope':'Fixture independent prop and static idle endpoint only; no production ownership, checkpoint, interruptions, full idle breathing or normal adoption.'}
(P / 'world-review-evidence.json').write_text(json.dumps(evidence, indent=2)+'\n', encoding='utf-8')
block = f'''## Veld North original-master idle and independent floor-case study — October 2, 2026

Staged cargo-north-master-family-v1/idle-join-v2 replaces final North standing
with whole original rear master at one148 ruler and shared material recipe;
unchanged original33x35 shell. First5 action frames exact parent reuse, pickup
reverse, finite520ms. Body-only005 is exact static idle alias; not full breathing.
Builtin authored graphite case33x24, fixed112193, independently behind boots.
65build checks0. Standalone457checks0/72native samples6.29s;45inputs stable,
all72pairs in4boards reviewed. Browser4finite completions and helmet endpoint seen.
Actual workshop current renderer fixture: {journeys['checks']}checks0 failures,
{world['seconds']}s;{world['targetedInputCount']}inputs unchanged, scratchAPPDATA/
2931owner files unchanged. Case fixed through actual8/24/48world-unit departure
both gears, prop/actual crew slots retained. Fourterminal/contact plus3departure
views per gear reviewed from retained v3 interval; same artwork/renderer as v4.
Failed v2 missing current bind_room interface and v3 six actor-kind oracle errors
retained with exact fixture/wrapper/runner sources. Fixture now extends current
James workshop renderer, own Veld prop fields, no normal renderer/controller edits.

Remaining: rise-to-master stance/material contact, full idle motion, first-step/
stop, independent case pickup/ownership/lifetime/checkpoint and guarded controller
needs/safety/medium/gear/death/Continue. South/master cardinal/furniture/swimming
and cross-library polish remain. Static endpoint/fixture prop does not complete
the full animation goal, which stays active. Lesson: inspect current room renderer
interface and actual crew slot kind; a fixed source prop cannot prove lifecycle.
Handoff: character/veld-cargo-north-master-family-v1/idle-join-v2/HANDOFF.md.

'''
refs = [R/'docs/CURRENT_STATUS.md', R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md', R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md', R/'skills/brinespace-character-pipeline/references/crew-life.md', Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for p in refs:
    st=p.stat(); tmp=p.with_name(p.name+'.veld-idle-join.tmp')
    with tmp.open('wb') as dst,p.open('rb') as src:
        dst.write(block.encode('utf-8'));shutil.copyfileobj(src,dst,1024*1024)
    now=p.stat();assert (now.st_size,now.st_mtime_ns)==(st.st_size,st.st_mtime_ns)
    for attempt in range(5):
        try:os.replace(tmp,p);break
        except PermissionError:
            if attempt==4:raise
            time.sleep(.2)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Veld North master idle join

## Objective and acceptance
Full Veld master-matched animation set and cross-library polish; active/incomplete.

## Accepted decisions and constraints
Whole original master standing body, shared recipe, unchanged rigid shell. Separate
authored floor prop; source interiors unmodified. Scratch APPDATA, preserve owner
saves/concurrent work/normal selections. Static endpoint is not full idle animation.

## Current state
This folder retains master extraction, two case generation candidates/provenance,
build and paired manifests/frames/APNGs, native/browser/world review and evidence.
Two tests+UIDs/two runners stage sources and own prop in current workshop wrapper.
No normal selection/controller/room changes.

## Verification
65build0;457standalone0/72samples/all pairs seen; world v4 validation and journeys
are authoritative. v2/v3 failures and exact harness sources retained. Actual case
stays fixed while Veld departs8/24/48world units.14world views and browser endpoint
seen; not uninterrupted native cadence or production lifecycle acceptance.

## Next action
Whole authored rise-to-master and genuine first-step/stop; full North idle motion.
Then pickup/contact/independent prop lifecycle and guarded controller safety and
Continue before normal adoption. South/cardinal/furniture/swimming and full-library
consistency remain. Arrival hold still skips ordinary update in authoring subclass.
''',encoding='utf-8')
print('Recorded scoped review, handoff and five maintained references; full goal remains active.')
