from pathlib import Path
P=Path(__file__).resolve().parents[2]
entry='''## James ordinary directional lying staged - 2026-09-30

Four independent bare sources packaged into lie-down/sleep/get-up:12 states/72 refs.
Fixed anatomical scales, exact selected standing arrivals, shared sleeping neutral,
reverse rises and retained depth/timings. South/north boot corrections selected;
north sleep uses quiet neutral after generated breathing stretched calves.
456 packaging and409 native loader/clock checks PASS; scratch profile unchanged.
Helmet pairing, continuous motion and actual ordinary-bed contact remain pending.
Current hab selects the separately installed east bunk; the attempted ordinary-north
room probe is preserved as failed evidence, not acceptance. Runtime bindings unchanged;
80 retained bare states remain. See docs/JAMES_LYING_HANDOFF_2026-09-30.md.

'''
lesson='''

### James ordinary lying source ownership - 2026-09-30

Use a single anatomical scale measured from each source's standing pose; reclining
and foreshortened silhouettes should not be resized to standing bounding height.
Protect the actual head region even when boots/knees become the upper silhouette.
Orthographic sole-facing boots should retain anatomical width; reduce source
perspective inflation through an authored correction, never per-frame scale.
Reject sleep breathing that stretches calves or moves resting contacts: a repeated
authored neutral is a transparent temporary selection, not proof of breathing polish.
Current crew-hab layouts can select the separate east bunk instead of ordinary
lying; verify the actual selected station before asserting north/pillow contact.
Staged native loader/clock success does not establish real furniture contact.
Evidence: docs/JAMES_LYING_HANDOFF_2026-09-30.md.
'''
def atomic(path,transform):
 before=path.read_bytes();after=transform(before);tmp=path.with_name(path.name+'.james.tmp');tmp.write_bytes(after)
 if path.read_bytes()!=before:tmp.unlink();raise RuntimeError('Concurrent update: '+str(path))
 tmp.replace(path)
status=P/'docs/CURRENT_STATUS.md'
if b'## James ordinary directional lying staged - 2026-09-30' not in status.read_bytes():atomic(status,lambda b:entry.encode()+b)
for rel in ['docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 path=P/rel
 if b'### James ordinary lying source ownership - 2026-09-30' not in path.read_bytes():atomic(path,lambda b:b+lesson.encode())
path=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
if b'### James ordinary lying source ownership - 2026-09-30' not in path.read_bytes():atomic(path,lambda b:b+lesson.encode())
print('James staged milestone and pipeline/bible/skill lessons recorded')
