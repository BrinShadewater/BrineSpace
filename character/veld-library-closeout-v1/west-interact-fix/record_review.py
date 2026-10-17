from pathlib import Path
import json,shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[2]
verdict=json.loads((P/'VERDICT.json').read_bytes())
assert len(verdict['measurements'])==12 and verdict['sourcePresentationsVerified']==250
title='## Veld West interaction repair rejected at source review — October 3, 2026'
note=title+'''

Continued the existing-library closeout using the original West master, selected
idle and old action poses as separate appearance, registration and motion inputs.
Existing master-based142-frame idle/scanner sources improve identity and helmet
joins but use a stance11native pixels to the right of selected idle/walk; no
normal admission of that pair without a coherent adjoining standing-family review.
Normal Veld curiosity arrival currently selects East scanner for1.02seconds;
West source-clock availability is not proof of normal West action dispatch.

Three built-in whole four-pose redraws preserved as raw images with exact prompts,
reference hashes and fixed equal2x2 extraction. V1 restores warmer skin/brown hair
and neutral suit detail but grows to160–162px/floor177–178 versus idle148/floor171.
V2, authored from repeated registered whole idle, remains153–154px/top16–17/floor169
with head/panel drift. V3 shrinks to139px and reflows the grid: top rowfloor164,
bottom rowfloor156. All rejected. No local anatomy, colour, pose-bound scaling,
recenter/refloor or rescue-crop corrections; no candidate runtime manifest.

All12 extracted candidates and complete comparison board inspected. Current
Veld loader order, relevant manifests and250 selected West source presentations
verified unchanged. No native tests warranted for rejected, unselected artwork;
no owner profile or controller changes. Installed turn body consistency fix remains.

Lesson: colour/detail improvements are insufficient when a sheet changes density,
head proportions or cell registration. Even explicit numerical placement and an
idle grid can reflow. Preserve failed sources and do not expand a failed key into
helmet variants or motion. Review idle/walk/action as one standing family before
admitting an otherwise improved source with a different stance axis.
West repair remains open; full Veld completion remains unverified and incomplete.
Handoff: character/veld-library-closeout-v1/west-interact-fix/HANDOFF.md.

'''
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 3, 2026 · Project: Brine Space · Task: West interaction closeout

## Objective and acceptance
Repair selected West interaction interiors against original identity and current idle joins. Complete Veld library remains incomplete.

## Accepted decisions and constraints
Finish existing library; whole poses, one registered ruler, no local anatomy/colour/rescale/recenter/refloor rescue. Preserve selected endpoints and840ms timing. Do not replace coherent existing work with an attractive but misregistered drawing.

## Current state
Three built-in four-pose raw redraws, exact prompts and all inputs saved here. All rejected; no runtime manifest, normal selection, controller or owner profile changes. Earlier12-state helmet turn body fix remains installed.
Existing original-based West142-frame idle/scanner pair is staged:11px axis difference from selected standing family prevents isolated admission. Current Veld curiosity arrive dispatch is East/1.02s; West source tests cannot prove automatic West dispatch.

## Verification
All12 extracted candidate poses and six-slot before/after comparisons inspected. V1H160–162/floor177–178; V2H153–154/top16–17/floor169; V3H139/floor164toprow156bottomrow. Selected idleH148/top24/floor171. V3 grid reflows. Exact source bindings and250 selected West source presentations plus loader order unchanged. No native tests run: source review rejected these candidates before admission.

## Next action
Resolve original-based West standing-family admission together (idle/walk/action registration and materials), or prove a single correctly registered whole interior pose before another sheet expansion. Do not repeat numerical sheet-layout retries or resize these candidates to force a pass. Repair/North/South/cargo/furniture/water/death and full native lifecycle remain open. No completion claim.
''',encoding='utf-8')
(P/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Veld West — repair review</title><style>body{background:#202a30;color:#e8eded;font:16px system-ui;margin:24px;line-height:1.5}p{max-width:850px}img{width:100%;max-width:1104px}a{color:#b7dae9}</style><h1>Veld West — repair review</h1><p>The selected scanner interiors change her face, hair and suit. Three whole-pose redraws improve the materials but fail the size or placement checks, so none is installed.</p><p>Rows: selected animation, then three rejected candidates. The first and last frames remain the selected idle pose, making the size and foot-position differences visible.</p><img src="all-candidates-comparison.png" alt="Selected West animation above three rejected redraws with unchanged idle endpoints"><p>We are keeping the installed animation until a replacement preserves Veld's identity, proportions, registration and motion together.</p><p><a href="../HANDOFF.md">Closeout notes</a></p>''',encoding='utf-8')
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
 else:raise RuntimeError('Concurrent updates prevented guarded prepend: '+str(path))
parent=P.parent/'HANDOFF.md';text=parent.read_text(encoding='utf-8');section='\n## Latest West repair attempt\nThree whole four-pose redraws rejected for head/size/registration drift. No normal changes.250 selected West source presentations and loader order verified unchanged. See west-interact-fix/HANDOFF.md. Original-based idle/scanner pair also needs coherent adjoining walk registration before admission.\n'
if '## Latest West repair attempt' not in text:parent.write_text(text+section,encoding='utf-8')
