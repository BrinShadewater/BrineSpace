from pathlib import Path
import copy,json,hashlib,shutil
P=Path(__file__).resolve().parent;R=P.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
records=[];sources={}
for gear,folder in [('bare','krusher-james-cyan-test-v2'),('helmet','krusher-james-helmet-fit-v2')]:
 source=R/'character'/folder;mp=source/'manifest.json';m=json.loads(mp.read_text());sources[mp.relative_to(R).as_posix()]=sha(mp)
 m['name']='Krusher Dom';m['status']='James utility suit selected by owner; locomotion candidate';m['identity']={'name':'Krusher Dom','title':'System Administrator','department':'AI & Robotics','accentTarget':'#527C80','baseFamily':'James / Branforth'}
 for state in m['states']:
  original_files=state['frameFiles'];new=[]
  for relative in original_files:
   src=source/relative;target='frames/'+gear+'/'+state['id']+'/'+Path(relative).name;dst=P/target;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst);new.append(target)
   records.append({'file':target,'source':src.relative_to(R).as_posix(),'sha256':sha(src)})
  state['frameFiles']=new
 (P/(gear+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
(P/'sources').mkdir(exist_ok=True);(P/'review').mkdir(exist_ok=True)
for direction in ['south','east','north','west']:
 src=R/'character/krusher-bill-base-test-v2/sources'/f'{direction}-head-native.png';dst=P/'sources'/src.name;shutil.copyfile(src,dst);sources[src.relative_to(R).as_posix()]=sha(src)
for source,dest in [('character/krusher-james-helmet-fit-v2/review/cardinal-comparison.png','character-sheet.png'),('character/krusher-james-helmet-fit-v2/review/motion-preview.mp4','locomotion-preview.mp4')]:
 src=R/source;shutil.copyfile(src,P/'review'/dest);sources[source]=sha(src)
provenance={'ownerDecision':{'date':'2026-10-03','quote':'James utility suit','scope':'Canonical base selection for Krusher Dom; no final artistic acceptance or game selector change inferred'},'sourceHashes':sources,'frames':records,'identity':m['identity'],'scope':'Frozen selected James utility suit derivative, eight idle/walk states per gear; original source gait and body pixels retained'}
(P/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n',encoding='utf-8');print(json.dumps({'copiedFrames':len(records),'statesPerGear':8}))
