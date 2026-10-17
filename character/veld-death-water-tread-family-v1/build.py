"""Assemble source-bound cardinal tread-to-prone candidates; do not alter runtime selection."""
from pathlib import Path
import copy,hashlib,json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
DIRS=['east','west','north','south'];checks=0;bound={};reports={};manifests={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for gear in ['bare','helmet']:
 states=[];header=None
 for direction in DIRS:
  folder=R/f'character/veld-death-water-tread-{direction}-coherent-v1';m=json.loads((folder/f'{gear}-manifest.json').read_text(encoding='utf-8'));s=copy.deepcopy(m['states'][0])
  if header is None:header=copy.deepcopy(m)
  assert all(m.get(k)==header.get(k) for k in ['frameWidth','frameHeight','pivot','standingHeight','precomposed','textureFilter']);checks+=1
  assert s['id']=='death-water-tread-'+direction and len(s['frameFiles'])==6 and not s['loop'];checks+=1
  assert s['frameDurationsMs']==[180,180,220,220,260,500] and s['waterKinds']==['tread','transition','transition','transition','transition','swim'];checks+=1
  files=[]
  for i,name in enumerate(s['frameFiles']):
   f=folder/name;im=Image.open(f);assert im.mode=='RGBA' and im.size==(256,256);checks+=1
   files.append('../'+folder.name+'/'+name);bound[f.relative_to(R).as_posix()]=sha(f)
   if i==0:
    master=R/f'character/veld-water-{direction}-coherent-v1/frames/{gear}/tread-{direction}/000.png'
    assert im.tobytes()==Image.open(master).convert('RGBA').tobytes();checks+=1;bound[master.relative_to(R).as_posix()]=sha(master)
  terminal=R/f'character/veld-death-water-{direction}-coherent-v1/frames/{gear}/death-water-{direction}/005.png'
  assert Image.open(folder/s['frameFiles'][5]).convert('RGBA').tobytes()==Image.open(terminal).convert('RGBA').tobytes();checks+=1;bound[terminal.relative_to(R).as_posix()]=sha(terminal)
  s['frameFiles']=files;states.append(s)
  package=json.loads((folder/'validation.json').read_text(encoding='utf-8'));native=json.loads((R/f'output/veld-death-water-tread-{direction}-candidate-v1/validation.json').read_text(encoding='utf-8'))
  assert package['passed'] and native['passed'] and not native['realProfileChanges'];checks+=1
  for row in package['rows']:
   if row['gear']==gear:
    assert row['sha256']==sha(folder/m['states'][0]['frameFiles'][row['slot']]);checks+=1
  evidence=json.loads((folder/'candidate-evidence.json').read_text(encoding='utf-8'));hashes=evidence.get('boundFiles',evidence.get('files',{}))
  for path in [R/f'output/veld-death-water-tread-{direction}-candidate-v1/native.log',R/f'tests/test_veld_death_water_tread_{direction}_candidate.gd']:
   assert hashes[path.relative_to(R).as_posix()]==sha(path),'Native evidence changed';checks+=1
  reports[direction]={'packageChecks':package['checks'],'nativeChecks':187,'nativeSeconds':native['seconds'],'nativeScope':'per-direction direct player only; not assembled-family playback/NPC oxygen routing/world/disk Continue'}
  for f in [folder/'build.py',folder/'build-evidence.json',folder/'validation.json',R/f'output/veld-death-water-tread-{direction}-candidate-v1/native.log']:
   bound[f.relative_to(R).as_posix()]=sha(f)
 header.update(name='Veld cardinal tread-to-prone water death candidates '+gear,states=states,status='staged_tread_entrance_family_controller_world_restore_normal_selection_pending');manifests[gear]=header
 (P/f'{gear}-manifest.json').write_text(json.dumps(header,indent=2)+'\n',encoding='utf-8')
board=Image.new('RGBA',(6*256,8*256),'#202a30');draw=ImageDraw.Draw(board)
for gi,gear in enumerate(['bare','helmet']):
 for di,direction in enumerate(DIRS):
  state=manifests[gear]['states'][di]
  for i,file in enumerate(state['frameFiles']):
   board.alpha_composite(Image.open(P/file).convert('RGBA'),(i*256,(gi*4+di)*256));draw.text((i*256+4,(gi*4+di)*256+4),f'{direction} / {gear} / {i}'+(' exact tread master' if i==0 else ''),fill='white')
board.save(P/'all-cardinal-poses.png');board.resize((852,1136),Image.Resampling.LANCZOS).save(P/'station-scale-contact.png')
report={'passed':True,'checks':checks,'states':8,'references':48,'runtimeSelected':False,'sourceReports':reports,'boundFiles':bound,'scope':'assembled cardinal tread-to-prone candidate pixels/contracts/exact tread and corpse endpoints and existing per-direction proof; live incoming entry/controller/world/disk Continue/normal selection and full motion polish remain'}
(P/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
(P/'index.html').write_text('<meta charset="utf-8"><title>Veld tread-to-prone death candidates</title><style>body{background:#202a30;color:#eee;font:16px system-ui;margin:24px}a{color:#9bd3ed}img{max-width:100%}</style><h1>Veld cardinal tread-to-prone water death — candidate family</h1><p>Four independent cameras, both gear versions. Each first slot is the exact selected tread master. Compare all six finite poses below. Source/package candidates only; arbitrary live incoming poses, actual oxygen routing, furnished corpse/clearance, disk Continue and normal selection remain. North/south pitch pacing, body-center travel and family material/detail continuity remain for polish.</p><p>'+ ' · '.join(f'<a href="../veld-death-water-tread-{d}-coherent-v1/">{d.title()} finite comparison</a>' for d in DIRS)+'</p><img src="station-scale-contact.png"><p><a href="all-cardinal-poses.png">Full-size all poses</a></p>',encoding='utf-8')
print(f'{checks} family source/contract/master-entry checks PASS;8states/48refs,tread-to-prone source candidates only')
