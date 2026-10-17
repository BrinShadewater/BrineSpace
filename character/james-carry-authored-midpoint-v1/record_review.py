from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
for name,root in [('inputs.json',r),('lower-inputs.json',p)]:
    data=json.loads((p/name).read_bytes());assert all(hashlib.sha256((root/k).read_bytes()).hexdigest()==h for k,h in data['preCallSha256'].items())
for name,execution,verdict,findings in [
    ('review.json','exec-d7923287-46cb-491a-a489-3e0c777b0af6','rejected-height',[
        'Raw/full/upper and82/54/27station-scale boards inspected. Intended intermediate front-left orientation, stable two-hand case grip, belt-side tools and planted feet represented.',
        'Head crown76matches endpoints, but sole221 versus224 gives145visible height versus148. Full source not accepted at this scale; no figure-bounds fitting applied.',
        'Material/detail and shoulder patch differ subtly from independent endpoints; static pose cannot establish temporal continuity or original-master identity acceptance.']),
    ('lower-review.json','exec-7bdb00a3-6677-4f61-987a-788df2d3a046','provisional-representative-pose',[
        'Raw generated crop/full/detail and82/54/27station boards inspected. Local authored lower-shin extension restores crown76/sole224 at original whole-canvas scale.',
        '62500 original midpoint pixels outside94,178..160,224 byte-exact, including head/torso/hands/case/hips/kneepads. Original source limbs not warped or globally fitted.',
        'Both boots remain planted and leg joints read coherently; no purple backpack or large black underarm mass in this static candidate.',
        'Single bare representative midpoint only; exact45degree angle is authoring intent, not measured projection. Fine material/patch/tool/boot-family matching still requires neighboring poses and motion review.',
        'No shared helmet, native/source temporal review, normal integration, fresh Continue or owner acceptance.'])]:
    path=p/name;data=json.loads(path.read_bytes());data.update(visualReviewPending=False,sourceAcceptance=False,selected=False,disposition=verdict,generationExecution=execution,findings=findings);path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
section='''### James explicitly authored carrying midpoint and height repair — October 2, 2026

Matched whole-video448180480450899 terminal REJECTED after all142frames: wrong-way
spin, lifted feet, purple backpack. New single bare whole-body midpoint authored
between exact South/West carrying references using built-in transparent imagegen
exec-d7923287-46cb-491a-a489-3e0c777b0af6. References256uniform4x; raw1254whole
canvas ->256, no body-bounds fit/grade. Raw/full/upper/82/54/27boards reviewed:
intended front-left angle and two-hand case grip viable, but145height/crown76/
sole221 differs from endpoint148/crown76/sole224. Original full draft rejected.

Localized lower-shin source edit exec-7bdb00a3-6677-4f61-987a-788df2d3a046 uses
original80square crop88,152..168,232, uniformly8x before call and original80square
after. Admitted only94,178..160,224;62500outside original midpoint pixels exact,
head/torso/hands/case/hips/kneepads protected. Generated lower-shin extension,
not pixel stretching/whole-body fit, restores crown76/sole224. Raw/full/detail/
82/54/27boards inspected; static bare midpoint-lower-v2 provisionally viable.
Material/patch/tool/boot-family differences still require adjacent poses and full
motion. SourceAcceptance remains false; no helmet/native/normal admission.

Lesson: a good intermediate angle can still be three native pixels short. Record
actual crown/sole against common source ruler, repair anatomy in generated source,
and preserve successful upper pose exactly. Bounding geometry is a diagnostic,
not proof of master identity or smooth cadence. Next author22.5/67.5degree whole
carrying poses at common148ruler, review full shortest-path joins/material, fit
shared helmet, then native cargo/Continue and full cardinal/context consistency.
Frozen inputs stable; all new raster/video files covered by Git LFS. Normal
cap/V9/riseV6/caseV7 remain selected. Full objective active/incomplete.
Evidence:character/james-carry-authored-midpoint-v1/HANDOFF.md.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James canonical South carry and matched quarter-turn submission');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new);assert path.read_bytes()==old;os.replace(tmp,path)
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James authored carrying midpoint

## Objective and acceptance
Full master/style/perspective/size/height/proportion/matte James animation set,
then full cross-family consistency and polish. Active/incomplete.

## Accepted decisions and constraints
Normal cap/V9/riseV6/caseV7 retained. Explicit authored carrying angles replace
uncontrolled whole-turn retries. Common256canvas/148standing ruler/pivot128224;
no per-pose fitting, anatomy warp or grade. Sources remain provisional.

## Current state
Whole midpoint raw.png/prompt.txt, inputs/package and reviewed whole/upper/station
boards retained. Initial source145height rejected. Local generated lower-shin
repair lower-raw.png/lower-prompt.txt admitted to midpoint-lower-v2.png;
lower-review.json closed provisional representative pose. Five guides updated.

## Verification
Both frozen input inventories stable; all raw/source/detail/station boards inspected.
Initial crown76/sole221, repair crown76/sole224 matching endpoint geometry.
62500original midpoint outside pixels exact. LFS applies to generated rasters/video.
No paired helmet, advancing motion/native lifecycle/normal selection or owner acceptance.

## Next action
Author22.5 and67.5degree whole-body carried poses from same source family/ruler,
review ordered complete turn and actual endpoint joins/material/feet. Then shared
helmet/native cargo lifecycle and fresh Continue before versioned normal admission.
Finish all cardinal/context/master checks and full cross-family consistency polish.

Built-in imagegen executions:exec-d7923287-46cb-491a-a489-3e0c777b0af6;
lower repair:exec-7bdb00a3-6677-4f61-987a-788df2d3a046.
Saved prompts:prompt.txt,lower-prompt.txt; raw sources:raw.png,lower-raw.png.
''',encoding='utf-8')
print('Initial short pose rejected; repaired representative midpoint provisional. Both inventories stable; five guides and handoff updated.')
