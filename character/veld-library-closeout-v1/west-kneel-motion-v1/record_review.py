from pathlib import Path
import json,uuid,shutil,time
P=Path(__file__).resolve().parent;R=P.parents[2]
title='## Veld original West lowering source staged — October 3, 2026'
note=title+"""

Registered one authored West kneel key at west-kneel-anchor-v3 using one fixed
integer translation18right5down; retained-window RGBA exact, no visible clipping,
colour/anatomy/rescale edits. Master-repair guidance permits registering authored
cells by the same planted boot. This corrects earlier overly broad prohibition:
fixed whole-key authoring registration is distinct from per-frame generated clip
recentring/reflooring, which remains disallowed. Key head27/floor223 matches the
original ruler. Guided keyv2 remains rejected for head24/shrunken upper body.
Key3buildchecks and28native checks pass;2native presentations per three scales.

One direct Hailuo02 lowering-only job448684324352355 succeeded;6s/768/24fps,
estimated USD0.28, billing unverified. Exact two input plates/prompt/task/full142
source retained under character/veld-library-closeout-v1/west-kneel-motion-v1.
Fixed whole768-to256 extraction, no pose/RGB correction. All142 raw/bare and helmet
poses inspected in chronology. Front visible ground silhouette x106..108 versus
initial107 improves substantially on prior samplev1 x75..108. This foreground-band
diagnostic is not separated-foot pressure/root/contact proof. Rear boot settles
below original223floor during hold (source floor222..229); head26..28 vs master27.
Whole pose preserves connected limbs, small face/brown hair/warm skin/charcoal
quilt more closely than selected old cool/soft sample interiors. No vial/rise.

Paired full142-slot lowering-source manifests preserve5917ms rounded24fps holds,
finite endpoint; no controller retiming/admission. Original rigid West helmet shell
tracks moving head; body outside region exact142/142.570APNG groupedpixel/hold
checks,1720final native checks/0failures;284native presentations at47/93/148px.
Native midlower/middlehold/terminal captures visually compared against original
standing and currentselectedkneel. State entry/finite endpoint/idle return/fresh
player snapshot continuation tested, not physical contact/fullcontroller/disk
Continue.914targetedinputs and2931ownerprofilefiles unchanged. First native interval
preserved in output/veld-west-kneel-motion-v1-first-timing: inherited40ms holds
corrected to unretimedsource before final validation. Selected West274PNGs and4
manifests match installed inventory; normal selection/controller unchanged.

Preview: character/veld-library-closeout-v1/west-kneel-motion-v1/index.html.
Next: resolve rearboot contact and derive an explicit1s lowering phase with truthful
endpoint/timing before matching sample/examination/rise and adjoining West cargo.
Whole Veld library remains incomplete; no new normal admission this interval.
Handoff: character/veld-library-closeout-v1/west-kneel-motion-v1/HANDOFF.md.

"""
(P/'HANDOFF.md').write_text("""# Project handoff

Updated: October 3, 2026 · Brine Space · Veld West lowering

## Objective and acceptance
Finish the Veld library against original masters. This interval produces a proportionally matched registered kneel key and complete lowering-only staged source. User visual acceptance of this new preview remains open.

## Accepted decisions and constraints
One fixed whole-key integer registration by the same planted boot is permitted by master-repair guidance; no anatomy/RGB/rescale edits or per-frame generated clip correction. Keep original small face, brown bun with intentional silver streak, warm skin, charcoal quilt and rigid original helmet. Preserve prior sources and installed approved turns.

## Current state
Key west-kneel-anchor-v3 reuses authored keyv1 with18right5down, head27/floor223, exact whole retained RGBA and no visible clipping. Guided keyv2 remains rejected. New source job448684324352355 has142slots/5917ms; estimated USD0.28, billing unverified. Whole lower ends on one knee, empty hands, no rise. Paired manifests/APNGs preserve all slots and source timing. Common256canvas/pivot128224/H148. Original shell tracks head; body outside region exact. No normal selection/controller changes.

## Verification
Key3build/28native checks with2three-scale presentations. Source142helmet bodychecks/570APNG/1720finalnative checks passed,284presentations at47/93/148px. All142raw/bare and142helmet chronology poses viewed; representative native41/70/141 viewed against original and selected. Entry/finite endpoint/idle return/fresh-player snapshot continuation pass.914targetedinputs and2931owner files unchanged. Selected West274PNGs/4manifests unchanged. First inherited40ms timing interval preserved separately; corrected fullsource5917ms validated. Evidence output/veld-west-kneel-motion-v1 and output/veld-west-kneel-anchor-v3. No fullcontroller/contact/disk Continue proof.

## Remaining work and next action
Front visible ground silhouette x106..108 vs107 improves on oldsamplev1 x75..108; not separated-foot pressure proof. Rearboot/floor222..229 vsoriginal223 requires contact review. Clip retains early standing hold, lower, extended settling hold; not the game's1s lower. Resolve contact and select a truthful1s lower phase with matching endpoint. Then sample/examination/rise and adjoiningcargo at same original stance before normal admission. Other directional materials/joins/furniture/water/death and full fresh-process Continue remain. Full library not finished.
""",encoding='utf-8')
K=P.parent/'west-kneel-anchor-v3'
(K/'HANDOFF.md').write_text('# Registered West kneel key handoff\n\nOne fixed whole authored key registered18right5down, preserving source density and retained RGBA exactly; no visible clipping. Head27/floor223 matches original. Original West shell and exact body outside its region.3build checks/28native checks pass,2native presentations at47/93/148px. No motion/contact/normal admission. Now used as frozen endpoint input by ../west-kneel-motion-v1; see its HANDOFF.md. Guided keyv2 remains rejected.\n',encoding='utf-8')
(P/'VERDICT.md').write_text('# Staged lowering-only source\n\nA substantial improvement in original-master appearance and front ground silhouette. Rearboot settling and1scontroller timing remain unresolved. All142slots preserved, no normal installation or sample/rise acceptance. See HANDOFF.md for evidence and next work.\n',encoding='utf-8')
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
parent=P.parent/'HANDOFF.md'
section='\n## Original West lowering source staged\nRegistered whole kneel key matches head27/floor223; fixed authoring registration, not per-frame clip repair. Complete lowering-only142slots5917ms per gear,1720native checks/284presentations pass. Front ground silhouette steadier; rearboot and1stiming remain open. No normal admission. See west-kneel-motion-v1/HANDOFF.md.\n'
text=parent.read_text(encoding='utf-8')
if '## Original West lowering source staged' not in text:parent.write_text(text+section,encoding='utf-8')
