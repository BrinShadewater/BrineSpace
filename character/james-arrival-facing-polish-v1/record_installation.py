from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1]
def read(p):return json.loads(p.read_text())
for folder,name in [(P,'native-baseline'),(P,'native-installed'),(R/'character/james-seated-family-v1','native')]:
    v=read(folder/(name+'-validation.json'))
    assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'], (folder,name)
before=read(P/'baseline-evidence.json');after=read(P/'installed-evidence.json')
assert before['mismatches']==12 and before['failures']==0
assert after['mismatches']==0 and after['failures']==0 and len(after['results'])==16
assert sum(len(r['captures']) for r in after['results'])==72
source=R/'scripts/branforth_npc.gd'
assert 'timer = float(Life.STAGES.life_inspect) if movement_medium=="dry" else 1.02' in source.read_text()
(P/'selection.json').write_text(json.dumps(dict(status='installed_owner_review_pending',fullSetComplete=False,
    script='scripts/branforth_npc.gd',scriptSha256=hashlib.sha256(source.read_bytes()).hexdigest(),
    baselineChecks=67,baselineFacingMismatches=12,installedChecks=after['checks'],
    cases=16,captures=72,dryDiagnosticSeconds=6,wetDiagnosticSeconds=1.02,
    artChanged=False,scope=after['scope']),indent=2)+'\n')
def atomic(file,fn):
    before=file.read_bytes();after=fn(before)
    if before==after:return
    tmp=file.with_name(file.name+'.james.tmp');tmp.write_bytes(after)
    if file.read_bytes()!=before:tmp.unlink();raise RuntimeError('Concurrent edit '+str(file))
    tmp.replace(file)
note='''### James generic diagnostics arrival and complete tablet clock — September 30, 2026

Actual James move/arrive baseline showed12 wrong East facings in16 dry/flooded,
bare/helmet,4-direction generic maintenance-room approaches. The subclass's
curiosity fallback forced East after inherited arrival; furniture station branches
already return with their authored facing. Remove only the generic East override.
Same-direction water arrival now plays all6 swim-stop poses and exact tread0.

Inspect the actual activity timer as well as the selected manifest: generic dry
diagnostics still waited1.02s while every accepted directional tablet clip lasts
5.5s. Use the existing Life.STAGES.life_inspect6s dry window: complete cycle plus
0.5s neutral tail. Wet generic dwell remains1.02s; no new underwater tablet art.
No source pixels, equipment, clearance, room stations or save schema changed.

3793 actual normal-grid checks PASS:16 explicit collision-checked approaches,
all1130 dry tablet slots through NPC.update, complete six-second need relief,
pause/neutral tail and48 same-facing water-stop slots.72 native captures reviewed,
plus fixed82px source preview. Seated furniture regression:72 native lounge and
observation captures,N/S facing, no failures. Scratch owner profiles unchanged.
Not pathfinder-generated or exterior journeys, workstation-specific facing turns
or full-family acceptance. Keep those separate from this generic arrival repair.
See docs/JAMES_ARRIVAL_FACING_HANDOFF_2026-09-30.md. Goal active.
'''
headline='''## James diagnostics arrival continuity fixed — September 30, 2026

Generic diagnostics preserves the incoming facing instead of snapping East.
Dry tablet diagnostics now runs its complete5.5s cycle plus0.5s neutral; wet dwell
unchanged.3793 actual checks PASS across16 dry/flooded approaches, both modes;
72 native captures reviewed and seated furniture regression PASS. Scratch owner
profiles unchanged. No art changes. [Handoff](JAMES_ARRIVAL_FACING_HANDOFF_2026-09-30.md).
Full-set motion/proportion/journey polish continues; goal active.

'''
atomic(R/'docs/CURRENT_STATUS.md',lambda b:b if headline.encode() in b else headline.encode()+b)
for file in [R/'docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    atomic(file,lambda b:b if note.encode() in b else b+b'\n\n'+note.encode())
update=b'\n\nGeneric non-East diagnostics arrival and the complete dry tablet timer are now repaired. See JAMES_ARRIVAL_FACING_HANDOFF_2026-09-30.md. Workstation-specific facing changes and full travel handoffs remain open.\n'
atomic(R/'docs/JAMES_CONSISTENCY_HANDOFF_2026-09-30.md',lambda b:b if update in b else b+update)
handoff='''# Project handoff

Updated:2026-09-30 · Project:Brine Space · Task:James diagnostics arrival polish

## Objective and acceptance
Continue full James master matching and cross-family motion/handoff polish.
Installed controller correction; owner/full-set acceptance remains open.

## Accepted decisions and constraints
Directional diagnostics uses the accepted tablet facing James; wrench stays on
the belt. Furniture supplies its own facing. Dry animation gets a complete cycle,
wet generic dwell stays1.02s. Preserve source art, clearance and save schemas.
All native work uses scratch APPDATA and fingerprints the owner's real profile.

## Current state
scripts/branforth_npc.gd removes generic curiosity's forced East and gives dry
diagnostics the existing6s inspection window.5.5s accepted tablet cycle plus0.5s
neutral.16 actual-arrival fixture and normal-grid capture/review scripts in
character/james-arrival-facing-polish-v1. Source PNGs unchanged. Pipeline/bible/
continuation and canonical+installed skill lessons updated.

## Verification
Before:67 checks confirm12 wrong facings in16 generic dry/flooded approaches.
After:3793 checks,zero mismatches; all1130 dry tablet slots through actual
NPC.update, normal need relief at6s, pause/neutral tail and48 water-stop slots
ending on same-facing tread0.72 native captures visually reviewed;82px paired
source GIF reviewed at midpoint. Final seated regression72 native lounge/
observation captures,N/S facing,zero failures. Owner profiles unchanged each run.
Fixtures author collision-checked routes; not autonomous pathfinder/exterior,
workstation-specific rotations or all-room evidence.

## Next action
Review North ordinary water boot proportions and West water death limb length;
restore North sleep breathing. Prove workstation-specific facing transitions,
complete furniture/meal/equipment and exterior dispatch/airlock/cargo-return
journeys. Goal active. No processes remain after final PASS.
'''
file=R/'docs/JAMES_ARRIVAL_FACING_HANDOFF_2026-09-30.md'
if file.exists():atomic(file,lambda b:handoff.encode())
else:file.write_text(handoff)
print('Arrival polish recorded:3793 checks,16 cases,72 captures; no source art change; goal active')
