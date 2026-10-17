"""Register preserved probe art and export independent propulsion/scan layers."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
from scipy import ndimage
import numpy as np,json,math,hashlib
R=Path(__file__).resolve().parent;SIZE=512
ORDER=['east','southeast','south','southwest','west','northwest','north','northeast']
def save(im,path):
 p=R/path;p.parent.mkdir(parents=True,exist_ok=True);im.save(p);return path
def clean(im):
 a=np.array(im.convert('RGBA'));l,n=ndimage.label(a[:,:,3]>128);counts=np.bincount(l.ravel());counts[0]=0
 a[:,:,3]=np.where(ndimage.binary_dilation(l==counts.argmax(),iterations=2),a[:,:,3],0)
 im=Image.fromarray(a);return im.crop(im.getbbox())
def effect(h,kind,n):
 a=ORDER.index(h)*math.pi/4;u=np.array([math.cos(a),math.sin(a)]);v=np.array([-u[1],u[0]]);im=Image.new('RGBA',(SIZE,SIZE));d=ImageDraw.Draw(im);phase=n/60
 def p(x,y=0):return tuple(np.array([256,256])+u*x+v*y)
 if kind=='wake':
  for j in range(9):
   q=(phase+j/9)%1;x=-lengths[h]/2-8-q*85;y=math.sin(j*2.4+q*4)*q*15;r=1+q*2
   c=p(x,y);d.ellipse((c[0]-r,c[1]-r,c[0]+r,c[1]+r),outline=(126,177,191,round(130*(1-q))))
 if kind=='scan':
  origin=lengths[h]/2-8;radius=15+phase*110
  pts=[p(origin+radius*math.cos(t),radius*math.sin(t)) for t in np.linspace(-.48,.48,30)]
  d.line(pts,fill=(112,183,204,round(165*(1-phase))),width=2)
  for sign in [-1,1]:d.line([p(origin),p(origin+112*math.cos(.48),sign*112*math.sin(.48))],fill=(105,177,195,35),width=1)
  c=p(origin);d.ellipse((c[0]-3,c[1]-3,c[0]+3,c[1]+3),fill=(143,206,220,round(100+65*math.sin(phase*math.pi)**2)))
 return im
poses={};lengths={};headings={};diag=Image.open(R/'sources/diagonals-v1.png').convert('RGBA');cw,ch=diag.width//2,diag.height//2
cells={'northeast':(0,0),'southeast':(1,0),'southwest':(0,1),'northwest':(1,1)}
for h in ORDER:
 if h in cells:
  x,y=cells[h];raw=clean(diag.crop((x*cw,y*ch,(x+1)*cw,(y+1)*ch)));a=ORDER.index(h)*math.pi/4
  yy,xx=np.where(np.array(raw)[:,:,3]>128);proj=xx*math.cos(a)+yy*math.sin(a);target=math.hypot(240/math.sqrt(2),192/math.sqrt(2));scale=target/(proj.max()-proj.min())
 else:raw=clean(Image.open(R/f'sources/{h}-probe.png'));scale=.625
 scaled=raw.convert('RGBa').resize((round(raw.width*scale),round(raw.height*scale)),Image.Resampling.LANCZOS).convert('RGBA');base=Image.new('RGBA',(SIZE,SIZE));base.alpha_composite(scaled,((SIZE-scaled.width)//2,(SIZE-scaled.height)//2));poses[h]=base
 a=ORDER.index(h)*math.pi/4;yy,xx=np.where(np.array(base)[:,:,3]>128);proj=(xx-256)*math.cos(a)+(yy-256)*math.sin(a);lengths[h]=float(proj.max()-proj.min())
 headings[h]={'pose':save(base,f'poses/{h}.png'),'angle':a,'sourceScale':scale,'length':lengths[h],'pivot':[256,256]}
empty=save(Image.new('RGBA',(SIZE,SIZE)),'effects/empty.png');effects={}
for h in ORDER:
 for kind in ['wake','scan']:
  atlas=Image.new('RGBA',(SIZE*6,SIZE*10));files=[]
  for n in range(60):
   im=effect(h,kind,n);files.append(save(im,f'effects/{kind}-{h}/{n:02}.png'));atlas.paste(im,(n%6*SIZE,n//6*SIZE))
  effects[kind+'-'+h]={'frames':files,'atlas':save(atlas,f'atlases/{kind}-{h}.png'),'columns':6,'frameCount':60}
states=[]
for h in ORDER:
 for state in ['idle','cruise','brake','scan','return']+(['launch','dock','recharge'] if h in ['north','east','south','west'] else []):
  kind='scan' if state=='scan' else 'wake' if state in ['cruise','return','launch','brake'] else None
  states.append({'id':state+'-'+h,'heading':h,'state':state,'fps':30,'frameCount':60,'loop':state in ['idle','cruise','scan','return','recharge'],'body':headings[h]['pose'],'effect':kind+'-'+h if kind else None,'lamp':'yellow' if state=='recharge' else 'blue'})
bay=json.loads((R/'sources/bay-study-manifest.json').read_text())
launchers={h:{'image':f'sources/{h}-launcher.png','anchor':m['anchor'],'libraryScale':.945} for h,m in bay['directions'].items()}
resource=clean(Image.open(R/'sources/resource-v2.png'));resource.thumbnail((130,100),Image.Resampling.LANCZOS);save(resource,'resource.png')
data={'id':'survey-probe-v1','frameSize':512,'worldUnitsPerPixel':.34,'fps':30,'headings':headings,'states':states,'effects':effects,'launchers':launchers,'resource':'resource.png','missionSeconds':32,'sources':[{'path':p.relative_to(R).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (R/'sources').glob('*.png')],'scope':'Animation preview: eight-way travel and scanning, four bay orientations; native room calibration and gameplay integration pending.'}
(R/'manifest.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
board=Image.new('RGBA',(1200,700),'#17272e');d=ImageDraw.Draw(board)
for i,h in enumerate(ORDER):
 x=i%4*300;y=i//4*350;d.text((x+10,y+12),h.upper(),fill='white');board.alpha_composite(poses[h].resize((280,280),Image.Resampling.LANCZOS),(x+10,y+25));small=poses[h].resize((174,174),Image.Resampling.LANCZOS);board.alpha_composite(small,(x+60,y+170))
save(board,'review/directions.png');print(f'{len(states)} clips; 8 headings; {len(effects)*60} separate effect frames; no source upscaling.')
