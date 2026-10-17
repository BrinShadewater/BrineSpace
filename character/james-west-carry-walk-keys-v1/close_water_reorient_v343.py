from pathlib import Path
import json,hashlib,shutil
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];src=p/'water-stop-bridge-v340';out=p/'water-reorient-review-v343'
v=json.loads((src/'reorient_probe-validation.json').read_bytes());assert v['exitCode']==0 and v['realProfileUnchanged'] and not v['timedOut']
d=json.loads((src/'reorient-review.json').read_bytes());assert d['checks']==19585 and d['failures']==0 and d['samples']==816 and d['rows']==288
for name in ['reorient_probe.log','reorient_probe-validation.json','reorient-review.json']:shutil.copyfile(src/name,out/name)
for stem,count in [('probe',290),('interrupt_probe',2289),('clearance_probe',3697)]:
    v=json.loads((out/(stem+'-validation.json')).read_bytes());assert v['exitCode']==0 and v['realProfileUnchanged'] and not v['timedOut']
    assert any('checks='+str(count)+' failures=0' in line for line in v['summary'])
inventory=json.loads((p/'selected-family-audit-v333/selected-inventory.json').read_bytes())
durations=[]
for gear,rows in inventory['gears'].items():
    bank={x['key']:x for x in rows}
    for source in ['west','east','north','south']:
        for target in ['west','east','north','south']:
            if source==target:continue
            turn=bank['swim-turn-'+source+'-'+target]
            for slot in range(6):
                swim=bank['swim-'+source];stop=bank['swim-stop-'+source]
                durations.append(40+sum(swim['durationsMs'][slot+1:5])+sum(turn['durationsMs']))
                durations.append(40+sum(stop['durationsMs'][:slot])+sum(turn['durationsMs']))
bindings={}
for stem in ['phase_player','reorient_player','staged_grid','reorient_probe']:
    f=src/(stem+'.gd');assert (src/(stem+'.gd.uid')).is_file();bindings[str(f.relative_to(r))]=hashlib.sha256(f.read_bytes()).hexdigest();shutil.copyfile(f,out/(stem+'.gd.txt'))
report={**d,'version':343,'finitePoseSlots':3096,'regressions':{'entry':290,'interrupt':2289,'clearance':3697,'failures':0},'syntheticRendererCollisionRows':288,'authoredCombinedClockRangeMs':[min(durations),max(durations)],'clockRangeSource':'Derived from V333 selected clocks and current deterministic bridge construction; technical range, not observed physical movement.','postRunCodeBindings':bindings,'prelaunchFreeze':False,'ownerProfileUnchanged':True,'sourceAcceptance':False,'fullGoalComplete':False,'visualMotionAcceptance':False,'remaining':'Full changed-heading temporal/source-motion review and responsiveness, repeated requests at completion, blocked-space fallback, actual main-scene/exterior route collision, normal selection and whole-run Continue; remaining full-family source fidelity and polish.'}
(out/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
section='''### James staged changed-heading swimming restart — October 3, 2026

V343 reorientation subclass retains V342 base and selected original pixels/metadata.
Actual loader confirms all24bare/helmet direction-pair turn entries/exits exactly
match neutral swim poses.288finite derived rows reuse remaining stroke or reversed
rise, then the selected directional turn. Resume starts from current exact pose;
finite plan completion resets gait at destination neutral without replaying travel.
Fixture renderer now predicts/clears whole reorientation envelope without mutation.

Isolated native19585checks0:816changed-heading resume samples,288rows/3096pose slots,
every slot clock/pause/fresh restore/interrupted stop pose, finite checkpoint keys,
288open/blocking geometry renderer cases through actual James collision primitive.
Regressions on the new subclass:290entry +2289interruption +3697clearance checks0.
Owner profiles unchanged. Tested source text snapshots/post-run hashes retained;
no prelaunch freeze. No new art, grading or normal production selection.

Finite clocks span560..1360ms across installed rows (selected-clock derivation).
Earlier commentary estimated over two seconds from an unrelated dry-turn clock;
that estimate is withdrawn. Exact pose equality does not prove
good responsiveness or temporal motion. Full playback review, repeated requests
at completion, blocked-space fallback, actual native/main-scene/exterior route and
whole-run Continue remain before installation. Pixel sources retain original
coarse material/master fidelity issues. Full animation goal active/incomplete.
Handoff: character/james-west-carry-walk-keys-v1/water-reorient-review-v343/HANDOFF.md.
'''
assert report['authoredCombinedClockRangeMs']==[560.0,1360.0],report['authoredCombinedClockRangeMs']
record_guides(r,section,'### James staged heading-safe rise and full-bridge clearance — October 3, 2026')
(out/'HANDOFF.md').write_text('# Project handoff\n\nUpdated: October 3, 2026 · Task: James changed-heading resume\n\n## Objective and acceptance\nFull James animation set matching original masters followed by consistency/polish. Incomplete.\n\n## Accepted decisions and constraints\nExact selected poses and original rulers/grade/equipment; finite visual plans keep actor physics independent. Staged only.\n\n## Current state\n'+section+'\n## Verification\n19585new checks0;three new-player regressions290/2289/3697checks0;816resume samples;288finite rows/3096slot samples/288synthetic collision cases;owner unchanged. No native motion or whole-run acceptance.\n\n## Next action\nReview actual changed-heading playback and responsiveness before installation; resolve blocked-space/repeated-command/completion cases, main-scene/exterior route and Continue. Then continue missing family and whole-set master fidelity/polish.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();data=json.loads(old);data['waterReorientReview']={'version':343,'file':str((out/'review.json').relative_to(r)),'checks':19585,'failures':0,'samples':816,'rows':288,'normalChanged':False};assert ledger.read_bytes()==old;ledger.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print('V343:19585new checks0;three regression probes0;816changed-heading resumes/288rows;five guides updated;staged only.')
