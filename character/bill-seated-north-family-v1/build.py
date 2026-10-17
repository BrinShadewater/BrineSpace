from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
def main():
 bindings={};counts={}
 for gear in ['bare','helmet']:
  folder=P.parent/('bill-seated-north-coherent-v1' if gear=='bare' else 'bill-seated-helmet-north-coherent-v1')
  inputs=[(folder,'manifest.json'),(P.parent/'bill-seated-idle-north-v1',gear+'-manifest.json'),(P.parent/'bill-reading-north-v1',gear+'-manifest.json'),(P.parent/'bill-reading-entry-north-v1',gear+'-manifest.json')];states=[]
  for pack,name in inputs:
   source=pack/name;bindings[source.relative_to(ROOT).as_posix()]=hashlib.sha256(source.read_bytes()).hexdigest()
   for state in json.loads(source.read_text(encoding='utf-8'))['states']:
    state['frameFiles']=['res://'+(pack/file).relative_to(ROOT).as_posix() for file in state['frameFiles']]
    for file in state['frameFiles']:bindings[file]=hashlib.sha256((ROOT/file.removeprefix('res://')).read_bytes()).hexdigest()
    states.append(state)
  m={'name':'Bill selected north sitting '+gear,'frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'selected_runtime','states':states}
  if gear=='helmet':m['equipment']='diving-helmet'
  (P/(gear+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8');counts[gear]={'states':len(states),'frameRefs':sum(len(s['frameFiles']) for s in states)}
 (P/'source-bindings.json').write_text(json.dumps({'counts':counts,'sha256':bindings},indent=2)+'\n',encoding='utf-8');print('Consolidated north sitting/reading:12gear states/72refs;whole literal res paths')
if __name__=='__main__':main()
