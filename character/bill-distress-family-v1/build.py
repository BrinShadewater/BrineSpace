"""Aggregate reviewed directional poses; preserve source frames and exact joins."""
from pathlib import Path
import copy,json,hashlib
from PIL import Image
HERE=Path(__file__).resolve().parent
DIRS=['east','west','north','south']
def main():
 for gear in ['bare','helmet']:
  states=[];hashes={}
  for direction in DIRS:
   folder=HERE.parent/('bill-swim-distress-'+('helmet-' if gear=='helmet' else '')+direction+'-coherent-v1')
   p=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
   state=copy.deepcopy(p['states'][0]);state['frameFiles']=['../'+folder.name+'/'+f for f in state['frameFiles']];states.append(state)
   for file in state['frameFiles']:hashes[file]=hashlib.sha256((HERE/file).read_bytes()).hexdigest()
  manifest={'name':'Bill four-direction distress '+gear,'frameWidth':256,'frameHeight':256,'pivot':[128,128],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'installed_runtime_reviewed','states':states}
  if gear=='helmet':manifest['equipment']='diving-helmet'
  (HERE/f'{gear}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8');(HERE/f'{gear}-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n',encoding='utf-8')
  board=Image.new('RGB',(1536,1024),(29,43,51))
  for row,state in enumerate(states):
   for col,file in enumerate(state['frameFiles']):im=Image.open(HERE/file).convert('RGBA');board.paste(im,(col*256,row*256),im)
  board.save(HERE/f'{gear}-contact.png')
 print('Built four-direction paired distress manifests; all source folders remain load-bearing')
if __name__=='__main__':main()
