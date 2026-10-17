from pathlib import Path
import json, hashlib, os, uuid

p=Path(__file__).resolve().parent
r=p.parents[1]
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
proof=json.loads((p/'validate-validation.json').read_bytes())
assert proof['exitCode']==0 and proof['realProfileUnchanged']
native=json.loads((p/'validate-evidence.json').read_bytes())
assert native['failures']==0 and native['captures']==12
review=json.loads((p/'review-acceptance.json').read_bytes())
assert review['sourceBoardsReviewComplete'] and review['reviewedSourceFrames']==864
assert all(sha(r/f['path'])==f['sha256'] for f in review['reviewedBoards'])
package=json.loads((p/'package-review.json').read_bytes())
assert package['sourceFrames']==864
for row in package['records']:
    assert sha(r/row['source'].removeprefix('res://'))==row['sourceSha256']
    assert sha(r/row['candidate'].removeprefix('res://'))==row['candidateSha256']
archive=p/'before-selection'
archive.mkdir(exist_ok=True)
changes=[]
for rel in ['scripts/grid_canvas.gd','character/ACTIVE_ASSETS.json']:
    f=r/rel
    before=f.read_bytes()
    after=before
    for mode in ['bare','helmet']:
        a=('james-inspect-material-continuity-v1/'+mode+'-manifest.json').encode()
        b=(p.name+'/'+mode+'-manifest.json').encode()
        assert before.count(a)==1
        after=after.replace(a,b)
    for mode in ['bare','helmet']:
        east=('james-east-inspect-body-grade-v26/'+mode+'-manifest.json').encode()
        assert before.count(east)==1 and after.count(east)==1
    saved=archive/f.name
    assert not saved.exists()
    saved.write_bytes(before)
    temp=f.with_name(f.name+'.'+uuid.uuid4().hex+'.tmp')
    temp.write_bytes(after)
    try:
        assert f.read_bytes()==before
        os.replace(temp,f)
    finally:
        if temp.exists():temp.unlink()
    changes.append(dict(path=rel,before=hashlib.sha256(before).hexdigest(),after=sha(f)))
# Only normal loading supplies sources here: no fixture-only overrides.
src=(p/'validate.gd').read_text(encoding='utf-8')
start=src.index('    player.load_manifest(BODY,true)')
end=src.index('    var manifests := [BODY,HELMET]',start)
src=src[:start]+'    check(player.equipment_frames["diving-helmet"].has("inspect-north"),"Normal installed diagnostics")\n'+src[end:]
src=src.replace('validate.gd.uid','validate-selected.gd.uid').replace('validate-evidence.json','validate-selected-evidence.json')
src=src.replace('Staged South/North/West paired candidate on actual normal-loaded player;', 'Actual normal-loaded South/North/West paired selection without appended candidates;')
src=src.replace('Not normal adoption, room/route/Continue or uninterrupted motion acceptance.', 'Normal selection verified; not room/route/Continue or uninterrupted motion acceptance.')
(p/'validate-selected.gd').write_text(src,encoding='utf-8')
route=(r/'character/james-east-inspect-body-grade-v26/native-arrival-continue.gd').read_text(encoding='utf-8')
route=route.replace('james-east-inspect-body-grade-v26',p.name)
route=route.replace('(new141 East source poses per mode)','(East141/South141/West154/North137 poses per mode; edge-only South/North/West correction)')
(p/'native-arrival-continue.gd').write_text(route,encoding='utf-8')
evidence=dict(changes=changes,selected=True,stagedChecks=native['checks'],reviewedSourceFrames=864,reviewedSourceBoards=18,reviewedNativeCaptures=12,reviewedNativeBoards=3,normalValidationPending=True,routeContinuePending=True,fullGoalComplete=False)
(p/'selection-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
files=[r/c['path'] for c in changes]+[p/(m+'-manifest.json') for m in ['bare','helmet']]+[p/'validate-selected.gd',p/'native-arrival-continue.gd']
(p/'selected-inputs.json').write_text(json.dumps(dict(preLaunchSha256={f.relative_to(r).as_posix():sha(f) for f in files}),indent=2)+'\n')
print(json.dumps(dict(selected=True,changedNormalFiles=2,stagedChecks=native['checks'],normalValidationPending=True)))
