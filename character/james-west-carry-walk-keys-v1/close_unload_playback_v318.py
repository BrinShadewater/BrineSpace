from pathlib import Path
import json,hashlib,re,base64,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'north-unload-rise-between-v317';q=p/'north-unload-playback-review-v318';q.mkdir(exist_ok=True);sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();inputs=json.loads((o/'playback-inputs.json').read_bytes());assert all(sha(r/f)==h for f,h in inputs['sources'].items());assert sha(o/'playback-review.html')==inputs['htmlSha256'];html=(o/'playback-review.html').read_text(encoding='utf-8');images=re.findall(r'data:image/png;base64,([A-Za-z0-9+/=]+)',html);m=json.loads((o/'bare-review-manifest.json').read_bytes());paths=[f[6:] for s in m['states'][:2] for f in s['frameFiles']];assert len(images)==len(paths)==13
for image,path in zip(images,paths):assert base64.b64decode(image)==(r/path).read_bytes()
assert sum(inputs['originalClocks'])==sum(inputs['candidateClocks'])==520;obs=json.loads((o/'browser-observations-v318.json').read_bytes());slow=[x for x in obs['observations'] if x.get('speed')==.125 and x['screenshot'].startswith('browser-phase-')];assert len(slow)==7
for i,x in enumerate(slow):assert f'candidate {i}/6' in x['statusBeforeScreenshot'] and f'candidate {i}/6' in x['statusAfterScreenshot'] and (o/x['screenshot']).exists()
assert obs['observations'][-1]['terminal']=='519 ms · original 5/5 · candidate 6/6 · paused'
report=dict(disposition='observed_browser_source_playback_samples',tabId='3',serverSessionId=51553,sourceVersion=317,htmlEmbeddedSourcesExact=13,slowAdvancingPhasesReviewed=7,normalSpeedScreenshotsReviewed=3,finiteEndpointReviewed=True,normalChanged=False,selected=False,sourceAcceptance=False,fullGoalComplete=False,findings=['Live eighth-speed advancing playback: seven candidate slots each observed/screenshot reviewed; original and candidate clocks mapped independently. Normal-speed three samples capture actual phases1,4,6; requested0/3 wait-to-capture races preserved. Finite replay visibly ends519ms original5/candidate6 paused.', 'Added rise drawing is visibly present, but broad bent body changes abruptly toward slimmer source317/standing endpoint. Head/backpack/hardware/fabric identity and exposure change around4to5; prioritize proportion/material continuity repair before acceptance or helmet propagation.', 'Initial sole225 vs224, lower phase knee/boot spread, case/idle disposition and21+9px unequal rise spacing remain. Browser samples are not every displayed refresh continuously watched or actual Godot arrival-controller gameplay.', 'No new source generation/native run/normal selection. Previous31769checks0 applies unchanged bank; all-family/master/helmet/carry-to-turn/controller/lifecycle/full-set polish remain.'])
(q/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');ledger=p/'material-repair-progress.json';before=ledger.read_bytes();d=json.loads(before);d['northUnloadPlaybackReview']=dict(version=318,file=(q/'review.json').relative_to(r).as_posix(),sourceVersion=317,slowAdvancingPhases=7,selected=False,sourceAcceptance=False,normalChanged=False);d['nextVisualRepair']='Observed317 playback318 exposes broad bent body/head/backpack/detail change to slimmer317/endpoint at4to5; repair proportions/material continuity before helmet propagation. Then phase support/case/idle disposition and rise spacing, carry-turn/actual arrival/controller/lifecycle/normal adoption and whole-family polish.';assert ledger.read_bytes()==before;ledger.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
section='''### James unloading advancing playback comparison - October3,2026

V318 observed current317 source playback in local browser tab3/8878. Self-contained
HTML13embedded source slots verified exact; original6/candidate7 use independent
520ms clock maps. Eighth-speed advancing samples capture all7candidate phases,
each visible status before/after screenshot agrees; all screenshots viewed.
Normal-speed samples actually show1/4/6 despite0/3/6 requested waits; capture
races preserved rather than relabelled. Finite replay visibly ends519ms paused on
original5/candidate6. No every-refresh continuous observation or actual native
arrival-controller acceptance. No source generation, repeated native test or normal
selection.317 bank unchanged; prior69native checks retain only their original scope.

Visual finding: additional rise is present, but broad bent body/head/backpack/gear
and fabric differ from slimmer317/standing endpoint at4to5. Prioritize this join's
master proportions/material before helmet propagation. Initial1pxsole, lower
knee/boot drift, floor-case/idle disposition and uneven21+9rise remain. Full goal
active/incomplete. Lesson: compare unequal-count clips by elapsed clock; save UI
capture races and distinguish sampled advancing playback from gameplay cadence.
Handoff: character/james-west-carry-walk-keys-v1/north-unload-playback-review-v318/HANDOFF.md.
'''
guides=record_guides(r,section,'### James additional unloading rise pose')
(q/'HANDOFF.md').write_text('''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: James playback assessment

## Objective/decisions
Complete master-matched full James set, actual integration and all-family polish.
Versioned candidates; matte master identity/proportions/support, wrench on belt.

## Changed files/current state
317 playback HTML/input hashes and13exact embedded source slots, saved browser
observations/screenshots;318 review/HANDOFF. New builder318, ledger and five guides.
Bank/art/normal runtime unchanged. Live server session51553 at8878, browser tab3
marked deliverable this turn; revalidate live handles if continuing later.

## Evidence/limits
All7eighth-speed candidate phases sampled during actual advancing browser playback,
all screenshots viewed. Three normal-speed actual screenshot phases1/4/6; wait
races retained. Finite replay visibly519ms original5/candidate6 paused.13embeds
exact/clocks520ms verified. Not continuously watched every refresh or actual Godot
controller motion. No new generation/native run; prior31769checks0 scope retained.
Broad bent body/head/backpack/detail changes to slimmer317/endpoint at4to5 remain.

## Next work
Repair master proportion/material/head/gear join before shared helmet propagation.
Then sole/knee support, uneven rise/case-to-idle disposition, latest carry-turn and
actual arrival selector, normal lifecycle/checkpoint/Continue/interruptions and
all-family polish. Full goal active, no external blocker.
''',encoding='utf-8')
with(p/'HANDOFF.md').open('a',encoding='utf-8') as stream:stream.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for f in o.glob('browser-*.png')];attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3));print(json.dumps(dict(embeddedExact=13,slowPhasesReviewed=7,normalScreenshotsReviewed=3,finiteEnd=True,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
