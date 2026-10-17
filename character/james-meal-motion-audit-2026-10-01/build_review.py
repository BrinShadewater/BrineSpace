from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageChops
P=Path(__file__).resolve().parent;R=P.parents[1]
C=R/'character/james-animation-coverage-2026-09-30/runtime-coverage.json'
coverage=json.loads(C.read_text());cache={};metrics=[];clips=[];joins=[]
actions=['meal-acquire','eat','meal-deposit','cup-acquire','drink','cup-deposit']
def load(mode,key):
    path=R/coverage[mode][key]['path']
    if path not in cache:cache[path]=json.loads(path.read_text())
    manifest=cache[path];state=next(s for s in manifest['states'] if s['id']==key)
    frames=[Image.open(R/f.removeprefix('res://') if f.startswith('res://') else path.parent/f).convert('RGBA') for f in state['frameFiles']]
    return manifest,state,frames
def plane(im,m):
    scale=148/m['standingHeight'];im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS) if scale!=1 else im
    p=Image.new('RGBA',(256,256));at=(round(128-m['pivot'][0]*scale),round(224-m['pivot'][1]*scale));p.alpha_composite(im,at);return p
for direction in ['north','south','east','west']:
    selected=[(mode,a+'-'+direction) for mode in ['body','equipment'] for a in actions if a+'-'+direction in coverage[mode]]
    board=Image.new('RGB',(9*256,len(selected)*280),'#303b40');draw=ImageDraw.Draw(board)
    for row,(mode,key) in enumerate(selected):
        m,s,frames=load(mode,key);mm,ms,mf=load(mode,'idle-'+direction);master=plane(mf[0],mm)
        board.paste(master,(0,row*280+24),master);draw.text((8,row*280+8),mode+' master '+direction,fill='white')
        prepared=[]
        for i,im in enumerate(frames):
            p=plane(im,m);prepared.append(p);board.paste(p,((i+1)*256,row*280+24),p);draw.text(((i+1)*256+8,row*280+8),key+' '+str(i),fill='white')
            arr=np.array(p);yy,xx=np.where(arr[:,:,3]>180)
            metrics.append({'mode':mode,'key':key,'index':i,'framePath':s['frameFiles'][i],'crown':int(yy.min()),'sole':int(yy.max()),'width':int(xx.max()-xx.min()+1),'sha256':hashlib.sha256(im.tobytes()).hexdigest()})
        views=[]
        for i,p in enumerate(prepared):
            v=Image.new('RGB',(650,290),'#303b40');d=ImageDraw.Draw(v);d.text((8,8),mode+' '+key+' / selected source clock / '+str(i),fill='white');v.paste(master,(0,26),master);v.paste(p,(256,26),p)
            small=p.resize((142,142),Image.Resampling.BILINEAR);v.paste(small,(505,145),small);views.append(v)
        ds=s.get('frameDurationsMs',[100]*len(frames));bound=np.rint(np.cumsum([0]+ds)/10).astype(int)*10;times=np.diff(bound).tolist();name=mode+'-'+key+'.gif'
        views[0].save(P/name,save_all=True,append_images=views[1:],duration=times,loop=0)
        clips.append({'mode':mode,'key':key,'frames':len(frames),'manifest':coverage[mode][key]['path'],'preview':name,'sourceClockMs':sum(ds),'role':'sealed inspection substitute' if mode=='equipment' else 'bare meal motion'})
    board.save(P/(direction+'-all-poses.png'))
    if direction in ['north','south']:
        pairs=[('meal-acquire',-1,'eat',0),('eat',-1,'meal-deposit',0),('meal-deposit',-1,'cup-acquire',0),('cup-acquire',-1,'drink',0),('drink',-1,'cup-deposit',0),('cup-deposit',-1,'idle',0)]
        for a,i,b,j in pairs:
            ma,sa,fa=load('body',a+'-'+direction);mb,sb,fb=load('body',b+'-'+direction);pa=plane(fa[i],ma);pb=plane(fb[j],mb)
            diff=ImageChops.difference(pa,pb);exact=not any(max(x)>0 for x in diff.get_flattened_data())
            assert exact,(direction,a,b)
            joins.append({'direction':direction,'from':a,'to':b,'wholeRegisteredPixelsExact':True})
report={'selectedClips':len(clips),'allSourceReferences':len(metrics),'exactRegisteredJoins':len(joins),'clips':clips,'joins':joins,'metrics':metrics,'coverageSha256':hashlib.sha256(C.read_bytes()).hexdigest(),'scope':'Every selected normal bare meal phase and sealed inspection substitute source frame, all four facings, native148 and82 equivalent. Source-clock GIFs, no new native route/gear/furniture or full-set acceptance claim.'}
(P/'review-evidence.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ['selectedClips','allSourceReferences','exactRegisteredJoins','scope']}))
