from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];S=R/'character/james-tablet-east-belt-fixed-source-v2'
checks=[];records=[];arrays={}
for mode in ['bare','helmet']:
    source=json.loads((S/(mode+'-manifest.json')).read_bytes());candidate=json.loads((P/(mode+'-manifest.json')).read_bytes())
    checks.append({'name':mode+' geometry metadata','pass':all(source[k]==candidate[k] for k in ['frameWidth','frameHeight','pivot','standingHeight','precomposed','textureFilter'])})
    for old,new in zip(source['states'],candidate['states']):
        checks.append({'name':mode+' '+old['id']+' clock/count/loop','pass':all(old[k]==new[k] for k in ['id','frameCount','frameDurationsMs','loop'])})
    frames=[]
    st=next(s for s in source['states'] if s['id']=='inspect-east');ct=next(s for s in candidate['states'] if s['id']=='inspect-east')
    for i,(old,new) in enumerate(zip(st['frameFiles'],ct['frameFiles'])):
        a=np.array(Image.open((S/old).resolve()).convert('RGBA'));im=Image.open(P/new).convert('RGBA');b=np.array(im);frames.append(im)
        rgb=a[:,:,:3].astype(int);r,g,blue=rgb.transpose(2,0,1);yy,xx=np.indices(a.shape[:2]);spread=np.ptp(rgb,2)
        green=(10*g>13*r)&(10*g>13*blue)&(g>70)
        equipment=(xx>=98)&(yy>=40)&(yy<138)&(rgb.sum(2)>255)&(spread<35)
        mask=(green|equipment)&(a[:,:,3]>0)
        if mode=='helmet':
            bare=np.array(Image.open((S/'candidate-frames/bare'/Path(old).name).resolve()).convert('RGBA'))
            protected=np.any(a!=bare,2)&~green;mask &= ~protected
            checks.append({'name':str(i)+' exact non-key-spill shared helmet difference region','pass':np.array_equal(a[protected],b[protected])})
        if i in [0,140]:mask[:]=False
        equal_alpha=np.array_equal(a[:,:,3],b[:,:,3]);equal_outside=np.array_equal(a[~mask],b[~mask])
        checks.extend([{'name':mode+str(i)+' original alpha','pass':equal_alpha},{'name':mode+str(i)+' outside bounded colour mask','pass':equal_outside}])
        rr,gg,bb=b[:,:,:3].astype(float).transpose(2,0,1);remaining=(b[:,:,3]>0)&(gg>1.3*rr)&(gg>1.3*bb)&(gg>70)
        checks.append({'name':mode+str(i)+' key spill removed','pass':not remaining.any()})
        if i in [0,140]:checks.append({'name':mode+str(i)+' exact master','pass':np.array_equal(a,b)})
        records.append({'mode':mode,'index':i,'changedPixels':int(np.any(a!=b,2).sum()),'changedAboveY40':int(np.any(a[:40]!=b[:40],2).sum()),'remainingKeyGreenPixels':int(remaining.sum())})
    arrays[mode]=frames
    for page in range(5):
        board=Image.new('RGB',(8*184,4*208),'#303b40');draw=ImageDraw.Draw(board)
        for j,i in enumerate(range(page*32,min((page+1)*32,141))):
            at=((j%8)*184,(j//8)*208+24);board.paste(frames[i],at,frames[i]);draw.text((at[0]+4,at[1]-20),mode+' candidate '+str(i),fill='white')
        board.save(P/(mode+'-candidate-cycle-'+str(page)+'.png'))
    board=Image.new('RGB',(7*184,3*208),'#303b40');draw=ImageDraw.Draw(board)
    for col,i in enumerate([0,20,40,60,83,120,140]):
        for row,im in enumerate([frames[0],Image.open((S/st['frameFiles'][i]).resolve()).convert('RGBA'),frames[i]]):
            at=(col*184,row*208+24);board.paste(im,at,im);draw.text((at[0]+4,at[1]-20),['master','selected '+str(i),'candidate '+str(i)][row],fill='white')
    board.save(P/(mode+'-material-comparison.png'))
for i in range(141):checks.append({'name':str(i)+' paired body below60','pass':np.array_equal(np.array(arrays['bare'][i])[60:],np.array(arrays['helmet'][i])[60:])})
installed=all(('res://character/'+P.name+'/'+m+'-manifest.json') in (R/'scripts/grid_canvas.gd').read_text() for m in ['bare','helmet'])
report={'checks':len(checks),'failures':[c for c in checks if not c['pass']],'records':records,'productionInstalled':installed,'scope':'All282 native-material candidate images, original alpha/outside bounded material selector and exact master endpoints; paired lower body and complete source clocks/pivots. Non-key-spill helmet difference region exact. Does not prove semantic segmentation, natural animation admission or full James acceptance.'}
(P/'material-package-evidence.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'checks':len(checks),'failures':len(report['failures']),'firstFailures':report['failures'][:3],'maxChangedAboveY40':max(r['changedAboveY40'] for r in records)}))
assert not report['failures']
