from pathlib import Path
import json, uuid, hashlib

P = Path(__file__).resolve().parent
R = P.parents[1]
for name, summary in [('native-connected', '40503 checks; 0 failures'),
                      ('native-dry-equipment', '29629 checks; 0 failures'),
                      ('native-routes', '13478 checks; 0 failures'),
                      ('test_owner_report_regressions', 'OWNER REPORT REGRESSIONS PASS')]:
    v = json.loads((P / (name + '-validation.json')).read_text())
    log = (P / (name + '.log')).read_text()
    assert v['exitCode'] == 0 and not v['timedOut'] and v['realProfileUnchanged']
    assert 'SCRIPT ERROR:' not in log and '\nERROR:' not in log and summary in log
dry = json.loads((P / 'dry-equipment-evidence.json').read_text())['results']
wet = json.loads((P / 'route-evidence.json').read_text())['results']
connected = json.loads((P / 'connected-evidence.json').read_text())['results']
for variant in ['baseline', 'installed']:
    assert sum(x['service'] for x in dry if x['variant'] == variant) == 96
assert sum(x['facingSnap'] for x in dry if x['variant'] == 'baseline') == 76
assert not any(x['facingSnap'] for x in dry if x['variant'] == 'installed')
wb = [x for x in wet if x['variant'] == 'baseline' and x['service']]
wa = [x for x in wet if x['variant'] == 'installed' and x['service']]
assert len(wb) == 50 and sum(x['arrivalBodyClear'] for x in wb) == 46
assert len(wa) == 46 and all(x['arrivalBodyClear'] for x in wa)
assert sum(x['stopSlots'] for x in wa) == 276
assert all(not x['facingSnap'] for x in wa)
assert sum(x['service'] for x in connected if x['variant'] == 'installed' and x['medium'] == 'dry') == 32
assert not any(x['facingSnap'] for x in connected if x['variant'] == 'installed')
assert sum(x['service'] and not x['arrivalBodyClear'] for x in connected if x['variant'] == 'baseline' and x['medium'] != 'dry') == 4

def atomic(path, transform):
    before = path.read_bytes() if path.exists() else b''
    after = transform(before)
    if after == before:
        return
    tmp = path.with_name(path.name + '.james-' + uuid.uuid4().hex + '.tmp')
    tmp.write_bytes(after)
    if (path.read_bytes() if path.exists() else b'') != before:
        tmp.unlink()
        raise RuntimeError('Concurrent edit: ' + str(path))
    tmp.replace(path)

selection = json.loads((P / 'selection.json').read_text())
selection.update(status='installed_dry_and_wet_safe_equipment_arrivals',
    dryCases=192, dryServices=96, dryBaselineFacingSnaps=76, dryInstalledFacingSnaps=0,
    connectedCases=128, connectedDryServices=32, connectedChecks=40503,
    dryChecks=29629, checks=13478, baselineServices=50, baselineSafeServices=46,
    installedServices=46, baselineFacingSnaps=42, installedFacingSnaps=0,
    lostServiceCases=4, lostSafeServiceCases=0, unsafeLifeSupportContactsRejected=4,
    stopServices=46, stopSlots=276, fullSetComplete=False,
    baselineProfileSha256=hashlib.sha256((R / 'character/chief-engineer-branforth-v2/clearance.json').read_bytes()).hexdigest(),
    pending=['Safe flooded life-support work contact/pose remains unresolved; current routes reject colliding front contacts',
             'Full furniture/meal/equipment/exterior journeys and owner visual acceptance',
             'Nonblocking East maintenance prop overlaps during complete journey review'])
atomic(P / 'selection.json', lambda _: (json.dumps(selection, indent=2) + '\n').encode())

note = '''### James dry workstation approaches and corrected counterfactual - September 30, 2026

James station-facing hook now also applies on dry equipment routes. Non-exact
destinations use facing-aware graph search on dry links. Exact console contacts
constrain the final contact segment, not the preceding grid-node heading; preserve
the route headings through smoothing. Check the actual incoming/outgoing contact
segment against the existing travel envelope. Do not force a grid node to face
north when the short console segment must subsequently turn north. Initial over-
constraint lost32 dry services; retained failure, corrected endpoint semantics.

Corrected192 dry cases:29,629 clean checks PASS, all96 services retained;76 arrival
facing snaps become0. Connected five-room128 cases:40,503 clean checks PASS, all32
dry life-support approaches retained; every tablet slot in the two sampled console
cycles matches normal-selected pixels. Six native first/middle/final console views
reviewed at master density, both gear modes; no art/grade/clock changes.

Counterfactual subclass identity can fall through to Bill's lazy collision profile.
Explicitly preload James swim/tread/action profiles for BaselineJames; preserve prior
counterfactual files and supersede their comparison counts. Corrected wet192-case
test:13,478 clean checks PASS. Baseline reaches50 services;46 have a clear arrived
body,4 life-support arrivals face north inside blockers. Installed keeps all46 safe
services and276 stop slots, rejecting those4 colliding contacts. Do not describe
this as full wet service coverage or as retaining all50 activities. Connected wet
life support confirms the4 baseline collisions; all8 nearby nodes and9 front
offsets checked per gear at q0 reject the north swim envelope. Safe work contact or
pose remains unresolved; do not move owner furniture or shrink the diver to pass.

Owner-report controller regressions PASS; final native logs clean and real profiles
unchanged. Previous wet44-to46/no-loss and no-life-support-baseline claims are
superseded by the explicit James-profile comparison. Installed46 stop playback
evidence remains valid. Full furniture/meal/equipment/exterior journeys and owner
acceptance remain; full James goal active. Current recorder is record_dry_installation.py.

'''
for path in [R / 'docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md',
             R / 'docs/ASSET_PIPELINE_AND_WORKFLOW.md',
             R / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
             R / 'skills/brinespace-character-pipeline/references/crew-consistency.md',
             Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    atomic(path, lambda b: b if note.encode() in b else b + b'\n' + note.encode())

headline = '''## James dry equipment approach facing installed - September 30, 2026

All96 dry services retained;76 facing snaps become0. 29,629 dry and40,503 connected-
room checks PASS; console tablet/native views reviewed. Corrected James-profile
wet comparison:13,478 checks PASS, all46 safe services and276 stop slots retained;
four colliding life-support contacts rejected, safe flooded work pose still open.
Earlier wet comparison counts are superseded. Controller regressions PASS; profiles
unchanged. [Handoff](JAMES_WORKSTATION_ARRIVAL_HANDOFF_2026-09-30.md). Full goal active.

'''
atomic(R / 'docs/CURRENT_STATUS.md', lambda b: b if headline.encode() in b else headline.encode() + b)
handoff = '''# Project handoff

Updated:2026-09-30 · Project:Brine Space · Task:James equipment arrival continuity

## Objective and acceptance
Full James animation/master consistency and complete cross-family journeys.
Dry/wet safe equipment facing and selected stops installed; full goal active.

## Accepted decisions and constraints
Master density/material and full body/turn clearance govern. Preserve owner layouts,
other actors, override interfaces and concurrent changes. No clip-forcing or body
shrinking. Tests do not establish full owner or release acceptance.

## Current state
bill_npc.gd supports desired heading in dry graph search too; exact contacts govern
the final appended segment and its body/turn clearance. branforth_npc.gd enables
equipment-facing hook on dry approaches. Previous selected start/stop metadata and
grid clearance retained. No art, grade, clock or save changes. Fixtures/selection
and record_dry_installation.py in character/james-workstation-arrival-polish-v1.
Historical recorders must not be rerun. Pipeline/bible/status/both skills updated.

## Verification
29,629 checks/192 dry cases PASS:96 services retained,76 facing snaps become0.
40,503 checks/128 connected cases PASS:32 dry console approaches and selected tablet
slots; six native console views reviewed. Counterfactual now explicitly uses James
clearance profiles, not inherited script-filename fallback to Bill. Earlier paired
comparison counts superseded; prior files and failed over-constraint retained.
13,478 checks/192 wet cases PASS:50 baseline services,46 clear arrived bodies and4
life-support collisions. Installed retains46 safe services and276 stop slots,
rejects4 collisions. q0 front-contact scan:8 graph nodes and9 offsets per gear have
no clear north swim pose. No full flooded console coverage claimed. Owner-report
regressions PASS, final logs clean and real profiles unchanged; no process running.

## Next action
Resolve a safe flooded life-support contact/work pose without altering owner layouts
or hiding collisions. Then complete autonomous furniture/meal/equipment/exterior
journeys and cross-family motion/material review. Keep the entire goal intact;
colliding baseline arrivals are not accepted successful services.
'''
atomic(R / 'docs/JAMES_WORKSTATION_ARRIVAL_HANDOFF_2026-09-30.md', lambda _: handoff.encode())
print('Recorded dry equipment facing and corrected James-profile wet comparison; full goal active.')
