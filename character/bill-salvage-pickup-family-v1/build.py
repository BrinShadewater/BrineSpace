"""Aggregate independently authored paired states without copying source frames."""
from pathlib import Path
import json,hashlib,copy
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
for gear in ['bare','helmet']:
 states=[];inputs=[];hashes={}
 for direction in ['east','west','north','south']:
  for action in ['salvage','swim-pickup']:
   folder=f'bill-{action}-{direction}-coherent-v1' if gear=='bare' else f'bill-{action}-helmet-{direction}-coherent-v1'
   # Existing salvage equipment folders use the same family naming convention.
   pack=P.parent/folder;m=json.loads((pack/'manifest.json').read_text(encoding='utf-8'));inputs.append({'folder':folder,'manifestSha256':hashlib.sha256((pack/'manifest.json').read_bytes()).hexdigest()})
   assert m['pivot']==[128,128] and m['standingHeight']==148
   for state in copy.deepcopy(m['states']):
    state['frameFiles']=['../'+folder+'/'+f for f in state['frameFiles']]
    for f in state['frameFiles']:hashes[f]=hashlib.sha256((P/f).read_bytes()).hexdigest()
    states.append(state)
 manifest={'name':f'Bill underwater work/pickup family {gear}','frameWidth':256,'frameHeight':256,'pivot':[128,128],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'installed_runtime_reviewed','states':states}
 if gear=='helmet':manifest['equipment']='diving-helmet'
 for name,data in [(gear+'-manifest.json',manifest),(gear+'-hashes.json',hashes),(gear+'-inputs.json',inputs)]:
  (P/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 for bg,name in [((29,43,51),'dark'),((218,225,224),'light')]:
  board=Image.new('RGB',(1024,1024),bg);d=ImageDraw.Draw(board)
  for row,direction in enumerate(['east','west','north','south']):
   pad={'east':(6,40),'west':(42,40),'north':(24,56),'south':(24,-24)}[direction]
   swim=f'bill-swim-{direction}-coherent-v1' if gear=='bare' else f'bill-swim-helmet-{direction}-coherent-v1'
   carry=f'bill-swim-carry-{direction}-coherent-v1' if gear=='bare' else f'bill-swim-carry-helmet-{direction}-coherent-v1'
   work=f'bill-salvage-{direction}-coherent-v1' if gear=='bare' else f'bill-salvage-helmet-{direction}-coherent-v1'
   pick=f'bill-swim-pickup-{direction}-coherent-v1' if gear=='bare' else f'bill-swim-pickup-helmet-{direction}-coherent-v1'
   for col,(folder,action,index,padding) in enumerate([(swim,'swim',0,pad),(work,'salvage',0,(0,0)),(pick,'swim-pickup',4,(0,0)),(carry,'swim-carry',0,pad)]):
    im=Image.new('RGBA',(256,256));im.alpha_composite(Image.open(P.parent/folder/'frames'/f'{action}-{direction}'/f'{index:03}.png').convert('RGBA'),padding)
    board.paste(im,(col*256,row*256),im);d.text((col*256+5,row*256+8),f'{direction} {action} {gear}',fill='white' if name=='dark' else 'black')
  board.save(P/f'{gear}-master-comparison-{name}.png')
print('Built paired four-direction family;8states/48refs per equipment mode')
