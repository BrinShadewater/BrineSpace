"""Keep measured lifecycle scope, current world clips and the rejected evidence."""
from pathlib import Path
import json, os, hashlib
from PIL import Image, ImageDraw
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
def atomic(path, transform):
    old=path.read_bytes();temp=path.with_name(path.name+'.james-lifecycle.tmp');temp.write_bytes(transform(old))
    assert path.read_bytes()==old, f'Concurrent modification: {path}';os.replace(temp,path)
def dump(path,value):path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
r=json.loads((P/'native-lifecycle-evidence.json').read_text());v=json.loads((P/'native-lifecycle-validation.json').read_text())
assert (r['checks'],r['failures'])==(13764,0)
assert len(r['journeys'])==4 and len(r['matrix'])==40
assert v['exitCode']==0 and not v['timedOut']
log=(P/'native-lifecycle.log').read_text()
assert not any(term in log for term in ['ERROR:','WARNING:','SCRIPT ERROR'])
second=[x for x in r['matrix'] if x['mode']=='new-attempt'];death=[x for x in r['matrix'] if x['mode'].startswith('death')]
assert len(second)==4 and all(x['actualFullSecondDispatchReturn'] for x in second)
assert len(death)==8 and min(x['renderBodyDifference'] for x in death)>5
directions=['east','south','west','north'];board=Image.new('RGB',(730,4*310),'#303b40');draw=ImageDraw.Draw(board)
for q,direction in enumerate(directions):
    item=next(x for x in death if x['rotation']==q and x['mode']=='death-after')
    for column,key in enumerate(['before','after']):
        image=Image.open(ROOT/item[key]['native'].removeprefix('res://')).convert('RGB').crop((125,150,305,295))
        image=image.resize((360,290),Image.Resampling.NEAREST)
        board.paste(image,(column*365,q*310+20))
        draw.text((column*365+8,q*310+3),direction+' / '+('recall entrance' if key=='before' else 'death after release'),fill='white')
    journey=next(j for j in r['journeys'] if j['rotation']==q)
    frames=[Image.open(ROOT/s['native'].removeprefix('res://')).convert('RGB') for s in journey['contactSamples']]
    assert len(frames)==21
    gif=P/(direction+'-world-review.gif')
    frames[0].save(gif,save_all=True,append_images=frames[1:],duration=[350]+[90]*19+[700],loop=0,disposal=2)
    pack=P.parent/('james-case-release-'+direction+'-v1')
    frames[0].save(pack/'native-lifecycle-world-review.gif',save_all=True,append_images=frames[1:],duration=[350]+[90]*19+[700],loop=0,disposal=2)
    selection=json.loads((pack/'selection.json').read_text())
    selection.setdefault('evidence',{})['currentWorldLifecycle']='../james-case-release-lifecycle-v1/native-lifecycle-evidence.json'
    selection['currentWorldReview']='native-lifecycle-world-review.gif'
    dump(pack/'selection.json',selection)
    atomic(pack/'HANDOFF.md',lambda old:old+b'\n## October 1 lifecycle follow-up\nCurrent shared runtime preserves release-facing death, renders deceased James in open sea after expedition clears, and removes the extra .038cell case offset. All four facings tested in james-case-release-lifecycle-v1:13,764checks/0fail, four parent recalls/fresh-scene Continues plus four real second dispatches/returns and36controlled interruption branches. Current rendered clip: native-lifecycle-world-review.gif. Older native-world review/report retains its original pre-origin-fix revision/scope. Strict owner-profile guard failed with last_session.json delta; mortality pose joins/peer traffic/full-set polish remain.\n')
board.save(P/'death-visibility-review.png')
scope='Four real cardinal parent recalls and fresh-scene Continues with exact case anchor/heading restoration; four additional real second dispatch/arrival/recall/return trips.36 controlled interruption branches naturally reach pickup2 from actual parent work arrivals; actor-only restore/world resets, not36 complete interrupted trips/Continues. Selected equipped source, exact entrance, removed/depleted/disabled sites, low-air safety, held empty-pose physical motion under site obstruction, no extraction/credit, actual dead-body render presence against hidden controls and visible death heading. Death raw texture byte equality uses different canvas/pivots and does not certify pose continuity. Bare exterior/peer traffic/other hazard contexts remain unproven.'
r['scope']=scope
for item in death:item['deathInputTextureBytesMatch']=item.pop('deathInputPixelsMatch')
dump(P/'native-lifecycle-evidence.json',r)
old_scope='Death contact discontinuity is measured separately and is not certified by selected-source checks.'
replacement='Death texture byte identity is measured across different canvas/pivots; it does not certify pose continuity. Four additional real second-dispatch arrival/recall/return trips and actual body render controls are checked.'
atomic(P/'prepare_fixture.py',lambda old:old.replace(old_scope.encode(),replacement.encode()))
atomic(P/'lifecycle-body.gd.txt',lambda old:old.replace(b'"deathInputPixelsMatch":death_match',b'"deathInputTextureBytesMatch":death_match'))
atomic(P/'native-lifecycle.gd',lambda old:old.replace(old_scope.encode(),replacement.encode()).replace(b'"deathInputPixelsMatch":death_match',b'"deathInputTextureBytesMatch":death_match'))
dump(P/'selection.json',{'status':'verified_world_lifecycle_visual_fixes','ownerVisualAcceptance':False,'checks':13764,'failures':0,'actualParentReturnsAndContinues':4,'actualSecondDispatchReturns':4,'controlledInterruptionBranches':36,'productionFiles':['scripts/branforth_npc.gd','scripts/main.gd','scripts/james_case_deposit.gd'],'productionSourceHashes':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ['scripts/branforth_npc.gd','scripts/main.gd','scripts/james_case_deposit.gd']},'evidence':'native-lifecycle-evidence.json','validation':'native-lifecycle-validation.json','scope':scope,'profileGuard':v['realProfileUnchanged'],'profileDelta':v['profileDelta'],'fullGoalActive':True})
handoff='''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James release lifecycle and death visibility

## Objective and acceptance
Full James animation coverage/master/style/perspective/height/proportions/grade work remains active. This milestone fixes shared runtime visual defects and exercises release interruptions; it does not finish life/rest/mortality coverage or cross-family polish. Owner visual acceptance pending.

## Accepted decisions and constraints
Independent four-facing art and source clocks retained. Case is cosmetic site-owned state; no cargo, economy or route rule change. Keep actual visible release heading when death clears the action. A deceased diver must remain drawable in open sea after expedition clears. Body renderer subtracts .038cell in get_chief_branforth_position then adds it in draw; the ground case must use the resulting real foot origin without another offset. Compare actual drawn pixels using the real pivot, not just loaded texture presence or raw bytes from incompatible planes.

## Current state
branforth_npc.gd die preserves saved release-facing before clearing it. main.gd has_chief_branforth permits active dead exterior bodies after expedition clears. james_case_deposit.gd rectangle removes extra .038cell vertical offset for all four facings. Other concurrent changes in these files are not this milestone. New lifecycle fixture/generator/body source/paired Godot UID, current evidence/validation/log, review board and four current world GIFs. Four source packs now link current shared lifecycle evidence and native-lifecycle-world-review.gif; older world reports/GIFs retain their original scope/revision.

## Verification
Final13,764checks/0fail, terminal engine0/no timeout/no warnings/errors, scratch APPDATA resolved. Four real cardinal parent pickup2 recalls/airlock returns with paused fresh-scene disk Continue including exact case anchor/heading, plus four real second dispatch/arrival/work0 recall/return trips proving ownership clears only at new work arrival.36controlled branches from actual parent arrivals naturally reach pickup2: erased/depleted before release, erased/depleted/inactive after, death before/after, registered site-obstructed turn and normal low-air safety. Actor-only restore/world reset between branches; these are not36 complete interrupted trips/Continues. Movement continues under held empty pose, turns release when obstruction clears; no metal/data credit/extraction. Eight actual death visible-pixel comparisons against actor-hidden controls average26.22..35.51RGB levels, threshold5; all visible headings retained. Actual body/case scene crops reviewed. Strict full owner-profile guard FAILED, last_session.json delta only; cause unproven, no owner rollback or clean-guard retry.
Rejected evidence retained: prior-initial-review13,652green checks had8capture-helper script errors and wrong death heading; prior-heading-only-review13,712green checks still drew no dead open-sea body; prior-offset-sampler-review13,740checks/4fails had actual visible corpses but pixel sampler added a nonexistent .038cell offset. Offline corrected body score33.33confirmed coordinate fault before final native run. These earlier counts do not certify current fixes. Raw death texture byte comparisons cross256x276/p128,128 and256x360/p128,224 planes; false equality is not registered motion evidence.

## Next action
Return to missing James life/rest/meal/mortality context artwork. Actual registered release-to-death arm/body transitions still need contextual motion/polish; current checks prove heading/visibility, not smoothness. Peer traffic, other hazards and broader interrupted Continue contexts remain open. Then complete cross-family master/height/proportion/material/perspective/motion polish. No commit/export or owner layout/save change; goal active.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
note='''\n## James release lifecycle and death visibility — October 1, 2026

Shared four-facing release runtime fixes: preserve visible cancellation-facing on death; draw James's dead exterior body after expedition clears; remove the ground case's extra .038cell vertical offset (body getter subtracts that offset and drawing adds it back). Source art/clocks, economy and route rules retained. Current clips in each release pack: native-lifecycle-world-review.gif. Older world GIF/reports retain pre-origin-fix revision evidence.
Final13,764checks/0fail: four real cardinal parent recalls/returns/paused fresh-scene Continues with exact world case restoration, plus four real second dispatch/arrival/work0 recall/returns.36controlled interruptions from actual work arrivals: removed/depleted sites before/after, inactive remaining site, death before/after, actual site-obstructed turn and normal low-air recall. Actor-only restores/world resets; not36full interrupted trips/Continues. Eight dead-body render comparisons with hidden controls average26.22..35.51RGB levels; visible heading retained, case origin checked against body renderer. Native0/clean/no timeout/scratch. Strict full owner-profile guard FAILED,last_session.json delta; attribution unproven, no owner restoration or clean-guard retry. Prior false-green/fixture-error evidence archived in james-case-release-lifecycle-v1.
Lesson: verify actual world draw presence, not loaded texture alone. Clearing an expedition can remove the actor's visibility condition while its death source still loads correctly. Audit source pivot plus actor-position and draw offsets together; repeating one offset in both a test and cosmetic layer can conceal a real contact jump. Compare registered image planes before drawing motion conclusions from unequal bytes. Mortality pose continuity is still pending; current fixes prove heading/visibility/contact origin. Full James goal active, life/rest/meal/context gaps and peer traffic/other hazards/full cross-family polish remain. See character/james-case-release-lifecycle-v1/HANDOFF.md. No commit/export requested.
'''.encode('utf-8')
paths=[ROOT/'docs/CURRENT_STATUS.md',ROOT/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
    if b'James release lifecycle and death visibility' not in path.read_bytes():atomic(path,lambda old:note+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n'+note)
print(json.dumps({'checks':13764,'failures':0,'actualTrips':8,'freshSceneContinues':4,'controlledInterruptionBranches':36,'currentWorldClips':4,'profileGuard':'failed: last_session.json'}))
