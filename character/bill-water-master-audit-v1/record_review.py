"""Record inspected source evidence without changing artwork or runtime selection."""
from pathlib import Path
from PIL import Image
import hashlib,json,numpy as np
P=Path(__file__).resolve().parent; R=P.parent.parent
report=json.loads((P/'audit.json').read_text(encoding='utf-8'))
changed=[f for f,h in report['inputsSHA256'].items() if hashlib.sha256((R/f).read_bytes()).hexdigest()!=h]
assert not changed,changed
def registered(path,pivot,height):
    im=Image.open(R/path).convert('RGBA'); scale=148/height
    if scale!=1: im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    out=Image.new('RGBA',(320,352));out.alpha_composite(im,(round(160-pivot[0]*scale),round(224-pivot[1]*scale)))
    return out
checks=[]
for row in report['rows']:
    if row['direction']!='west':continue
    normal_file='character/crew-runtime-matte-v1/bill/manifest.json' if row['gear']=='bare' else 'character/bill-shared-helmet-runtime-v2/manifest.json'
    normal=json.loads((R/normal_file).read_text(encoding='utf-8'))
    a=registered(row['normalIdleSource'],normal['pivot'],normal['standingHeight'])
    index=0 if row['phase']=='entry' else len(row['frameFiles'])-1
    b=registered(row['frameFiles'][index],row['sourcePivot'],row['sourceHeight'])
    aa=np.array(a);bb=np.array(b);different=np.any(aa!=bb,axis=2)
    checks.append(dict(phase=row['phase'],gear=row['gear'],pose=index,registeredRGBAExact=not bool(different.any()),changedPixels=int(different.sum()),normalAlphaBounds=a.getchannel('A').getbbox(),contextAlphaBounds=b.getchannel('A').getbbox()))
report['visualReview']={'status':'All four static boards inspected at their shared physical scale; provisional fidelity findings, not motion acceptance.',
 'east':'Closer normal/context continuity. Some moving poses differ in cuffs/material; final exit context is a walking pose, not idle. Inspect motion and contact separately.',
 'west':'Highest repair priority: bare standing contexts visibly broader/brighter than current normal idle; helmet standing contexts use normal helmet idle. Arm-ready bare head/body and later rising poses still need original-master proportion/detail/grade review.',
 'north':'Early lowered entry poses appear smaller in head/backpack/arm mass; later rise has broader bare head and brighter hardware than normal idle. Distinguish articulation from source-density drift in close registered comparisons.',
 'south':'Early lowered and near-standing poses remain brighter than current matte normal idle. Revised squat is improved; full head/shoulder/detail and moving-join review remains pending.',
 'limits':['Foot ruler records registration, not actual ground/water contact.','Bare master repeated in helmet rows proves no helmet design fidelity.','Static context mismatch is not automatically a runtime endpoint defect: fixture bridges bind actual incoming/outgoing gait frames.','No new native, save, profile or continuous-motion acceptance.']}
report['westStandingContextChecks']=checks
report['inputVerification']={'frozenInputs':len(report['inputsSHA256']),'changed':changed,'allStable':True}
report['nextRepair']='Original-master West arm-ready pose and staged bare standing context authority, preserving fixed source density; then West rise and North/South grade/proportion repairs. Refresh native evidence only after new source selection.'
(P/'audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
note='''## Bill four-direction water master audit — October 2, 2026

Reviewed all four source boards:122 frame slots/16 rows against current normal idle manifests and established original directional master registrations. Common H148/320x352/p160224; no posed-height fitting, mirroring, grading or source mutation. All152 frozen inputs unchanged. Bare master repeated in helmet rows is identity context only. No native/profile access or new continuous motion/contact acceptance.

West is first repair priority: bare standing contexts visibly broader/brighter than current normal idle while helmet contexts use current normal idle. Registered RGBA endpoint comparisons are recorded in character/bill-water-master-audit-v1/audit.json. West arm-ready and rising interiors also need original-master head/build/detail/grade repairs; changing static contexts alone cannot certify these poses. North early lowered head/backpack/arm mass and later rising head/hardware remain provisional; South early/near-standing grade still differs from current matte idle; East is closer but motion/contact/cuff/material review remains open.

Lesson: compare each gear's complete pose bank against the actual current normal manifest at common physical scale. Equipment source endpoint substitution can conceal a different bare body authority. Separate context consistency, posed anatomy, material grade and runtime gait binding. Foot registration alone does not prove contact; static source equality does not prove moving continuity. References retain directional authoring density and do not fit each crouch to standing height.

Next original-master West arm-ready/context repair, then West rise and North/South proportion/grade; refreshed native contact/motion evidence, guarded normal admission/cargo lifecycle and entire-library consistency/polish. Full Bill objective active/incomplete. Audit: character/bill-water-master-audit-v1/index.html.
'''
guides=[R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in guides:
    with f.open('rb') as s:s.seek(max(0,f.stat().st_size-65536));tail=s.read().decode('utf-8',errors='replace')
    if '## Bill four-direction water master audit — October 2, 2026' not in tail:
        with f.open('a',encoding='utf-8') as s:s.write('\n\n'+note)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Bill full animation set

## Objective and acceptance
Complete full Bill set matching original masters, camera, physical scale/proportions and matte grade, then cross-family consistency/polish and normal game integration.

## Accepted decisions and constraints
Reversible source repairs authorized. Preserve independently authored directions and fixed source density. No per-pose height fitting. Keep staged candidates unselected until scoped visual/runtime admission evidence. Protect owner data and concurrent crew work.

## Current state
Four-direction source audit boards/index, recorded findings and reproducible endpoint/input checks. Six guidance files updated. Art and runtime selections unchanged.

## Verification
122 slots,16 rows,152 source/reference/manifest inputs stable; all four boards visually inspected. West endpoint registered RGBA comparisons in audit.json. Static evidence only; no new native/profile interval or continuous motion/contact acceptance.

## Next action
Repair West original-master arm-ready/context authority, then rise and North/South grade/proportions; refresh native contact/motion evidence, normal admission/cargo lifecycle and full-library consistency/polish. Full goal remains active.
''',encoding='utf-8')
print(json.dumps({'stableInputs':len(report['inputsSHA256']),'westChecks':checks,'guidanceFiles':len(guides)}))
