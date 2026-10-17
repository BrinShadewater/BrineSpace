"""Review every currently selected ordinary rest pose and cross-family joins."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];coverage=json.loads((R/'character/james-animation-coverage-2026-09-30/runtime-coverage.json').read_text());cache={};records=[];joins=[];clocks=[]
def load(mode,key):
    file=R/coverage['body' if mode=='bare' else 'equipment'][key]['path']
    if file not in cache:cache[file]=json.loads(file.read_text())
    m=cache[file];s=next(s for s in m['states'] if s['id']==key);ims=[];paths=[]
    for f in s['frameFiles']:
        path=R/f.removeprefix('res://') if f.startswith('res://') else (file.parent/f).resolve();ims.append(Image.open(path).convert('RGBA'));paths.append(path)
    return m,s,ims,paths
def plane(im,m):
    assert m['standingHeight']==148
    out=Image.new('RGBA',(256,256));out.alpha_composite(im,(128-int(m['pivot'][0]),224-int(m['pivot'][1])));return out
for direction in ['north','south','east','west']:
    board=Image.new('RGB',(7*256,6*280),'#303b40');draw=ImageDraw.Draw(board);timelines={}
    for mode_i,mode in enumerate(['bare','helmet']):
        mm,ms,mi,_=load(mode,'idle-'+direction);master=plane(mi[0],mm);phases={};timeline=[]
        for action_i,action in enumerate(['lie-down','sleep','get-up']):
            key=action+'-'+direction;m,s,ims,paths=load(mode,key);prepared=[plane(im,m) for im in ims];phases[action]=prepared;row=mode_i*3+action_i
            board.paste(master,(0,row*280+24),master);draw.text((5,row*280+5),mode+' standing master',fill='white')
            for i,im in enumerate(prepared):
                board.paste(im,((i+1)*256,row*280+24),im);draw.text(((i+1)*256+5,row*280+5),mode+' '+key+' '+str(i),fill='white')
                a=np.array(im);yy,xx=np.where(a[:,:,3]>192);rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);opaque=a[:,:,3]>192
                neutral=opaque&(np.ptp(rgb,2)<28)&(rgb.mean(2)>20)&(rgb.mean(2)<110)&~((r-b>18)&(g-b>10))
                records.append({'mode':mode,'key':key,'index':i,'path':paths[i].relative_to(R).as_posix(),'sha256':hashlib.sha256(paths[i].read_bytes()).hexdigest(),'registeredBounds':[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())],'neutralMedian':np.median(rgb[neutral],0).tolist() if neutral.any() else None})
            duration=sum(s['frameDurationsMs']);clocks.append({'mode':mode,'key':key,'visualCycleMs':duration})
            if action=='sleep':
                remaining=10400;slot=0
                while remaining>0:
                    dt=min(int(s['frameDurationsMs'][slot%len(ims)]),remaining);timeline.append({'key':key,'index':slot%len(ims),'durationMs':dt,'image':prepared[slot%len(ims)]});remaining-=dt;slot+=1
            else:
                for i,dt in enumerate(s['frameDurationsMs']):timeline.append({'key':key,'index':i,'durationMs':int(dt),'image':prepared[i]})
        for label,a,b in [('standing->lie',master,phases['lie-down'][0]),('lie->sleep',phases['lie-down'][-1],phases['sleep'][0]),('sleep->rise',phases['sleep'][-1],phases['get-up'][0]),('rise->standing',phases['get-up'][-1],master)]:
            aa=np.array(a);bb=np.array(b);joins.append({'mode':mode,'direction':direction,'join':label,'wholeRegisteredPixelsExact':np.array_equal(aa,bb),'changedPixels':int(np.any(aa!=bb,2).sum())})
        wm,ws,wi,_=load(mode,'walk-'+direction);walk=plane(wi[0],wm)
        joinboard=Image.new('RGB',(3*256,280),'#303b40');jd=ImageDraw.Draw(joinboard)
        for col,(label,im) in enumerate([('get-up final',phases['get-up'][-1]),('standing master',master),('walk frame0',walk)]):joinboard.paste(im,(col*256,24),im);jd.text((col*256+5,5),mode+' '+direction+' '+label,fill='white')
        joinboard.save(P/(mode+'-'+direction+'-standing-walk.png'))
        timelines[mode]=timeline
    board.save(P/(direction+'-all-poses.png'))
    assert [x['durationMs'] for x in timelines['bare']]==[x['durationMs'] for x in timelines['helmet']]
    views=[];events=[]
    for event_i,(bare,helmet) in enumerate(zip(timelines['bare'],timelines['helmet'])):
        v=Image.new('RGB',(1000,340),'#303b40');d=ImageDraw.Draw(v);d.text((8,8),'James '+direction+' ordinary rest / complete12s service timeline / '+bare['key']+' source '+str(bare['index']),fill='white')
        for j,im in enumerate([bare['image'],helmet['image']]):
            v.paste(im,(j*240,55),im)
            for h,x in [(82,515),(54,740),(27,885)]:
                scale=h/148;small=im.resize((round(256*scale),round(256*scale)),Image.Resampling.BILINEAR);v.paste(small,(x+j*(small.width+5),310-round(224*scale)),small)
        views.append(v);events.append({k:v for k,v in bare.items() if k!='image'})
    times=[e['durationMs'] for e in events];bound=np.rint(np.cumsum([0]+times)/10).astype(int)*10;dur=np.diff(bound).tolist();views[0].save(P/(direction+'-service-clock.gif'),save_all=True,append_images=views[1:],duration=dur,loop=0)
    (P/(direction+'-timeline.json')).write_text(json.dumps({'durationMs':sum(times),'events':events,'scope':'Source event replay of complete normal service12s, repeated six-slot breathing loop at3600ms and final partial cycle. Not newly authored frames or actual route video.'},indent=2)+'\n',encoding='utf-8')
report={'sourceReferences':len(records),'joins':joins,'clocks':clocks,'records':records,'scope':'All selected ordinary rest source poses in four facings/bare+helmet; fixed physical ruler/master/standing-walk comparison and full service-clock source replays. No new native furniture/gear/rotation claims.'}
(P/'review-evidence.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({'sourceReferences':len(records),'exactJoins':sum(j['wholeRegisteredPixelsExact'] for j in joins),'joins':len(joins),'nonExact':[j for j in joins if not j['wholeRegisteredPixelsExact']]}))
