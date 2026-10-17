from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[2]
source=json.loads((P/'SOURCE_REVIEW.json').read_bytes());assert all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in source['bindings'].items())
inventory_path=R/'character/veld-master-consistency-current-v2/selected-library.json';inventory=json.loads(inventory_path.read_bytes());bindings=dict(source['bindings'])
shell_path=R/'character/veld-helmet-original-turntable-v1/v3-study/shells/000.png';shell=Image.open(shell_path).convert('RGBA')
def fitted(bare):
 im=bare.copy();im.paste((0,0,0,0),(115,77,143,103));im.alpha_composite(shell,(112,68));return im
for gear in ['bare','helmet']:
 data=json.loads((P/f'{gear}-source-manifest.json').read_bytes())
 first=data['states'][0];single=dict(first);single['id']='interact-north';single['frameCount']=78
 for key in ['frameFiles','frameDurationsMs','facings','waterKinds','waterPoses','depthOffsets']:single[key]=first[key][:78]
 data['states'].append(single)
 frames=[Image.open(R/ref[6:]).convert('RGBA') for ref in single['frameFiles']]
 frames[0].save(P/f'{gear}-single-action.png',save_all=True,append_images=frames[1:],duration=single['frameDurationsMs'],loop=1,disposal=0,blend=0)
 replay=Image.open(P/f'{gear}-single-action.png');assert replay.n_frames==78
 for i,im in enumerate(frames):replay.seek(i);assert np.array_equal(np.asarray(im),np.asarray(replay.convert('RGBA')));assert round(replay.info['duration'])==single['frameDurationsMs'][i]
 for name,filename in [('reference-north','original-idle-master.png'),('prepared-north','prepared-idle-master.png')]:
  im=Image.open(P/filename).convert('RGBA');im=im if gear=='bare' else fitted(im);dest=P/f'{gear}-{name}.png';im.save(dest)
  data['states'].append(dict(id=name,frameCount=1,frameFiles=['res://'+dest.relative_to(R).as_posix()],frameDurationsMs=[1000],loop=True))
 entry=inventory['resolved'][gear]['idle-north'];selected=R/entry['frameFiles'][0];assert hashlib.sha256(selected.read_bytes()).hexdigest()==inventory['sourceBindings'][entry['frameFiles'][0]]
 im=Image.open(selected).convert('RGBA');plate=Image.new('RGBA',(256,256));px,py=entry['pivot'];plate.alpha_composite(im,(128-round(px),224-round(py)));dest=P/f'{gear}-selected-idle.png';plate.save(dest)
 data['states'].append(dict(id='idle-north',frameCount=1,frameFiles=['res://'+dest.relative_to(R).as_posix()],frameDurationsMs=[1000],loop=True))
 path=P/f'{gear}-native-manifest.json';path.write_text(json.dumps(data,indent=2)+'\n')
 for state in data['states']:
  for ref in state['frameFiles']:
   p=R/ref[6:];bindings[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
 for p in [path,selected,R/entry['manifest']]:bindings[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
for p in [inventory_path,P/'prepare_native.py',P/'SOURCE_REVIEW.json',P/'generation.json']:
 bindings[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
(P/'full-source-record.json').write_text(json.dumps(dict(frameCount=142,durationMs=5917,bindings=bindings,scope='Complete source trial paired to original rear helmet and original/prepared/current selected idle references. Native appearance only; no motion/occlusion/adoption acceptance implied.'),indent=2)+'\n')
test=(R/'tests/test_veld_west_interact_source_v1.gd').read_text().replace('character/veld-interact-west-original-master-v1/original-action-video-v1/bare-source-manifest.json','character/veld-interact-north-original-master-v1/front-occluded-v2/bare-native-manifest.json').replace('character/veld-interact-west-original-master-v1/original-action-video-v1/helmet-source-manifest.json','character/veld-interact-north-original-master-v1/front-occluded-v2/helmet-native-manifest.json').replace('veld-west-interact-source','veld-north-interact-source').replace('source-interact-west','source-interact-north').replace('reference-west','reference-north').replace('idle-west','idle-north').replace('West scanner','North scanner').replace('VELD WEST INTERACT SOURCE','VELD NORTH INTERACT SOURCE')
# Four references remain at the same physical foot/ruler; add prepared source separately.
test=test.replace('var idle:Texture2D','var prepared:Texture2D\n var idle:Texture2D').replace('range(3):\n    var tex','range(4):\n    var tex').replace('[texture,master,idle]','[texture,master,prepared,idle]').replace('[230.0,430.0,630.0]','[170.0,330.0,490.0,650.0]').replace('for j in range(3):draw_string','for j in range(4):draw_string').replace('[155.0,355.0,555.0]','[110.0,270.0,430.0,590.0]').replace('["Scanner action","Original master","Selected idle"]','["Scanner action","Original master","Prepared source","Selected idle"]')
test=test.replace('view.master=player.frame_at_elapsed("reference-north",0,equipment);view.idle','view.master=player.frame_at_elapsed("reference-north",0,equipment);view.prepared=player.frame_at_elapsed("prepared-north",0,equipment);view.idle')
extra='''
  check(bank["interact-north"].size()==78,"All contiguous first complete interaction slots loaded")
  var single_elapsed:=0.0
  for i in range(78):
   var single_duration:float=float(manifest.states[1].frameDurationsMs[i])/1000.0
   check(player.frame_at_elapsed("interact-north",single_elapsed+single_duration*.5,equipment)==bank["source-interact-north"][i],"First full action retains every source pose and clock")
   single_elapsed+=single_duration
  check(absf(single_elapsed-3.25)<.0001,"Single contiguous action duration preserved")
  check(player.frame_at_elapsed("interact-north",4,equipment)==bank["source-interact-north"][77],"Single action holds completed rest without second cycle")
'''
test=test.replace(' var file:=FileAccess.open(OUT+"records.json"',extra+' var file:=FileAccess.open(OUT+"records.json"')
(R/'tests/test_veld_north_interact_source_v1.gd').write_text(test);(R/'tests/test_veld_north_interact_source_v1.gd.uid').write_text('uid://cveldnorthinteract1\n')
runner=(R/'tools/run_veld_west_interact_source_v1.py').read_text().replace('veld-west-interact-source','veld-north-interact-source').replace('character/veld-interact-west-original-master-v1/original-action-video-v1','character/veld-interact-north-original-master-v1/front-occluded-v2').replace('test_veld_west_interact_source_v1','test_veld_north_interact_source_v1').replace("P/'build_source_clip.py'","P/'prepare_native.py'").replace("P.glob('*-source-manifest.json')","P.glob('*-native-manifest.json')").replace('Complete paired West interaction','Complete paired North interaction')
(R/'tools/run_veld_north_interact_source_v1.py').write_text(runner)
review=(R/'character/veld-interact-west-original-master-v1/original-action-video-v1/review_native.py').read_text().replace('veld-west-interact-source','veld-north-interact-source').replace('West','North').replace('(145,395,310,570)','(85,395,250,570)')
(P/'review_native.py').write_text(review)
print('Complete North paired source/original/prepared/selected idle native review prepared')
