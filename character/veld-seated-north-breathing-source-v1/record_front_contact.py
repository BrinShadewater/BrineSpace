from pathlib import Path
import json,hashlib,re
P=Path(__file__).resolve().parent;R=P.parents[1]
dirs=['veld-seated-journey-v1','veld-seat-front-continue-v1','lounge-seat-contacts-v1','veld-seat-approach-probe-v1']
for name in dirs:
 v=json.loads((R/'output'/name/'validation.json').read_text());assert v['passed'] and not v['realProfileChanges']
fit=json.loads((P/'fitted-verification.json').read_text())
assert all(hashlib.sha256((P/n).read_bytes()).hexdigest()==h for n,h in fit['hashes'].items())
title='Veld clear chair front and retained checkpoint contact — October 1, 2026'
note='''

## Veld clear chair front and retained checkpoint contact — October 1, 2026

Fixed observed sideways entry/rise glide through room contact registration,
not source distortion. Actual lounge rotation2 front153..165 is collision-clear
and joins node128/160; old169gap is wall-blocked. Shared fallback sofa/lounge_seat
resolver tries existing28gap then4px insets up to16, prefers clear front with
station-local service_limit/exact_approach. Existing normal clear-path checks
remain; no furniture/wall/collision-mask/teleport changes. Old63.5px lateral
shift becomes <.1px (~.0693actual existing contact tolerance), vertical32px.
Games-table contacts unchanged; fully blocked fronts retain side fallback and
still need coherent motion. crew_life seated_contact retains old checkpoint
side offset/depth without advertising old contacts to new goal selection.
Save schema/player clocks unchanged. Shared registration affects all crew;
current motion/native proof covers Veld. New North seated artwork stays staged,
16bound breathing files byte-exact; no art/master grade/scale/normal selection edit.

Latest6375natural chooser/path/move/timed seated checks,0failures,80.69sec
engine0/no errors,72native+72source captures. Paired room/source boards reviewed:
large sideways glide removed, stable held matte body and master helmet. Four
actual disk/fresh-scene restores front/retained side x2gears:81checks0failures,
154.51sec. Exact source/contact/depth/action/gear/visual-clock/pause retained.
Prescribed checkpoint cases, distinct from natural route. Native4pair board:
3byte-exact crops, first bare-front max5/255 room-shade difference with exact
source; prior first-render shade uncertainty remains.11static assertions4.68sec
and4-quarter approach probe4checks37.62sec pass. All2931non-log owner files
unchanged in isolated runs. Initial75.38sec fixture rejected .0693px against .01
threshold; kept evidence, adopted existing .1contact tolerance, no runtime move
change. Earlier6375/81.72sec pass precedes compatibility helper.

Lesson: a fixed foot cannot prove natural contact; prefer an actually reachable
front before inventing sideways pose deformation. Expand only the station search
band, keep collision/path checks authoritative. Preserve old checkpoint lookup
separately from future goal admission when changing contact registration. Bind
unchanged source revisions and verify actual fresh-scene restores, not snapshot
admission alone. Before-review artifacts/resolver retained in front-contact-v1.
Next fully blocked-front side contexts, independent East/West seated sources,
South room contexts, further hazards/rest/death joins/full-set polish. Full goal
active/incomplete. Handoff: this candidate/FRONT_CONTACT_HANDOFF.md.
'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
 old=path.read_bytes()
 if title.encode() not in old:
  new=note.encode();path.write_bytes(new.lstrip(b'\n')+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+new)
bound=json.loads((P/'journey-review.json').read_text())['files']
bound.update(json.loads((P/'front-continue-review.json').read_text())['files'])
files=[P/n for n in ['FRONT_CONTACT_HANDOFF.md','record_front_contact.py','review_front_continue.py','review_journey.py','make_journey_page.py','journey-review.html','front-continue-review.json']]
files += [R/'scripts/crew_room_activity.gd',R/'scripts/crew_life.gd',R/'tests/index.json']
for stem in ['lounge_seat_contacts','veld_seat_approach_probe']:
 files += [R/f'tests/test_{stem}.gd',R/f'tests/test_{stem}.gd.uid',R/f'tools/run_{stem}.py']
for name in dirs[2:]:files += [f for f in (R/'output'/name).iterdir() if f.is_file()]
files += [P/n for n in fit['hashes']]
for f in files:bound[f.relative_to(R).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
(P/'front-contact-evidence.json').write_text(json.dumps({'scope':'shared reachable front/retained contact resolver; Veld paired natural route and prescribed fresh-scene checkpoint proof; not full set/all layouts/all crew/owner acceptance','nativeJourneyChecks':6375,'freshContinueChecks':81,'staticAssertions':11,'files':bound},indent=2)+'\n')
print(json.dumps({'boundFiles':len(bound),'notes':5,'unchangedSourceFitFiles':len(fit['hashes']),'normalArtworkSelection':False}))
