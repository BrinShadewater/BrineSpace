from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];S=R/'character/veld-sofa-partial-fall-south-v1'
path=S/'motion-review-evidence.json';d=json.loads(path.read_text(encoding='utf-8'))
for name,digest in d['bindings'].items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest,name
d['reviewedBoards']=d['boards'];d['reviewedNativePresentations']=1176
d['visualReview']='All24contact sheets/all1176chronological native presentations inspected. Paired sit/rise body/material/shared-shell/contact accepted for guarded normal integration. Browser APNG review page visible; one screenshot confirms native/source preview presentation. No claim that all24clips were continuously watched, natural whole-world cadence or owner final acceptance.'
path.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
block='''## Veld partial South sofa falls in normal verification — October 2, 2026

Normal grid loader/ACTIVE_ASSETS now selects paired six-state manifests at
character/veld-sofa-partial-fall-south-selected-v1. Same72staged authored source
slots/runtime metadata; name/descriptive status only differs.166selection checks
pass. All24motion contact sheets/all1176chronological native presentations reviewed:
body/material/shared-shell/contact accepted for guarded integration.24lossless
APNGs/2400decoded checks retain exact room colours. Browser review page visibly
loaded; not a claim all24clips continuously watched or owner final acceptance.

Previous candidate-world evidence retains scope:79775checks/24ordinary disk/fresh
restores/7200futureticks and5111checks/1176native30fpsframes, zero failures;
84inputs/2931owner non-log files unchanged during each scratch interval. Those
intervals used explicit candidate injection before this loader admission. New
normal-only24case world/Continue fixture is running; every fresh scene checks
all72normal source slots/metadata without any manifest injection. Normal gameplay
integration remains under verification. No source redraw/grade/scale change.

Lesson: normal selection is a separate evidence boundary from an injected source
audition. Preserve original source/native/movie/checkpoint evidence and test actual
normal bindings independently after adoption; never relabel old interval hashes
as tests of the new loader. Current default sit is North/readSouth; keep dormant
side candidates separate from reachable service contexts. Full directional source
polish, natural traffic/priority hazards/title/new-process and cross-family master
review remain open. Full goal active/incomplete. Next poll normal Continue, inspect
fresh native before/after and complete relevant normal regressions/remaining set.
Handoff:character/veld-sofa-partial-fall-south-selected-v1/HANDOFF.md. No commit/export.

'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
    old=path.read_text(encoding='utf-8')
    if block.splitlines()[0] not in old:path.write_text(block+old,encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Normal South partial falls

## Objective and acceptance
Full master-consistent Veld set followed by cross-family polish. This milestone
admits paired partial South sofa fall sources; full objective remains incomplete.

## Accepted decisions and constraints
Same canonical selected sit/rise entrances and authored ground/neutral fall
interiors/endpoints, H148/256x272/p128224, exact180msincoming. Actual partial timer
owns saved seat fraction; early0/1floorrelease340ms/later2–5release780ms.
No room/owner furniture/art/grade/scale changes. Both gear variants required.

## Current state
New normal bundle references exact existing72source slots/six states pergear.
scripts/grid_canvas.gd adds two whole literal loader calls; ACTIVE_ASSETS adds
paired action/equipmentAction override and bindings, other parsed entries retained.
Candidate bundle stays staged; normal selected descriptive status is pending
normal verification.166selection checks0fail. UID-paired normal fixture/runner:
tests/test_veld_sofa_partial_south_normal_continue.gd and
tools/run_veld_sofa_partial_south_normal_continue.py. No candidate injection.

## Verification
All24motion boards/1176chronological native presentations inspected, source/
material/shell/contact accepted for guarded integration; no continuously watched
all24clip or owner acceptance claim. Visible browser23 on motion-review.html,
marked deliverable; screenshot shows source/native APNG preview. Candidate native:
5111checks0fail/289.05s/1176captures;2400lossless decoded checks0fail.
Candidate ordinary world:79775checks0fail/24disk-fresh/7200futureticks/895.7s.
These old intervals injected candidate, not current normal loader. Each preserves
84inputs/2931owner files. Current normal-only interval live session54472, output
output/veld-sofa-partial-south-normal-continue-v1. Wrapper freezes86inputs
(confirm final report count); every fresh scene checks72normal pixels/markers.
All-source normal lifecycle/Continue/final native captures pending. No old test
hash promotion. Full natural scheduler/traffic/hazards/Title/new-process pending.

## Next action
Poll54472, no restart on timeout; inspect terminal report/owner/input hashes.
Do not edit frozen production/test/manifests during run. Build normal Continue
review from24records; inspect all24native before/after pairs. Update descriptive
normal status only after pass; preserve exact runtime state/source metadata.
Keep reader/bunk/North guards intact. Default seated contexts Northsit/Southread;
genericSouthlife/side branches are dormant current compatibility, no fabricated
furniture to install art. Earlier East/West/source breathing exists staged; new
competing East study retained separately. Remaining full-set/current natural
context/material/master polish and final owner motion review open. No commit/export.
''',encoding='utf-8')
print('All24motion boards reviewed; normal paired admission/verification milestone recorded')
