"""Record the bounded James controller milestone without replacing shared notes."""
import hashlib
import json
import os
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = Path(__file__).resolve().parent

def atomic(path, data):
    temp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    temp.write_bytes(data)
    os.replace(temp, path)

def write_json(path, data):
    atomic(path, (json.dumps(data, indent=2) + '\n').encode())

guards = {}
for lane in ['north', 'east', 'south', 'west', 'continue', 'safety', 'source_paths']:
    guard = json.loads((PACK / f'{lane}-validation.json').read_bytes())
    assert guard['exitCode'] == 0 and not guard['timedOut']
    assert guard['realProfileUnchanged'] and guard['profileDelta'] == []
    guards[lane] = guard

runtime = ['scripts/james_construction_motion.gd', 'scripts/branforth_npc.gd',
           'scripts/crew_construction.gd', 'scripts/grid_canvas.gd']
review = {
    'status': 'native_controller_verified_owner_review_pending',
    'runtimeInstalled': True, 'fullSetComplete': False,
    'newlyAuthoredDrawings': 0, 'newSourceStates': 0,
    'runtimeHashes': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in runtime},
    'native': {'checks': 6209, 'failures': 0, 'cases': 24,
               'repeatedPowerLossCases': 4, 'captures': 833,
               'scope': 'Four bare cardinal real paid construction jobs; draw/held/stow power and door holds; repeated power loss during held return. Frozen paid progress/contact, sparks off, normal completion once.'},
    'continue': {'checks': 1496, 'failures': 0, 'cases': 3, 'captures': 21,
                 'scope': 'Fresh disk Continue: North partial exit, East neutral hold, South partial return. Exact paused actor/source/playback/work/clock, no second charge, completion once. Not all facing/phase combinations.'},
    'safety': {'checks': 21, 'failures': 0,
               'scope': 'Real South partial retraction: removed order, death, critical flooding. Normal safety clears motion; death renderer pre-update cannot retain stale torch. Not all hazard/gear/path combinations.'},
    'sourcePaths': json.loads((PACK / 'source-paths-evidence.json').read_bytes()),
    'profileGuards': guards,
    'visualReview': 'All 833 source-change captures across 19 boards and all 21 fresh Continue views inspected. Matte selected sources, stable apparent proportions/height and fixed feet; whole-source tool retraction/return replaces instant idle snap. South hand occlusion corrected in fixture and recaptured. Native room lighting and thaw fog are separate from unchanged source pixels.',
    'previewTiming': 'Source-order GIFs use 50ms per captured pose; simplified pose sequence, not continuous real-time gameplay recording.',
    'remaining': 'Repair contacts, wider family/gear/furniture/rotation contexts, release gameplay and owner visual acceptance. Full James animation goal remains active.'
}
write_json(PACK / 'selection-review.json', review)

for relative in ['character/james-construction-interrupt-v1/selection-review.json',
                 'character/james-construction-controller-v2/selection-review.json',
                 'character/james-torch-material-residue-v2/selection.json']:
    path = ROOT / relative
    data = json.loads(path.read_bytes())
    data['runtimeMotionReview'] = 'res://character/james-construction-motion-v1/selection-review.json'
    data['constructionInterruptionDefect'] = 'Resolved by parameterized whole-source runtime retraction/return; 24 native cases and four repeated holds reviewed. Earlier staged 24 aliases remain uninstalled.'
    data['fullSetComplete'] = False
    write_json(path, data)

block = '''## James construction interruption motion — October 1, 2026

Installed whole-selected-source retraction/neutral hold/reversed return in
james_construction_motion.gd, James actor snapshot/rebuild hooks, optional
construction controller hook and eligible renderer override. No new drawings or
states; selected matte torch sources/rulers remain unchanged. Paid work/contact
freeze during tool motion; sparks stop; safety precedes motion. Door rebuild
clears actor state before ordinary construction: retain the visible source before
that reset, then allow normal claim/contact/safety validation to reestablish it.
Held work clock resumes its saved phase instead of advancing through the outage.

Four bare directions:6209checks/24 power/door cases plus four repeated return
interruptions/833source-change captures/0failures. Fresh Continue:1496checks,
North exit/East hold/South return,21views/0failures; exact paused source/playback,
paid progress and normal completion once. Safety:21checks for South cancellation,
death/flood, including immediate death renderer. Source paths:7602checks across
all348 source indices and real-save corruption admission; algebra proof, not
native gameplay at every entry index. All seven final engine intervals exit0,
no timeout/strict owner profile unchanged/scratch APPDATA.

All833views on19boards and21Continue views reviewed. South hand occlusion in
the initial fixture was corrected and recaptured; fixed per-job crop/scale.
Room power lighting and West thaw fog vary independently of immutable source
pixels. GIFs show source order at50ms/pose, not real-time footage. Prior failed
door/parse/occluded diagnostic runs retained, not acceptance evidence. Lesson:
inspect every captured source change, protect motion against pre-controller
navigation resets, and test Continue inside exit/hold/return rather than only
ordinary work. Earlier24candidate aliases remain staged/uninstalled.

Evidence/HANDOFF:character/james-construction-motion-v1. Owner visual acceptance,
repair contacts and broader family/gear/furniture/rotation/release polish remain.
Full James animation goal active/incomplete; coverage is not completion.

'''
guides = [ROOT / 'docs/CURRENT_STATUS.md', ROOT / 'docs/ASSET_PIPELINE_AND_WORKFLOW.md',
          ROOT / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
          ROOT / 'skills/brinespace-character-pipeline/references/crew-consistency.md',
          Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for i, path in enumerate(guides):
    original = path.read_bytes()
    if block.splitlines()[0].encode() in original:
        continue
    insert = block.encode()
    atomic(path, insert + original if i == 0 else original + b'\n' + insert.rstrip() + b'\n')

handoff = '''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James construction motion

## Objective and acceptance
Full James animation/master consistency and cross-family polish. Active and
incomplete; current interruption repair installed/native reviewed, owner pending.

## Accepted decisions and constraints
Matte selected whole poses,148 standing ruler/p92,172; planted work contact,
belt wrench, forward torch. Paid work survives power/door holds; sparks stop.
Construction effects target doorway by owner decision. Safety precedes motion.
Preserve concurrent actor work and owner profile; scratch native APPDATA only.

## Current state
New scripts/james_construction_motion.gd/.uid, James actor snapshot/rebuild,
crew_construction optional hook and grid_canvas eligible motion override.
Parameterized selected sources; no artwork or state additions. All current
proof fixtures/helpers paired UIDs. selection-review.json freezes runtime hashes,
counts/scopes/guards; parent selections/five guides updated. Previous finite
24candidate aliases remain uninstalled. Diagnostic archives retained.

## Verification
6209native checks/24cases+4repeat losses/833captures;1496Continue checks/3cases/
21captures;21safety checks;7602source-path checks/348entries; all0failures.
All7final native intervals exit0/no timeout/strict owner unchanged. All19boards/
833views and21Continue views inspected. Exact whole sources, paused state/clock,
fixed work/feet and completion once. North restored camera shifts242px without
body scaling. South initial hand-occluded run superseded by visible recapture.
Source-order GIF timing simplified50ms/pose; no continuous footage claim.
Scoped runtime diff whitespace check passed. Not all Continue direction/phase,
hazard/gear/path contexts, owner acceptance or release gameplay.

## Next action
Inspect actual repair contacts/forward torch against masters and normal effects,
then wider family/gear/furniture/rotation consistency and owner/export polish.
Do not treat coverage or bounded source checks as full-set completion.
'''
atomic(PACK / 'HANDOFF.md', handoff.encode())
print('Recorded controller milestone, three parent evidence links and five guides.')
