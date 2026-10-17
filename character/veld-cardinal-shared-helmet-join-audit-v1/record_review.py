from pathlib import Path
import hashlib,json,os,shutil,time
P=Path(__file__).resolve().parent; R=P.parents[1]
p=P/'audit.json';d=json.loads(p.read_text())
for ref,digest in d['bindings'].items():
    f=R/(ref[6:] if ref.startswith('res://') else ref)
    assert hashlib.sha256(f.read_bytes()).hexdigest()==digest,ref
d['visualReview']={'date':'2026-10-02','boards':['north-cardinal-joins.png','east-cardinal-joins.png','south-cardinal-joins.png','west-cardinal-joins.png'],'findings':['All four helmet turn endpoints differ from held equipment, bounded to the head region for North/East/West.','South corrected original-master body grade differs from the older shared-turn body; bare turn endpoint is not exact.','Start0 equals held case in all four directions and both gears.','Gait contact is a different support pose; raw pixel differences are not failures and need motion-relative review.'],'next':'Extend shared original helmet across cardinal action families, preserving one physical equipment ruler/collar contact. Repair South original-master grading across turn sources without per-frame normalization.','scope':'Source boards only; no new raster art, native/gameplay acceptance or owner acceptance.'}
p.write_text(json.dumps(d,indent=2)+'\n')
note='''## Veld cardinal equipment and grade joins isolated — October 2, 2026

character/veld-cardinal-shared-helmet-join-audit-v1 compares standing/unload-final,
held/pickup-final, start0, gait-contact0 and shared-quarter start for all four
directions/both gears. South uses corrected original-master idle/cargo/start/gait
family; others use staged master cargo/start/gait packages.40source size checks,
four paired boards inspected with enlarged fixed head/collar region. All input
bindings unchanged. Source-only evidence; no art edits or native acceptance.

All eight start0/held pairs exact. Bare turn/held exact North/East/West; South
differs by1945pixels due older turn grade vs corrected cargo grade. Helmet turn/
held differs in every cardinal; North1074/East1192/West1391pixels, all within
fixed head/collar region; South2743 includes body-grade difference. These are
comparison flags, not a shell-only measurement. Gait contact intentionally differs
in support pose; never infer failure from raw pixel difference across poses.
Visual review confirms remaining shared-equipment substitution at action/turn joins
and South face/body grade mismatch. Next extend whole shared helmet across cardinal
idle/cargo/start/gait families and reconcile original-master South turn grade.
Then complete remaining full-set states, normal lifecycle integration and polish.
Full Veld goal remains active/incomplete. No normal selectors or owner saves changed.
Handoff: character/veld-cardinal-shared-helmet-join-audit-v1/HANDOFF.md.

'''
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Veld cardinal joins

## Objective and acceptance
Full original-master-matched Veld animation library and cross-library polish.
This audit identifies the next defects; it does not close the full goal.

## Accepted decisions and constraints
Original authored masters govern grade/proportion. Reuse whole equipment sources
with one physical ruler and registered collar. Preserve existing staged evidence.
Raw pixel differences across intentionally different poses are not failure tests.

## Current state
build_audit.py generates four paired comparison boards and audit.json with source
bindings. record_review.py records actual board review and maintained lessons.
South uses original-master corrected cargo/start/gait, other directions staged
master families. Shared-turn package is the combined original-helmet quarters.

## Verification
40 canvas checks and all source bindings stable. All four boards visually reviewed.
Eight start0/held pairs exact. Bare turn endpoints exact N/E/W; South body grade
differs. All helmet turn endpoints differ from older action equipment, head-only
N/E/W; South adds body grading differences. Gait0 is not a held pose and requires
movement-relative review. No art changes, Godot run, controller or owner acceptance.

## Next action
Extend shared whole helmet to cardinal idle/cargo/start/gait families and preserve
exact held/start joins. Match South turn body grade to original-master family with
authored source fidelity, never independent per-frame grade corrections. Review
actual motion at native scale. Remaining full idle/furniture/swimming, natural
case lifecycle/controller/save/Continue and full-set polish remain active.
''')
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for target in targets:
    with target.open('rb') as src:
        if src.read(120).startswith(note[:100].encode()):continue
        src.seek(0);before=target.stat();temp=target.with_name(target.name+'.veld-join-audit.tmp')
        with temp.open('wb') as dst:
            dst.write(note.encode());shutil.copyfileobj(src,dst,1024*1024)
    for i in range(20):
        now=target.stat();assert (now.st_size,now.st_mtime_ns)==(before.st_size,before.st_mtime_ns),str(target)
        try:os.replace(temp,target);break
        except PermissionError:
            if i==19:raise
            time.sleep(.5)
print('Four-board findings saved; input bindings stable; five maintained references updated.')
