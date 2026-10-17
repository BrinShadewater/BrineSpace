from pathlib import Path
import json, hashlib, os, uuid
P=Path(__file__).resolve().parent; R=P.parents[1]
def read(p): return json.loads(p.read_bytes())
def atomic(p,b):
    t=p.with_name(p.name+'.'+uuid.uuid4().hex+'.tmp'); t.write_bytes(b); os.replace(t,p)
def write(p,v): atomic(p,(json.dumps(v,indent=2)+'\n').encode('utf-8'))
before=read(P/'runtime-input-before.json')
after={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in before}
assert before==after
write(P/'runtime-input-after.json',after)
review=read(P/'review-evidence.json')
guards={}
for direction in ['east','south','west']:
    g=read(P/(direction+'-validation.json'))
    assert g['exitCode']==0 and not g['timedOut'] and g['realProfileUnchanged'] and not g['profileDelta']
    log=(P/(direction+'.log')).read_text(encoding='utf-8')
    assert not any(term in log for term in ['ERROR:','SCRIPT ERROR:','FAILED'])
    assert (P/(direction+'.gd.uid')).exists()
    e=read(P/direction/'evidence.json')
    assert e['failures']==0 and len(e['cases'])==6
    assert {(c['phase'],c['mode']) for c in e['cases']}=={(phase,mode) for phase in ['torch-draw','weld','torch-stow'] for mode in ['power','doors']}
    assert sum(c['repeatedLoss'] for c in e['cases'])==1
    assert all(c['workAfter']>c['workBefore'] for c in e['cases'])
    assert all(row['helmet'] for row in e['records'])
    guards[direction]={k:g[k] for k in ['exitCode','timedOut','realProfileUnchanged','profileDelta']}
checks=sum(f['checks'] for f in review['families'].values())
captures=sum(f['distinctCaptures'] for f in review['families'].values())
nb=sum(len(f['nativeBoards']) for f in review['families'].values())
sb=sum(len(f['sourceBoards']) for f in review['families'].values())
review['visualReview']={'nativeBoardsReviewed':nb,'sourceBoardsReviewed':sb,'masterReviewed':True,'ownerAcceptance':'pending'}
write(P/'review-evidence.json',review)
note=f'''## James helmet construction cardinal interruption review — October 1, 2026

character/james-construction-helmet-cardinal-v1 adds actual East/South/West paid
build interruption evidence to the earlier North lane. {checks} checks0failures,
{captures} distinct native/source captures:18power/locked-door cases across draw,
held weld and stow, including3repeated power losses during held-pose return.
Normal60Hz controller updates preserve paid work/order/physical foot, pause,
admissible snapshot, exact original selected helmet source and no interrupted
sparks; allthree actual jobs resume and complete once. Initial world/foot reset
per dedicated directional fixture, supported prescribed worn gear. No locker
fitting, natural owner layouts or new fresh-scene Continue proof.

All{nb}native/{sb}source boards plus original four-direction helmet master board
visually reviewed. Same matte grade,184canvas/p92,172/148 ruler, attached helmet,
whole arms/body, stable contact and neutral joins. All recorded sourceRGBA matches
original helmet pool; no new PNG/source state/art/production/timing changes.
Three engines terminal0/no timeout/clean logs, strict owner fingerprints unchanged
under separate scratch APPDATA. Ten whole-file production inputs equal before
launches and after terminal runs. GIF is50ms per captured East source pose,
simplified motion order, not continuous native footage. Owner review remains open.

Lesson: test arbitrary current-source retraction and repeated loss in each authored
facing. Whole-source recipe parity alone does not establish native controller,
visible contact or draw/held/stow handoffs. Remaining full-facing/phase disk
Continues, locker-to-job integration and broader full-set/cross-family polish.
Full James goal remains active. See folder HANDOFF.md and review-evidence.json.

'''
status=R/'docs/CURRENT_STATUS.md'; atomic(status,note.encode('utf-8')+status.read_bytes())
lesson=f'''\n## James dry helmet cardinal interruption evidence — October 1, 2026

East/South/West actual construction interruption matrix now complements North:
{checks} checks0failures/{captures} native original-source views;18draw/held/stow
power/door cases,3repeated losses mid-return, pause/clock/order/foot/sparks guards
and normal paid completion. All{nb}native/{sb}source boards and directional
helmet masters reviewed. No source/grade/ruler/timing or production change.
Each directional fixture uses ordinary approach after initial prescribed scene/
foot reset and supported worn gear; no locker integration or fresh Continue.
Scratch profiles unchanged, three clean terminal engines, ten production hashes
frozen. Whole-source parity must be accompanied by every authored facing's actual
interruption/contact/join review.50ms source-order GIF is not native cadence proof.
Evidence: character/james-construction-helmet-cardinal-v1. Full goal remains active.
'''
for p in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    atomic(p,p.read_bytes()+lesson.encode('utf-8'))
write(P/'selection-review.json',{'status':'installed_sources_cardinal_native_interruption_review_owner_pending','productionChanges':False,'newSourceStates':0,'fullSetComplete':False,'checks':checks,'failures':0,'captures':captures,'cases':18,'freshContinues':0,'guards':guards,'review':'review-evidence.json','remaining':['Full direction/phase disk Continues','Locker-to-job equipment integration','Natural owner worksite acceptance','Broader full-set and cross-family polish']})
parent=R/'character/james-construction-helmet-v1/selection-review.json'; v=read(parent); v['cardinalInterruptions']='character/james-construction-helmet-cardinal-v1/selection-review.json'; write(parent,v)
handoff=f'''# Project handoff

Updated: October 1, 2026 · Project: Brine Space · Task: James helmet construction cardinal interruptions

## Objective and acceptance

Continue full James set, master matching and cross-family polish. This milestone
closes other-facing actual construction interruption coverage; owner review open.

## Accepted decisions and constraints

Original matte helmet master sources, fixed184canvas/p92,172/148 standing ruler,
paid10second construction budget and whole-source retraction/reentry retained.
No art, timing, production scripts, owner layouts or save changes.

## Current state

Three directional native fixtures, separate scratch runs, reports/review boards,
master comparison and simplified East source-order GIF in this folder. Parent
helmet construction review linked; current status, pipeline, bible and both skill
references updated atomically without replacing concurrent actor work.

## Verification

{checks} checks0failures/{captures} exact original-source native captures,18 cases,
3repeated mid-return losses, all three normal paid jobs complete once. All{nb}
native/{sb}source boards and directional master comparison visually inspected.
Three engines exit0/no timeout/clean logs, owner fingerprints unchanged, ten
production input hashes unchanged. Initial world/foot reset, prescribed worn gear,
ordinary approach and actual controller updates. No new disk Continue or locker
fitting evidence. Source-order GIF uses50ms captured-pose steps, not native timing.

## Next action

Cover fresh disk Continue across every helmet construction facing/motion phase,
then actual locker fitting into jobs and remaining broader motion/master joins.
Full-set completion still requires cross-family and owner visual review.
'''
atomic(P/'HANDOFF.md',handoff.encode('utf-8'))
print(json.dumps({'checks':checks,'captures':captures,'nativeBoards':nb,'sourceBoards':sb,'guards':guards}))
