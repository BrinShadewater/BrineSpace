from pathlib import Path
import ast,json,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
audit=ROOT/'character/bill-west-master-head-audit-v1'
inputs=json.loads((audit/'review.json').read_text())['inputSHA256']
for p,h in inputs.items():assert sha(ROOT/p)==h,p
motion=json.loads((OUT/'motion-review.json').read_text())
for p,h in motion['frozenInputs'].items():assert sha(Path(p))==h,p
survey=json.loads((OUT/'head-survey.json').read_text())
for p,h in survey['inputs'].items():assert sha(Path(p))==h,p
detail=json.loads((OUT/'detail-family-review.json').read_text())
for p,h in detail['frozenInputs'].items():assert sha(Path(p))==h,p
family=json.loads((OUT/'family-review.json').read_text()) if (OUT/'family-review.json').exists() else None
if family:
 for p,h in family['frozenInputs'].items():assert sha(Path(p))==h,p
methodPath=OUT/'shared-to-single-review.json'
method=json.loads(methodPath.read_text()) if methodPath.exists() else None
if method:
 for p,h in method['inputs'].items():assert sha(Path(p))==h,p
materialPath=OUT/'cropped-master-detail-review.json'
material=json.loads(materialPath.read_text()) if materialPath.exists() else None
if material:
 for p,h in material['inputs'].items():assert sha(Path(p))==h,p
preferred=json.loads((OUT/'review.json').read_text())['poses']
coverage=json.loads((OUT/'detail-pass-coverage.json').read_text())
assert coverage['reviewSha256']==sha(OUT/'review.json')
assert len(coverage['phases'])==48
for phase in coverage['phases'].values():assert sha(Path(phase['receiptPath']))==phase['receiptSha256']
for pose in preferred:
 if pose['key'].startswith('bare-walk-'):assert coverage['phases'][pose['key']]['revision']==pose['revision']
for q in preferred:assert q['opaquePixelsOutsideOriginalCanvas']==0,q['key']
freeze=json.loads((ROOT/'character/bill-walk-west-master-repair-v2/selected-gait-freeze.json').read_text())
for p,h in freeze.items():assert sha(ROOT/p)==h,p
receipts=list(OUT.glob('generation-provenance-*.json'))
for p in receipts:
 q=json.loads(p.read_text());assert q['method']=='builtin imagegen'
 assert sha(Path(q['sourcePath']))==q['sourceSha256']
 assert sha(Path(q['promptFile']))==q['promptSha256']==q['submittedPromptSha256']
 assert sha(Path(q['savedPath']))==q['sha256']==sha(Path(q['originalPath']))
 for ref in q['references']:assert sha(Path(ref['path']))==ref['sha256']
 if q.get('supportOriginalPath'):
  from PIL import Image
  originalSupport=Path(q['supportOriginalPath'])
  assert sha(originalSupport)==q['supportOriginalSha256']
  cropped=Image.open(originalSupport).crop(tuple(q['supportCrop'])).convert('RGBA')
  savedSupport=Image.open(q['references'][1]['path']).convert('RGBA')
  if q.get('supportResampledSize'):
   assert q['supportResampling']=='BICUBIC'
   assert q['supportPhysicalScale']==q['standingRuler']/956*4
   assert q['supportResampledSize']==[round(cropped.width*q['supportPhysicalScale']),round(cropped.height*q['supportPhysicalScale'])]
   resized=cropped.resize(tuple(q['supportResampledSize']),Image.Resampling.BICUBIC)
   cropped=Image.new('RGBA',tuple(q['supportCanvasSize']))
   cropped.alpha_composite(resized,tuple(q['supportPastePoint']))
  assert cropped.size==savedSupport.size and cropped.tobytes()==savedSupport.tobytes()
 if q.get('derivedSheetPose'):assert sha(Path(q['sharedProvenancePath']))==q['sharedProvenanceSha256']
scripts=list(OUT.glob('*.py'))+list(audit.glob('*.py'))
for p in scripts:ast.parse(p.read_text(encoding='utf-8'))
pngs=sorted([*OUT.rglob('*.png'),*audit.rglob('*.png')])
names=[p.relative_to(ROOT).as_posix() for p in pngs]
attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],cwd=ROOT,input=('\0'.join(names)+'\0').encode(),capture_output=True,check=True).stdout.decode().split('\0')
assert all(attrs[i+2]=='lfs' for i in range(0,len(attrs)-1,3))
report={'generationReceipts':len({json.loads(p.read_text())['generationId'] for p in receipts}),'poseReceiptFiles':len(receipts),'derivedSharedSheetPoseReceipts':sum(bool(json.loads(p.read_text()).get('derivedSheetPose')) for p in receipts),'rejectedReceipts':sum(bool(json.loads(p.read_text()).get('rejected')) for p in receipts),'masterAuditInputsUnchanged':len(inputs),'motionInputsUnchanged':len(motion['frozenInputs']),'headSurveyInputsUnchanged':len(survey['inputs']),'detailInputsUnchanged':len(detail['frozenInputs']),'familyInputsUnchanged':len(family['frozenInputs']) if family else None,'selectedGaitInputsUnchanged':len(freeze),'pythonSyntaxChecks':len(scripts),'pngLfsChecks':len(pngs),'decodedApngFramesExact':motion['decodedFramesExact'],'nativeRunThisMilestone':False,'normalAdmission':False,'fullVisualAcceptance':False}
report['sharedComparisonInputsUnchanged']=len(method['inputs']) if method else None
report['materialComparisonInputsUnchanged']=len(material['inputs']) if material else None
report['detailCoverageReceiptHashesUnchanged']=len(coverage['phases'])
report['croppedMasterDetailPhases']=coverage['croppedMasterDetailCount']
report['restrainedSleeveCollarPhases']=coverage['restrainedSleeveCollarCount']
report['faceInteriorDefinitionPhases']=coverage['faceInteriorDefinitionCount']
report['singleTargetFaceDefinitionPhases']=coverage['singleTargetFaceDefinitionCount']
report['commonCanvasFaceDefinitionPhases']=coverage['commonCanvasFaceDefinitionCount']
report['preferredWalkingSharedSheetPoses']=sum(bool(json.loads((OUT/f"generation-provenance-{q['key']}-v{q['revision']}.json").read_text()).get('derivedSheetPose')) for q in preferred if q['key'].startswith('bare-walk-'))
(OUT/'milestone-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
