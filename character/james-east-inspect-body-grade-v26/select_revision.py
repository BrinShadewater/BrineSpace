from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1];old='james-tablet-east-matte-v3';new=p.name
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
inputs=json.loads((p/'loader-inputs.json').read_bytes());assert all(sha(r/f)==v for f,v in inputs['preLaunchSha256'].items())
proof=json.loads((p/'validate-validation.json').read_bytes());assert proof['exitCode']==0 and proof['realProfileUnchanged']
review=json.loads((p/'package-review.json').read_bytes());review.update(visualReviewPending=False,reviewedSourceBoards=10,reviewedComparisonBoards=2,reviewedNativeCaptures=4,
    sourceAcceptance=True,findings=['All282 revised sources and two master/current/candidate comparison boards reviewed. Neutral hair/body chroma improved, original shading/poses/equipment retained.',
    'Four staged native paired captures reviewed at148/82/54/27 rulers. No continuous visual cadence or room/Continue acceptance inferred.'])
(p/'package-review.json').write_text(json.dumps(review,indent=2)+'\n')
archive=p/'before-selection';archive.mkdir(exist_ok=True);changes=[]
for rel in ['scripts/grid_canvas.gd','character/ACTIVE_ASSETS.json']:
 f=r/rel;before=f.read_bytes();after=before
 for mode in ['bare','helmet']:
  a=(old+'/'+mode+'-manifest.json').encode();b=(new+'/'+mode+'-manifest.json').encode();assert before.count(a)==1
  after=after.replace(a,b)
 saved=archive/f.name;assert not saved.exists();saved.write_bytes(before)
 temp=f.with_name(f.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(after)
 try:assert f.read_bytes()==before;os.replace(temp,f)
 finally:
  if temp.exists():temp.unlink()
 changes.append(dict(path=rel,before=hashlib.sha256(before).hexdigest(),after=sha(f)))
for mode in ['bare','helmet']:
 f=p/(mode+'-manifest.json');before=f.read_bytes();(archive/f.name).write_bytes(before);data=json.loads(before);data['status']='selected_source_reviewed_normal_validation_pending'
 f.write_text(json.dumps(data,indent=2)+'\n');changes.append(dict(path=f.relative_to(r).as_posix(),before=hashlib.sha256(before).hexdigest(),after=sha(f)))
template=r/'character/james-tablet-east-matte-v3/validate.gd'
code=template.read_text().replace(old,new).replace('validate.gd.uid','validate-selected.gd.uid').replace('validate-evidence.json','validate-selected-evidence.json')
(p/'validate-selected.gd').write_text(code,encoding='utf-8')
route=(r/'character/james-tablet-east-matte-v3/native-arrival-continue.gd').read_text().replace(old,new)
(p/'native-arrival-continue.gd').write_text(route,encoding='utf-8')
files=[Path(__file__),p/'validate-selected.gd',p/'native-arrival-continue.gd',r/'scripts/grid_canvas.gd',r/'character/ACTIVE_ASSETS.json']+[p/(m+'-manifest.json') for m in ['bare','helmet']]
(p/'selected-inputs.json').write_text(json.dumps(dict(preLaunchSha256={f.relative_to(r).as_posix():sha(f) for f in files}),indent=2)+'\n')
(p/'selection-evidence.json').write_text(json.dumps(dict(changes=changes,selected=True,sourceBoardsReviewed=10,comparisonBoardsReviewed=2,nativeCapturesReviewed=4,stagedChecks=2357,routeContinuePending=True),indent=2)+'\n')
print('Selected paired East body-color revision; exact loader/registry paths updated. Normal validation and route/Continue pending.')
