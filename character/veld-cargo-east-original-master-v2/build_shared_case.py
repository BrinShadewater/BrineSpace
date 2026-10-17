from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
P=Path(__file__).resolve().parent;R=P.parents[1]
reg=json.loads((P/'contact-registration.json').read_text(encoding='utf-8'));scale=reg['sourceScale']
def whole_component(im):
 a=np.array(im.convert('RGBA'));labels,n=ndimage.label(a[:,:,3]>200);counts=np.bincount(labels.ravel());counts[0]=0;k=int(counts.argmax());a[~ndimage.binary_dilation(labels==k,iterations=3)]=0;return Image.fromarray(a)
raw=Image.open(P/'raw-unload-v4.png').convert('RGBA');case=whole_component(Image.open(P/'whole-floor-case-reference.png')).resize((round(104*scale),round(88*scale)),Image.Resampling.LANCZOS)
ca=np.array(case);cy,cx=np.where(ca[:,:,3]>200);case_pos=(151-int(cx.min()),223-int(cy.max()));case.save(P/'shared-floor-case.png')
deep=whole_component(Image.open(P/'raw-deep-body-v1.png'));da=np.array(deep);dy,dx=np.where(da[:,:,3]>200);target_height=81;estimated=round(deep.height*target_height/(dy.max()-dy.min()+1))
for adj in [0,1,-1,2,-2,3,-3]:
 h=estimated+adj;ratio=h/deep.height;im=deep.resize((round(deep.width*ratio),h),Image.Resampling.LANCZOS);a=np.array(im);y,x=np.where(a[:,:,3]>200)
 if int(y.max()-y.min()+1)==target_height:break
else:raise AssertionError('independent complete deep source density')
# Foreground boot contact is measured separately from the far boot and hands.
bottom=int(y.max());ys,xs=np.where(a[max(0,bottom-2):bottom+1,:,3]>200);foreground=xs<round(im.width*.5);contact=float(xs[foreground].mean());deep_pos=(round(reg['originalHeldNearContactTarget'][0]-contact),223-bottom)
body=Image.new('RGBA',(256,256));body.alpha_composite(im,deep_pos)
bodies=[]
for i in range(6):
 if i==0:b=Image.open(R/'character/veld-east-held-original-master-v1/frames/bare/000.png').convert('RGBA')
 elif i==3:b=body.copy()
 elif i==5:
  b=Image.new('RGBA',(256,256));b.alpha_composite(Image.open(R/'character/veld-side-foundation-v1/east-standing.png').convert('RGBA'),(36,52))
 elif i==4:
  row=reg['rows'][i];cell=whole_component(raw.crop(tuple(row['sourceCell'])));cell=cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS);b=Image.new('RGBA',(256,256));b.alpha_composite(cell,tuple(row['offset']))
 else:b=Image.open(P/'atlas-contact-frames'/f'{i:03}.png').convert('RGBA')
 bodies.append(b)
shell=Image.open(R/'character/veld-helmet-original-turntable-v1/v3-study/shells/005.png').convert('RGBA');sa=np.array(shell);_,sx=np.where(sa[-4:,:,3]>160)
frames={'bare':[],'helmet':[]};audits=[];checks=0
for i,b in enumerate(bodies):
 a=np.array(b);y,x=np.where(a[:,:,3]>200);top=int(y.min());hx=np.where(a[top:top+16,:,3]>128)[1];pos=(round((hx.min()+hx.max())/2-(sx.min()+sx.max())/2),top+28-shell.height);clear=(int(hx.min())-3,top,int(hx.max())+4,top+27)
 equipped=b.copy();equipped.paste((0,0,0,0),clear);equipped.alpha_composite(shell,pos)
 mask=np.ones((256,256),bool);mask[min(top,pos[1]):max(clear[3],pos[1]+shell.height),min(pos[0],clear[0]):max(clear[2],pos[0]+shell.width)]=False
 assert np.array_equal(np.array(equipped)[mask],a[mask]);checks+=1
 if i==0:equipped=Image.open(R/'character/veld-east-held-original-master-v1/frames/helmet/000.png').convert('RGBA')
 for gear,char in [('bare',b),('helmet',equipped)]:
  out=Image.new('RGBA',(256,256))
  if i>=3:out.alpha_composite(case,case_pos)
  out.alpha_composite(char);path=P/f'frames/{gear}/{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);out.save(path);frames[gear].append('res://'+path.relative_to(R).as_posix())
  z=np.array(out);assert not np.any(np.concatenate([z[0,:,3],z[-1,:,3],z[:,0,3],z[:,-1,3]])>20);checks+=1
 audits.append({'pose':i,'bodyHeight':int(y.max()-y.min()+1),'headWidth':int(hx.max()-hx.min()+1),'helmetPosition':list(pos),'helmetBodyProtected':True,'floorCase':i>=3})
durations=[70,90,100,100,90,70]
for gear in frames:
 m=json.loads((R/f'character/veld-east-held-original-master-v1/{gear}-manifest.json').read_text(encoding='utf-8'));template=m['states'][0];states=[]
 for name,ids,ds,loop in [('carry-east',[0],[1000],True),('unload-east',list(range(6)),durations,False),('pickup-east',list(reversed(range(6))),list(reversed(durations)),False),('idle-east',[5],[1000],True)]:
  state=copy.deepcopy(template);state.update(id=name,frameCount=len(ids),frameFiles=[frames[gear][i] for i in ids],frameDurationsMs=ds,loop=loop)
  for key,value in [('facings','east'),('waterKinds','idle'),('waterPoses',False),('depthOffsets',0.0)]:state[key]=[value]*len(ids)
  states.append(state)
 m.update(name='Veld original East cargo shared case '+gear,status='staged_not_installed',states=states);(P/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
board=Image.new('RGB',(1536,600),'#202a30');draw=ImageDraw.Draw(board)
for row,gear in enumerate(frames):
 for i in range(6):
  frame=Image.open(P/f'frames/{gear}/{i:03}.png');board.paste(frame,(i*256,row*290+20),frame);draw.text((i*256+5,row*290+3),f'{gear} {i}',fill='white')
board.save(P/'shared-case-paired-review.png')
out={'checks':checks,'failures':0,'independentDeepBody':{'generation':'618c45fd-b7bd-47b4-8891-b63a394b61c6','height':target_height,'uniformScale':ratio,'offset':deep_pos},'sharedCompleteCase':{'size':list(case.size),'position':case_pos,'opaqueBounds':[int(cx.min()),int(cy.min()),int(cx.max()+1),int(cy.max()+1)],'sharedPhases':[3,4,5],'groundY':223},'rows':audits,'scope':'Whole-source extraction/uniform registration and complete equipment reuse. No body-region/RGB edits. Source pilot; native/temporal/final artistic acceptance unproven.'}
(P/'shared-case-registration.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out))
