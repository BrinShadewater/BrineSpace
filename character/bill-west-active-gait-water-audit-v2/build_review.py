from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
old=json.loads((ROOT/'character/bill-west-active-gait-water-audit-v1/review.json').read_text())
bare=ROOT/'character/bill-walk-west-master-repair-v2';helmet=ROOT/'character/bill-walk-west-helmet-master-repair-v1'
ba=json.loads((bare/'bank-assessment.json').read_text());ha=json.loads((helmet/'bank-assessment.json').read_text());assert len(ba['poses'])==ha['authoredHelmetStudies']==48
barepaths={v['frame']:bare/v['study'] for v in ba['poses']};hashes={};boards=[]
def read(p):
 hashes[p.relative_to(ROOT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest();return Image.open(p).convert('RGBA')
def gait(gear,n,candidate):
 p=(barepaths[n] if gear=='bare' else helmet/f'canvas-normalized-study-{n:03}.png') if candidate else ROOT/f'character/bill-walk-west-material-v1/frames/{gear}/walk-west/{n:03}.png'
 im=read(p);assert im.size==(256,256);c=Image.new('RGBA',(352,320));c.alpha_composite(im,(32,0));return c
def water(bank,state,gear,n):
 path=OUT/f'{gear}-neutral-candidate.png' if (bank=='bill-land-water-west-v15' and n==0) or (bank=='bill-water-exit-west-master-v13' and n==7) else ROOT/f'character/{bank}/{gear}/frames/{state}/{n:03}.png'
 im=read(path);assert im.size==(352,320);return im
master=read(ROOT/'character/bill-water-exit-west-master-v8/sources/master-west-reference.png');master=master.resize((round(master.width*148/956),round(master.height*148/956)),Image.Resampling.LANCZOS);mc=Image.new('RGBA',(352,320));mc.alpha_composite(master,(160-master.width//2,224-master.height))
for gear in ['bare','helmet']:
 entry=old['actualNativeTickMatches'][gear+'67'];exitn=old['actualNativeTickMatches'][gear+'444'];resume=old['actualNativeTickMatches'][gear+'445']
 groups={'entry':[('Original master',mc),('Selected outgoing walk '+str(entry),gait(gear,entry,False)),('Candidate outgoing walk '+str(entry),gait(gear,entry,True)),('Revised entry neutral',water('bill-land-water-west-v15','land-swim-west',gear,0)),('Entry ready',water('bill-land-water-west-v15','land-swim-west',gear,1)),('Entry crouch',water('bill-land-water-west-v15','land-swim-west',gear,2))],
 'exit':[('Original master',mc),('Water rise',water('bill-water-exit-west-master-v13','swim-land-west',gear,6)),('Revised water final',water('bill-water-exit-west-master-v13','swim-land-west',gear,7)),('Selected resumed '+str(exitn),gait(gear,exitn,False)),('Candidate resumed '+str(exitn),gait(gear,exitn,True)),('Candidate next '+str(resume),gait(gear,resume,True))]}
 for kind,items in groups.items():
  b=Image.new('RGB',(2112,760),(23,42,51));d=ImageDraw.Draw(b)
  for i,(name,im) in enumerate(items):
   d.text((352*i+6,8),gear+' / '+name,fill='white');b.paste(im,(352*i,30),im);crop=im.crop((120,55,190,145)).resize((210,270),Image.Resampling.NEAREST);b.paste(crop,(352*i+70,410),crop)
  name=f'{gear}-{kind}-candidate-join.png';b.save(OUT/name);boards.append(name)
report={'status':'source_candidate_water_join_audit_unselected','actualContextAuthority':'Existing V10 captured ticks matched exactly in active-gait auditV1; no new native observation','actualNativeTickMatches':old['actualNativeTickMatches'],'candidateBanks':{'bare':48,'helmet':48},'walkingTranslationToWaterCanvas':[32,0],'commonPivot':[160,224],'standingRuler':148,'inputSHA256':hashes,'boards':boards,'normalAdmission':False,'nativeAcceptance':False,'visualAcceptance':False,'scope':'Exact dry contexts compared with water candidates with revised shared neutral endpoints on common canvas, source review only; no body/part fitting or new game run.'}
(OUT/'review.json').write_text(json.dumps(report,indent=2)+'\n')
html='<!doctype html><meta charset="utf-8"><title>Bill West candidate water joins</title><style>body{background:#172a33;color:#d9e2e7;font:17px system-ui;margin:24px}img{max-width:100%}</style><h1>Bill West walk candidates and water joins</h1><p>Both dry source banks have48candidates. Exact previously captured walking contexts, common148pixel ruler and physical pivot. Source comparison only; normal-game acceptance pending.</p>'
for name in boards:html+=f'<h2>{name}</h2><img src="{name}">'

html+='<h2>Revised shared neutral endpoints</h2><p>Matte grade is closer. Face/collar identity and physical transition/contact remain provisional; helmet boots have a one-pixel sole/width difference.</p>'
for gear in ['bare','helmet']:html+=f'<h3>{gear} neutral comparison</h3><img src="{gear}-neutral-master-review.png">'
html+='<h2>Finite source sequences</h2><p>Original500ms timing and26unchanged interior frames; source playback only. Reload to replay.</p>'
for kind in ['entry','exit']:
 for gear in ['bare','helmet']:html+=f'<h3>{gear} {kind}</h3><img src="staged-{kind}/{gear}/source-preview.png" style="width:352px">'
(OUT/'index.html').write_text(html);print(json.dumps({'boards':boards,'inputs':len(hashes),'normalAdmission':False}))
