from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent
DIRECTIONS=['east','west','north','south']
def main():
 bindings={};counts={}
 for gear in ['bare','helmet']:
  states=[]
  for direction in DIRECTIONS:
   folder=P.parent/(f'bill-recover-air-{direction}-coherent-v1' if gear=='bare' else f'bill-recover-air-helmet-{direction}-coherent-v1')
   m=json.loads((folder/'manifest.json').read_text(encoding='utf-8'));state=m['states'][0]
   assert state['id']=='recover-air-'+direction
   state['frameFiles']=['res://'+(folder/f).relative_to(P.parent.parent).as_posix() for f in state['frameFiles']]
   states.append(state)
   bindings[folder.relative_to(P.parent.parent).as_posix()+'/manifest.json']=hashlib.sha256((folder/'manifest.json').read_bytes()).hexdigest()
   for f in state['frameFiles']:bindings[f]=hashlib.sha256((P.parent.parent/f.removeprefix('res://')).read_bytes()).hexdigest()
  m={'name':f'Bill cardinal dry recovery {gear} selected family','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'installed_runtime_reviewed','states':states}
  if gear=='helmet':m['equipment']='diving-helmet'
  (P/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8');counts[gear]={'states':len(states),'frameRefs':sum(len(s['frameFiles']) for s in states)}
 (P/'source-bindings.json').write_text(json.dumps({'counts':counts,'sha256':bindings},indent=2)+'\n',encoding='utf-8')
 print('Selected recovery family:8 gear states/48 refs;whole literal res paths')
if __name__=='__main__':main()
