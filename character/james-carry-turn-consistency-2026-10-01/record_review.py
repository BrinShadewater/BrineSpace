from pathlib import Path
import json, os, uuid
from PIL import Image, ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
e=json.loads((P/'review-evidence.json').read_text());rows=e['records']
quarter={r['sha256'] for r in rows if len([q for q in rows if q['key']==r['key'] and q['mode']==r['mode']])==6}
half={r['sha256'] for r in rows if len([q for q in rows if q['key']==r['key'] and q['mode']==r['mode']])==11}
assert half.issubset(quarter)
e['halfTurnPixelsAllReuseReviewedQuarterTurns']=True
(P/'review-evidence.json').write_text(json.dumps(e,indent=2)+'\n')
# Exact six-slot clock, static masters left/right, animated source in middle.
sheet=Image.open(P/'carry-turn-east-south.png').convert('RGB');frames=[]
rr=[r for r in rows if r['key']=='carry-turn-east-south' and r['mode']=='bare']
for i in range(6):
    frame=Image.new('RGB',(768,560),'#303b40')
    for row in range(2):
        for col,source_col in enumerate([0,i+1,7]):
            frame.paste(sheet.crop((source_col*256,row*280,(source_col+1)*256,(row+1)*280)),(col*256,row*280))
    frames.append(frame)
frames[0].save(P/'east-south-master-comparison.gif',save_all=True,append_images=frames[1:],duration=[r['durationMs'] for r in rr],loop=0,disposal=2)
note='''

## James selected carrying-turn ruler review — October 1, 2026

james-carry-turn-consistency-2026-10-01 freezes184 selected references across
12 dry carrying-turn states/both gears. Whole-source quarter-turn boards compare
both directional idle masters at fixed pivot/148px scale. Twelve opposite-path
pairs are exact byte reversals; half-turn art is entirely reused reviewed quarter
poses. Bare crowns76..77/soles222..224 on256 plane; alpha heights146..149.
Helmet crowns68..74 include directional master shell differences; do not force
all facings to one bounding-box height. No runtime/art change or new native run.
Source-clock800ms East/South preview has fixed masters beside all six poses.
This proves source registration/coverage, not continuous native foot contact or
task handoffs. Reclining head fullness remains open in rest-material handoff.
Full James goal active; selected coverage is not full-set visual acceptance.
'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    data=path.read_bytes()
    if b'## James selected carrying-turn ruler review' in data:continue
    enc=note.encode('utf-8');new=enc.lstrip(b'\n')+b'\n'+data if path.name=='CURRENT_STATUS.md' else data+enc
    temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new);os.replace(temp,path)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James carrying-turn ruler review

## Objective and acceptance
Full James animation/master consistency and cross-family polish; active.

## Accepted decisions and constraints
Fixed148px declared scale and registration. No per-pose resizing/translation.
Compare both directional masters; shell perspective changes are not body scale.

## Current state
New read-only review builder, twelve paired source boards, frozen184paths/hashes/
bounds/durations and East/South exact800ms preview. No runtime/art modification.
Preceding rest material revision installed and verified; its handoff governs it.

## Verification
Four paired quarter-turn boards and two half-turn boards reviewed. Twelve
opposite pairs exact reverse; all half-turn pixels reuse reviewed quarter poses.
Bare crown76..77,sole222..224,height146..149. Helmet crown68..74 includes accepted
directional masters. No native/controller claim from source measurements.
Rest preceding revision752package/841native,146asset rebuild byte-identical;
strict owner delta last_session.json only,cause unproven.

## Next action
Continue master-relative shell/perspective and chronological/native turn joins;
rest reclining head fullness remains unresolved. Review actual cargo task handoffs
and other furniture/gear/travel contexts. Full library acceptance remains open.
''',encoding='utf-8')
print(json.dumps({'references':len(rows),'exactReversePairs':len(e['reverseChecks']),'halfTurnReuse':True,'previewDurationMs':sum(r['durationMs'] for r in rr),'runtimeChanges':False}))
