from pathlib import Path
import json,hashlib,uuid,shutil,time
P=Path(__file__).resolve().parent;R=P.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['INPUTS.json','SOURCE_REVIEW.json','FAMILY_REVIEW.json']:
 for f,h in json.loads((P/name).read_text()).get('bindings',{}).items():assert sha(R/f)==h,(name,f)
inv=json.loads((R/'character/veld-library-closeout-v1/installed/selected-library.json').read_text());refs=set();manifests=set()
for gear in ['bare','helmet']:
 for key in ['idle-west','walk-west','interact-west','kneel-west','repair-west','stand-west']:
  row=inv['resolved'][gear][key];refs.update(row['frameFiles']);manifests.add(row['manifest'])
for f in refs:assert sha(R/f)==inv['sourceBindings'][f]
for f in manifests:assert sha(R/f)==inv['bindings'][f]
for f in ['scripts/grid_canvas.gd','character/ACTIVE_ASSETS.json']:assert 'west-kneel-motion-v2' not in (R/f).read_text()
(P/'SELECTION_REVIEW.json').write_text(json.dumps(dict(unchangedWestSources=len(refs),unchangedWestManifests=len(manifests),failures=0,normalSelectionChanged=False),indent=2)+'\n')
assert json.loads((R/'output/veld-west-kneel-motion-v2/validation.json').read_text())['passed']
title='## Veld original West one-second kneel/rise staged — October 4, 2026'
note=title+"""

One scoped direct Hailuo02 boot-contact retry448693621641789 succeeded;
6s768P24fps, estimated USD0.28/billing unverified. Same frozen standing and
registered kneel plates. All142raw/native slots, exact prompt/input/task preserved
at character/veld-library-closeout-v1/west-kneel-motion-v2/. Whole fixed3:1
extraction; no per-frame placement, visibleRGB/anatomy or scale rescue.
All142bare whole poses and142helmet head/collar views visually inspected.

Correction to October3 summary: v1 floor229occurs during lowering, not held
kneeling (middle hold floor222..223). New explicit diagnostic in v1 keeps original
reports intact: rear toe dips6px below original223line; front sole lifts2px.
V2 removes below-line rear toe (whole floor220..223); front loweralpha220..223
still rises3px. Fixed foreground bands are not named-foot pressure/world-depth
proof. Body preserves original smallhead26..28vs27, warm skin/brown bun/matte
charcoal quilt. No vial/rise in raw source.

Staged lower selects every consecutive source14..70 (57poses/2375ms), uniformly
retimed1000ms at2.375x; derived rise reverses the same57whole poses/1000ms.
Complete142slot5917ms source remains visible and preserved; no movement pose
omitted, pixel interpolation or hidden bad-frame cut. Source's later settling hold
is not the selected endpoint. Original rigid West shell tracks head; body outside
region exact142/142. Common256canvas/pivot128224/H148. Preview includes600ms
review holds, not a sample action, controller or authored repeating game loop.

1480APNG groupedpixel/hold checks and3120nativeplayer checks pass;512native
presentations at47/93/148px. Advancing sampled player clock covers every source/
phase slot, exact source pixels and1s clocks; entry/finiteendpoint/idle-return/
freshplayer snapshot continuation pass. Not real-time60Hz coverage, NPCcontroller,
physical contact or disk Continue.914targetedinputs and2931owner profile files
unchanged. Selected West274PNGs/4manifests unchanged. No normal admission.

Review preview index.html here; handoff HANDOFF.md. Native representative lower
32and rise56visually reviewed; full native frames retained. Remaining: frontsole
contact and retimed motion quality, sample/examination and adjoining West cargo
joins before coherent admission. Do not issue uncontrolled repeated generations.
Full Veld library remains unfinished; no live job or approval gate.

"""
(P/'HANDOFF.md').write_text("""# Project handoff

Updated: October 4, 2026 · Brine Space · Veld West kneel/rise

## Objective and acceptance
Finish Veld against original masters. This interval stages a revised lowering source and1s lower/derived rise; visual/contact acceptance remains open.

## Accepted decisions and constraints
Same frozen original standing and whole once-registered kneel key. No local anatomy/RGB edits, per-frame translation/refloor or rescale. Original rigid West helmet shell; body outside its region exact. Preserve all source slots, previous candidates and normal selections.

## Current state
One MiniMax first/last job448693621641789, estimated USD0.28/billing unverified, succeeded. Complete142source/5917ms, fixed768to256 extraction. Lower uses all57source14..70poses uniformly retimed2375to1000ms (2.375x); rise reverses exact same poses. Later settling hold is not phase endpoint. Both gears/fullsource/manifests/APNGs and3200ms review cycle here.600ms holds are viewer holds, not sample handling. No normal installation or NPC changes.

## Verification
All142bare whole poses plus142helmet head/collar views reviewed; native representative lower32/rise56 at47/93/148 viewed.142exact bodyoutsidehelmet checks,1480APNG groupedpixel/hold checks,3120nativeplayer checks/512presentations pass. All source/phase sampled slots/pixels,1s phase clocks, finite endpoints, idle-return and freshplayer snapshot restore checked.914inputs and2931owner files unchanged.274selectedWestPNGs/4manifests unchanged. Native evidence output/veld-west-kneel-motion-v2. Not real-time60Hz coverage or actual NPC/controller/contact/disk Continue.

## Next action
Rear boot no longer dips below original223line; frontsole lifts up3px during source (wholefloor220..223). Contact and2.375xmotion quality remain open. Priorv1 toe6px dip occurred during lowering, not held kneel: new detailed diagnostic under v1 documents correction without erasing old evidence. Review motion, resolve remaining contact using coherent whole-source work before sample/examination and adjoiningcargo joins; avoid uncontrolled repeat jobs. Do not install this family in isolation. Full library unfinished.
""",encoding='utf-8')
(P/'VERDICT.md').write_text('# Staged West lower and derived rise\n\nRear toe no longer dips below original floor. Frontsole still lifts up3px; one-second retiming2.375x needs motion review.3120native player checks pass; no normal admission/contact/NPC/Continue acceptance. Exact source and all142frames retained. See HANDOFF.md.\n',encoding='utf-8')
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for path in paths:
 for attempt in range(20):
  with path.open('r',encoding='utf-8') as f:head=''.join(next(f,'') for _ in range(120))
  if title in head:break
  before=path.stat();tmp=path.with_name(path.name+'.veld-'+uuid.uuid4().hex+'.tmp')
  with tmp.open('wb') as dest,path.open('rb') as source:dest.write(note.encode('utf-8'));shutil.copyfileobj(source,dest,1024*1024)
  after=path.stat()
  if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):tmp.unlink();time.sleep(.5);continue
  try:tmp.replace(path)
  except PermissionError:tmp.unlink();time.sleep(.5);continue
  print(path.name,'updated');break
 else:raise RuntimeError('Concurrent update prevented prepend: '+str(path))
parent=P.parent/'HANDOFF.md';section='\n## Original West one-second kneel/rise staged — October4\nV2source removes rear toe below-floor dip; frontsole lifts3px. Full142source retained; every57movement pose14..70 retimed2.375xto1s, same exact reverse rise.3120nativeplayer checks/512presentations pass. No normal admission. Priorv1dip occurs during lower, not hold. See west-kneel-motion-v2/HANDOFF.md.\n'
text=parent.read_text(encoding='utf-8')
if '## Original West one-second kneel/rise staged' not in text:parent.write_text(text+section,encoding='utf-8')
print('Bound source inputs and selected West sources unchanged:',len(refs),len(manifests))
