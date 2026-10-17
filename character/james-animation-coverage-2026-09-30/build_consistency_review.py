from pathlib import Path
import json,re,sys
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];coverage=json.loads((P/'runtime-coverage.json').read_text());out=P/'consistency-review';out.mkdir(exist_ok=True)
requested=set(sys.argv[1:])
previous=json.loads((out/'diagnostics.json').read_text()) if requested and (out/'diagnostics.json').exists() else {}
cache={};metrics=previous.get('metrics',{});families={}
def state(mode,key):
    file=R/coverage['body' if mode=='bare' else 'equipment'][key]['path']
    if file not in cache:cache[file]=json.loads(file.read_text())
    m=cache[file];return file.parent,m,next(s for s in m['states'] if s['id']==key)
def frame(mode,key,index):
    folder,m,s=state(mode,key);path=s['frameFiles'][index]
    source=R/path.removeprefix('res://') if path.startswith('res://') else folder/path
    return Image.open(source).convert('RGBA'),m
def draw_frame(board,mode,key,index,x,y):
    im,m=frame(mode,key,index);sc=82/m['standingHeight'];im=im.resize((round(im.width*sc),round(im.height*sc)),Image.Resampling.BILINEAR)
    board.paste(im,(round(x-m['pivot'][0]*sc),round(y-m['pivot'][1]*sc)),im)
for key in coverage['body']:
    family=re.sub(r'-(east|west|north|south)(-(east|west|north|south))?$','',key);families.setdefault(family,[]).append(key)
for family,keys in families.items():
    if requested and family not in requested:continue
    board=Image.new('RGB',(1200,len(keys)*240),'#303b40');draw=ImageDraw.Draw(board)
    for row,key in enumerate(keys):
        d=key.split('-')[-1];d=d if d in ['east','south','west','north'] else 'east';y=row*240
        for mode,x in [('bare',90),('helmet',230)]:
            master='idle-'+d;draw_frame(board,mode,master,0,x,y+135);draw.text((x-45,y+5),master+' '+mode,fill='white')
        for mode,offset in [('bare',0),('helmet',3)]:
            if key not in coverage['body' if mode=='bare' else 'equipment']:continue
            folder,m,s=state(mode,key);n=len(s['frameFiles']);samples=[0,n//2,n-1]
            for col,index in enumerate(samples):
                x=390+(col+offset)*145;draw_frame(board,mode,key,index,x,y+135);draw.text((x-68,y+5),mode+' '+str(index)+' '+key,fill='white')
            entries=[]
            for index in sorted(set(samples)):
                im,_=frame(mode,key,index);a=np.array(im);yy,xx=np.where(a[:,:,3]>180);rgb=a[:,:,:3].astype(float);rr,gg,bb=rgb.transpose(2,0,1)
                gold=(a[:,:,3]>200)&(rr-bb>28)&(gg-bb>15)&(rr<170)
                cloth=(a[:,:,3]>200)&(rgb.max(2)<85)&(rgb.min(2)>18)&(abs(rr-bb)<16)&(abs(gg-bb)<16)
                assert 20 < 135+(yy.min()-m['pivot'][1])*82/m['standingHeight'] and 135+(yy.max()+1-m['pivot'][1])*82/m['standingHeight'] < 240, ('Review crop',mode,key,index)
                entries.append(dict(index=index,physicalAlphaSize=[round((xx.max()+1-xx.min())*148/m['standingHeight'],2),round((yy.max()+1-yy.min())*148/m['standingHeight'],2)],clothMedianRgb=np.median(rgb[cloth],axis=0).tolist() if cloth.any() else None,goldMedianRgb=np.median(rgb[gold],axis=0).tolist() if gold.any() else None))
            metrics[mode+'-'+key]=entries
    board.save(out/(family+'.png'))
    for page,start in enumerate(range(0,len(keys),6)):
        board.crop((0,start*240,1200,min(len(keys),start+6)*240)).save(out/(family+'-page-'+str(page)+'.png'))
(out/'diagnostics.json').write_text(json.dumps(dict(scope='Selected literal-source inventory; native82px equivalent Pillow board, first/middle/final samples. Alpha/material metrics are comparative diagnostics, not anatomy/visual acceptance or actual runtime render proof.',families=len(families),sampledClips=len(metrics),metrics=metrics),indent=2)+'\n')
print(len(requested) if requested else len(families),'family boards updated;',len(metrics),'selected clip diagnostics retained; visual review pending')
