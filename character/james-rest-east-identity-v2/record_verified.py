from pathlib import Path
import json,os,uuid,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
n=json.loads((P/'validate-evidence.json').read_text());w=json.loads((P/'validate-validation.json').read_text());v=json.loads((P/'packaging-validation.json').read_text())
assert n['failures']==0 and len(n['records'])==36 and not v['failures']
assert w['exitCode']==0 and not w['timedOut'] and (P/'validate.gd.uid').exists()
status='installed_native_source_verified_owner_review_pending'
for mode in ['bare','helmet']:
    file=P/(mode+'-manifest.json');pack=json.loads(file.read_text());pack['status']=status;file.write_text(json.dumps(pack,indent=2)+'\n',encoding='utf-8')
source_original='C:/Users/Alex/.codex/generated_images/01a0ef89-fc47-7e22-953f-3c02a051b0f6/exec-6a2e2f64-e49f-47c0-8fc9-557eb9ea965b.png'
(P/'selection.json').write_text(json.dumps({'status':status,'runtimeInstalled':True,'fullSetComplete':False,'sourceVersion':'source-v3.png','sourceOriginal':source_original,'sourceSha256':hashlib.sha256((P/'source-v3.png').read_bytes()).hexdigest(),'tool':'built-in imagegen','prompt':'prompt-v3.txt','statesPerMode':3,'sourceReferences':36,'fixedBodyScale':.4983164983164983,'fixedHelmetScale':.43209876543209874,'packageChecks':v['checks'],'nativeChecks':n['checks'],'nativeFailures':n['failures'],'nativeCaptures':36,'profileGuard':{'realProfileUnchanged':w['realProfileUnchanged'],'profileDelta':w['profileDelta']},'visualReview':'Source v3, fixed-ruler old/new head comparison, all36 paired source references and all36 native source-stage captures reviewed. Compact heads closer to East master; supported upward pitch retained. Captures use prescribed stages, not natural furniture journeys.','rejected':'candidate-v2-review.json','remaining':['Owner full-motion review','West/South reclining face proportions and cross-family identity review','All-frame continuous motion, actual gear and other furniture/travel/task handoffs across full James library'],'nativeScope':n['scope']},indent=2)+'\n',encoding='utf-8')
note='''

## James East reclining identity revision — October 1, 2026

james-rest-east-identity-v2/source-v3.png (built-in imagegen,prompt-v3.txt) replaces
the enlarged/full-cheeked East rest faces with a more compact master-relative
head. Entire authored figures retained; inherited fixed.4983164983 body ruler,
exact bare/helmet standing masters, shared neutral/reversed get-up and3600ms
sleeping clock. Accepted pitch donors reuse fixed.4320987654 common-shell ruler.
First candidate rejected/preserved: compact-head request changed poses3/4 to
forward-looking faces, creating an abrupt final tilt. v3 preserves upward pitch.
Review head identity/pitch before grading; matching whole standing height does
not prove the generated head matches when source0 is replaced by exact master.
Original metadata/ruler templates frozen locally before rebuilding override.

Paired three-state override selected after rest material in normal grid loader;
ACTIVE_ASSETS updated.147package/225native checks,0failures. All36 source poses
captured through normal NPC renderer with prescribed East life stages and checked
against exact loaded pixels, clocks/pivots/depth/rest-anchor metadata. All36
paired sources and36native crops reviewed, plus before/after heads/source-clock
comparison. Engine0/no timeout; strict real-profile guard false,last_session.json
only,cause unproven. Scratch APPDATA; no rollback. No actual furniture journey,
Continue or locker change claim: retained ordinary berths choose North regardless
of room rotation; specialized East bunk uses its own authored action family.
Full James objective active. West/South reclining head identity remains open.
'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    data=path.read_bytes()
    if b'## James East reclining identity revision' in data:continue
    enc=note.encode('utf-8');new=enc.lstrip(b'\n')+b'\n'+data if path.name=='CURRENT_STATUS.md' else data+enc
    temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new);os.replace(temp,path)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James East reclining identity

## Objective and acceptance
Full James animation/master/style/scale/perspective/material consistency and
cross-family polish. Goal active; installed source/native verified, owner pending.

## Accepted decisions and constraints
Compact master-relative head throughout whole source poses; preserve supported
recline/upward pitch, belt wrench, matte engineering suit. Fixed inherited body
and accepted common-shell rulers. Exact standing arrivals/joins and3600ms sleep.

## Current state
source-v3.png/prompt-v3.txt built-in imagegen; v2 rejected and saved for head-pitch
drift. New36paired lie/sleep/get-up frames; normal grid loader/ACTIVE_ASSETS select
East override after ordinary rest material. Other facings retained. Four original
metadata/ruler templates frozen; build_candidate.py/build_helmet.py deterministic.
validate.gd/.uid paired; source comparisons and36native pose captures retained.

## Verification
147package/225native checks0fail. Exact loaded36source slots via normal NPC
renderer prescribed life stages; clock/pivot/depth/rest-anchor metadata. All36
source and36native poses visually reviewed. Engine0/no timeout; strict owner
delta onlylast_session.json,cause unproven; scratch,no rollback. No natural berth,
Continue or gear-change journey: ordinary retained berth selectsNorth, special
East bunk uses separate actions. Source-clock preview is constructed playback.

## Next action
West/South reclining face proportional/perspective review, continuous motion
and family joins; actual furniture/gear/travel/task contexts where applicable.
Refresh selected inventory after this override; don't call coverage acceptance.
No provider/native job live. Full objective remains active.
''',encoding='utf-8')
print(json.dumps({'status':status,'packageChecks':v['checks'],'nativeChecks':n['checks'],'sourceReferences':36,'profileDelta':w['profileDelta']}))
