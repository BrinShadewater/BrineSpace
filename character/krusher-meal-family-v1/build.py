"""Reuse selected whole James meal poses; preserve source food/hand occlusion."""
import copy,hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;R=P.parent.parent
inventory=json.loads((R/'character/krusher-complete-animation-v1/source-coverage.json').read_text())
C=R/'character/krusher-james-canonical-v4';yy,xx=np.indices((256,256));target=np.array([82.,124.,128.]);luma=np.array([.2126,.7152,.0722]);records=[];checks=0
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
profiles={'bare':{'name':'Krusher Dom meals','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'candidate-not-installed','identity':{'name':'Krusher Dom','title':'System Administrator','department':'AI & Robotics','accentTarget':'#527C80','baseFamily':'James / Branforth'},'states':[]}}
profiles['helmet']=copy.deepcopy(profiles['bare']);profiles['helmet']['name']='Krusher Dom sealed-helmet meal inspection substitutes'
for gear in ['bare','helmet']:
 for action in ['eat','drink']:
  for direction in ['south','east','north','west']:
   key=action+'-'+direction;resolved=inventory['resolved'][gear][key];mp=R/resolved['manifest'].removeprefix('res://');state=copy.deepcopy(resolved['state']);profile=resolved['profile'];files=[]
   headpath=R/f'character/krusher-bill-base-test-v2/sources/{direction}-head-native.png';head=Image.open(headpath).convert('RGBA')
   helmet_m=json.loads((C/'helmet-manifest.json').read_text());tablet=next(s for s in helmet_m['states'] if s['id']=='interact-'+direction)
   chosen=[0,int(len(tablet['frameFiles'])*.18),int(len(tablet['frameFiles'])*.4),int(len(tablet['frameFiles'])*.6),int(len(tablet['frameFiles'])*.8),len(tablet['frameFiles'])-1]
   for i,relative in enumerate(state['frameFiles']):
    original_source=((R/relative.removeprefix('res://')) if relative.startswith('res://') else (mp.parent/relative)).resolve();a0=Image.open(original_source).convert('RGBA');pad=Image.new('RGBA',(256,256));offset=(round(128-profile['pivot'][0]),round(224-profile['pivot'][1]));pad.alpha_composite(a0,offset);a=np.array(pad);rgb=a[:,:,:3].astype(float);foreground=np.zeros((256,256),bool)
    if gear=='helmet':
     source=C/tablet['frameFiles'][chosen[i]];pad=Image.new('RGBA',(256,256));pad.alpha_composite(Image.open(source).convert('RGBA'),(36,52));out=np.array(pad);allowed=np.ones((256,256),bool);marking=np.zeros_like(allowed);headmask=np.zeros_like(allowed);anchor=None
    else:
     source=original_source
     zone=(a[:,:,3]>180)&(xx>=110)&(xx<151)&(yy>=65)&(yy<92)
     top=int(yy[zone].min());crown=zone&(yy<top+14);axis=round((int(xx[crown].min())+int(xx[crown].max()))/2)
     neck={'south':101,'east':100,'north':96,'west':100}[direction];head_bottom=neck+(top-76)
     # Preserve original high rear collar and the in-front meal equipment.
     x0=axis-head.width//2-5;x1=axis+head.width//2+6
     headmask=(xx>=x0)&(xx<x1)&(yy>=top-5)&(yy<head_bottom)
     collar=(yy>=head_bottom-5)&(a[:,:,3]>0)
     if direction=='south':collar&=(xx<axis-8)|(xx>axis+8)
     elif direction=='east':collar&=xx<axis-3
     elif direction=='west':collar&=xx>axis+3
     else:collar&=yy>=head_bottom-2
     headmask&=~collar
     if i in (2,3):
      if direction=='south':
       foreground|=(xx>=117)&(xx<125)&(yy>=94)&(yy<112)
       if action=='drink':foreground|=(xx>=126)&(xx<135)&(yy>=90)&(yy<118)
       else:foreground|=(xx>=125)&(xx<137)&(yy>=98)&(yy<104)
      elif direction=='east':foreground|=(xx>=135)&(xx<153)&(yy>=95)&(yy<113)
      elif direction=='west':foreground|=(xx>=106)&(xx<122)&(yy>=94)&(yy<113)
      else:foreground|=(xx>=110)&(xx<119)&(yy>=91)&(yy<head_bottom)
     foreground&=a[:,:,3]>0;headmask&=~foreground
     anchor=[axis-head.width//2,head_bottom-head.height]
     layer=Image.new('RGBA',(256,256));layer.paste(head,tuple(anchor));h=np.array(layer);out=a.copy();out[headmask]=h[headmask]
     yellow=(rgb[:,:,0]>rgb[:,:,2]*1.15)&(rgb[:,:,1]>rgb[:,:,2]*1.12)&(rgb[:,:,0]>35)&(rgb[:,:,1]>rgb[:,:,0]*.65)
     marking=yellow&(a[:,:,3]>0)&(yy>=96)&(yy<141)&(~headmask)&(~foreground)
     gain=np.minimum(1.15,(rgb@luma)/(target@luma));colour=np.rint(gain[:,:,None]*target).astype('uint8');out[marking,:3]=colour[marking];allowed=headmask|marking
     assert np.array_equal(a[~allowed],out[~allowed]);assert np.array_equal(a[foreground],out[foreground]);assert np.array_equal(a[141:],out[141:]);checks+=3
    rel=f'frames/{gear}/{key}/{i:03}.png';q=P/rel;q.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(q);files.append(rel)
    maskrel=f'masks/{gear}/{key}-{i:03}.png';maskpath=P/maskrel;maskpath.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(allowed.astype('uint8')*255).save(maskpath)
    fgrel=f'masks/{gear}/{key}-{i:03}-foreground.png';Image.fromarray(foreground.astype('uint8')*255).save(P/fgrel)
    records.append({'gear':gear,'state':key,'frame':i,'source':source.relative_to(R).as_posix(),'sourceHash':sha(source),'originalMealSource':original_source.relative_to(R).as_posix(),'originalSourceHash':sha(original_source),'output':rel,'outputHash':sha(q),'sourcePadding':list(offset),'allowedMask':maskrel,'foregroundMask':fgrel,'headPaste':anchor,'sourceManifest':resolved['manifest'],'sourceManifestHash':sha(mp),'headSource':headpath.relative_to(R).as_posix(),'headHash':sha(headpath),'canonicalTabletPose':chosen[i] if gear=='helmet' else None})
   state['frameFiles']=files;state['provenance']={'bodyReuse':'Current selected James whole meal source; Krusher identity/upper suit markings only' if gear=='bare' else 'Existing canonical-v4 Krusher sealed tablet inspection poses; closed helmet never displays eating or drinking','scope':'Existing per-state timing/loop/events retained; bare foreground utensils and hands retained'};profiles[gear]['states'].append(state)
for gear,m in profiles.items():(P/(gear+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n')
(P/'provenance.json').write_text(json.dumps({'checks':checks,'errors':[],'records':records,'scope':'Four-direction eating/drinking and sealed inspection substitutes. Original body registration, clocks, hands and utensils; no normal runtime installation.'},indent=2)+'\n')
font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),24)
for gear,m in profiles.items():
 board=Image.new('RGB',(1440,840),'#242c31');d=ImageDraw.Draw(board);d.text((15,10),'KRUSHER DOM / '+('MEALS' if gear=='bare' else 'SEALED INSPECTION SUBSTITUTES'),font=font,fill='white')
 for j,s in enumerate(m['states']):
  im=Image.open(P/s['frameFiles'][2]).convert('RGBA');x=(j%4)*360;y=50+(j//4)*390;tile=im.resize((256,256),Image.Resampling.NEAREST);board.paste(tile,(x+10,y),tile);small=im.resize((128,128),Image.Resampling.LANCZOS);board.paste(small,(x+210,y+150),small);d.text((x+10,y+285),s['id']+' / '+gear,font=font,fill='#cadcde')
 board.save(P/(gear+'-sheet.png'))
print(json.dumps({'states':16,'frames':len(records),'compositionChecks':checks,'errors':[]}))
