from pathlib import Path
import json,os,shutil,time,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
for filename in ['unload-extraction.json','family-registration.json','native-review-evidence.json']:
    p=P/filename;data=json.loads(p.read_text(encoding='utf-8'));data['visualReview']='Reviewed six whole authored sources,12paired exports/6helmet details, four chronological72source-native pair boards and browser helmet contact. Improved master identity/scale; case ground lock, terminal idle, continuous native/world/lifecycle acceptance remain.';p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
W=R/'character/veld-cargo-east-master-family-v1/veld-workshop-north-master-joins-v1-review/summary.json';data=json.loads(W.read_text(encoding='utf-8'));data['visualReview']={'reviewedPages':['staged-bare-2.png','staged-bare-3.png','staged-helmet-2.png','staged-helmet-3.png'],'sourceNativePairsReviewed':40,'fullNativeFrames':['staged-helmet-0464-native.png'],'observations':['Exact whole North held source matches turn endpoint.','New squat/release interiors maintain smaller head and original graphite/harness/canisters.','Terminal authored standing still changes body/grade when older selected idle appears.','Floor case retained within whole source, not independently owned; contact/occlusion continuity still pending.'],'scope':'Changed North and arrival/West context pose review only; first page unchanged sources reused from prior scoped review, not all316 captures or uninterrupted native motion.'};W.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
browser={'url':'http://127.0.0.1:8791/character/veld-cargo-north-master-family-v1/','contactScreenshot':'helmet-contact.jpg','contactPhase':3,'finiteCompletions':json.loads((P/'browser-review/samples.json').read_text(encoding='utf-8')),'scope':'One paused source contact pose visually inspected; four520ms finite browser source completions and completion JPEGs recorded. No uninterrupted/browser-native synchronized motion acceptance.'};(P/'browser-review/evidence.json').write_text(json.dumps(browser,indent=2)+'\n',encoding='utf-8')
block='''## Veld North master pickup/unload source and workshop review — October 2, 2026

New staged cargo-north-master-family-v1: six whole authored rear unloading poses
from original North identity and exact canonical held density reference. Built-in
imagegen c839a886-c68a-47aa-ad7d-2e494d651c50 raw2149x732/prompt/reference hashes
retained. Single standing148ruler .25517241379310346, boots floor662all6, head
proxies23/23/24/24/23/23 and0gutter edge pixels. Source/body/leg anatomy untouched
after extraction; no strips or per-pose scale. Fourteen old/new whole source/paired
contexts reviewed. New12exports alias exact canonical North held0, whole authored
interiors/final5; same West shared recipe/protected low prop region/alpha. Original
North shell33x35 at fixed scale/grade, no bun bulge. Pickup exact reverse; original
520msfinite metadata/whole res paths/H148/p128224.84build+87packagechecks0fail.

Standalone actual player453checks0/72native samples6.27s;44frozen inputs unchanged,
scratchAPPDATA/all2931owner files unchanged. Fourboards/72source-native pairs seen;
72decoded native viewer samples exact. Paused browser helmet contact reviewed,
4finite520ms completions recorded. Preview600ms repeats are separate from game
finite clocks. Actual default workshop/authoring coordinated subclass compared
normal vs staged North/East/West/masterturns:5055checks0,2102ticks316captures101.27s,
203targeted inputs stable/profile unchanged. Changed arrival/North contexts in
4boards40pairs plus full helmet squat scene seen. Both planted turn intervals
still0travel; North unload0 now exact whole turn endpoint.

Remaining: prop retained in whole source, no independent floor lock/ownership;
new terminal stand still mismatches older normal idle body/grade. First-step/stop,
continuous moving/contact/material polish, interruption/needs/safety/medium/gear/
death/fresh Continue and guarded runtime adoption remain. South/master cardinal
and furniture/full-library polish still in full goal, active/incomplete. No normal
selections/controller/room changes. Lesson: correct action interiors and master
turn aliases do not prove terminal idle identity or floor-prop lifecycle. Preserve
whole authored foreground/behind depth until independent prop evidence exists.
Handoff: character/veld-cargo-north-master-family-v1/HANDOFF.md.

'''
refs=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for p in refs:
    st=p.stat();tmp=p.with_name(p.name+'.veld-north.tmp')
    with tmp.open('wb') as dst,p.open('rb') as src:dst.write(block.encode());shutil.copyfileobj(src,dst,1024*1024)
    now=p.stat();assert (now.st_size,now.st_mtime_ns)==(st.st_size,st.st_mtime_ns),str(p)
    for attempt in range(5):
        try:os.replace(tmp,p);break
        except PermissionError:
            if attempt==4:raise
            time.sleep(.2)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Veld North master cargo

## Objective and acceptance
Full master/style/perspective/proportion/grade-matched Veld set, then full library
consistency. Active/incomplete. North authored family is a scoped milestone.

## Accepted decisions and constraints
Original North master/compact canonical held endpoint; whole authored anatomy,
single standing ruler, grounded boots, fixed original matte shell. Scratch APPDATA;
preserve owner saves, concurrent work and normal selections.

## Current state
New cargo-north-master-family-v1 raw/prompt/reference/execution and extraction,
build/package verifier, paired manifests12frames/4finite APNGs, browsercontrols,
nativeboards/viewers/evidence. Two new tests+UIDs and runners for standalone
actions and actual prescribed workshop stage/route via existing authoring-only
coordinated Veld subclass. World review folder remains under East family.
No normal controller or art selection changes.

## Verification
84build/87package0fail. Standalone453checks0/72native samples6.27s,44inputs stable;
all72pairs visually seen. World5055checks0/2102ticks316captures101.27s,203inputs
stable;4boards40pairs +full helmet squat reviewed, not all316/fullcontinuous motion.
Bothturns physically planted. Both runs scratchAPPDATA/2931owner files unchanged.
Browserhelmetcontact seen and4finite520ms completions recorded. Nativeviewer72
decoded snapshots exact,600ms previewreset distinct from520finite authored action.

## Next action
Fix terminal North idle join against actual original master, preserving proper
floor-case occlusion/independent prop lifecycle (case currently within whole source,
not independently locked). Do not paste body strips or make an idle carry a moving
floor prop. Inspect contact/release in full motion; single grade recipe remains
subject to material polish. Whole first-step/stop still needed; coordinated preview
arrival hold skips ordinary update and is not safety/checkpoint compatible.
Then guarded controller lifecycle across service loss/needs/fire/flood/medium/gear/
death and fresh Continue before normal adoption. South/cardinal master actions,
remaining furniture/swimming contexts and full-library consistency remain.
''',encoding='utf-8')
old=R/'character/veld-cargo-east-master-family-v1/WORKSHOP_JOIN_HANDOFF.md'
with old.open('ab') as f:f.write(b'\nNorth action milestone now exists: see character/veld-cargo-north-master-family-v1/HANDOFF.md. Terminal idle/prop lifecycle and true first-step/stop remain.\n')
print('Recorded North source/player/world/browser milestone and updated five maintained references; full goal active.')
