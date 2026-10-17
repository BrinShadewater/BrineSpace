"""Whole four-quarter identity plus shared current cardinal joins; full motion polish remains."""
from pathlib import Path
import json,copy,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
I=R/'character/bill-selected-source-audit-2026-10-01-locomotion-v12/source-inventory.json';audit=json.loads(I.read_text());quarters=['east-south','south-west','west-north','north-east'];routes=[['east','south','west'],['south','west','north'],['west','north','east'],['north','east','south']];records=[]
for gear in ['bare','helmet']:
 states=[];lookup={};original=json.loads((R/audit['selectedStateSources'][gear]['carry-turn-west-north']['manifest']).read_text());manifest={k:v for k,v in original.items() if k!='states'};manifest.update(name='Bill carry-turn current endpoint/native four-quarter identity matrix',status='selected_runtime',states=[])
 for pair in quarters:
  key='carry-turn-'+pair;ref=audit['selectedStateSources'][gear][key];st=copy.deepcopy(next(s for s in original['states'] if s['id']==key));source=ref['sourceFiles'][:]
  if pair in ['west-north','east-south','south-west','north-east']:
   new=json.loads((P.parent/('bill-carry-turn-'+pair+'-identity-v2')/('bare-manifest.json' if gear=='bare' else 'helmet-manifest.json')).read_text());source=next(s for s in new['states'] if s['id']==key)['frameFiles'][:]
  dirs=pair.split('-');source[0]=audit['selectedStateSources'][gear]['pickup-'+dirs[0]]['sourceFiles'][-1];source[-1]=audit['selectedStateSources'][gear]['pickup-'+dirs[1]]['sourceFiles'][-1]
  st['frameFiles']=source;st['provenance']='Current exact static-held cardinal joins;All four quarter paths use newly authored head/shell fits;full motion polish remains';lookup[key]=st;states.append(st)
  reverse='carry-turn-'+dirs[1]+'-'+dirs[0];back=copy.deepcopy(next(s for s in original['states'] if s['id']==reverse));back['frameFiles']=source[::-1];back['provenance']=st['provenance']+';reverse derived without mirror';lookup[reverse]=back;states.append(back)
 for route in routes:
  first=lookup['carry-turn-'+'-'.join(route[:2])];second=lookup['carry-turn-'+'-'.join(route[1:])];assert first['frameFiles'][-1]==second['frameFiles'][0]
  key='carry-turn-'+route[0]+'-'+route[2];st=copy.deepcopy(next(s for s in original['states'] if s['id']==key));st['frameFiles']=first['frameFiles']+second['frameFiles'][1:];st['provenance']='Two existing clockwise quarter paths;shared current static-held midpoint;original1600ms clock and facing metadata';states.append(st)
 manifest['states']=states;(P/('bare-manifest.json' if gear=='bare' else 'helmet-manifest.json')).write_text(json.dumps(manifest,indent=2)+'\n')
 for st in states:
  records.append({'gear':gear,'state':st['id'],'sourceFiles':st['frameFiles'],'sourceSha256':[hashlib.sha256((R/f[6:]).read_bytes()).hexdigest() for f in st['frameFiles']]})
(P/'bindings.json').write_text(json.dumps({'inventory':I.relative_to(R).as_posix(),'inventorySha256':hashlib.sha256(I.read_bytes()).hexdigest(),'rows':records,'remainingIdentityQuarters':[],'fullGoalComplete':False},indent=2)+'\n')
board=Image.new('RGB',(1536,2048),(34,52,62));dr=ImageDraw.Draw(board)
for row,(gear,pair) in enumerate((g,p) for g in ['bare','helmet'] for p in quarters):
 m=json.loads((P/('bare-manifest.json' if gear=='bare' else 'helmet-manifest.json')).read_text());st=next(s for s in m['states'] if s['id']=='carry-turn-'+pair)
 for i,f in enumerate(st['frameFiles']):
  im=Image.open(R/f[6:]).convert('RGBA');board.paste(im,(i*256,row*256),im);dr.text((i*256+3,row*256+3),gear+' '+pair+' '+str(i),fill='white')
board.save(P/'quarter-review.png');print('Paired24states/184references;48current joins locked;all four quarter head identities revised;full motion review remains')
