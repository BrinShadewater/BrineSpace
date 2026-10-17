"""Review actual ordered selected rest sources, not historic comparison boards."""
from pathlib import Path
import re,json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];P.mkdir(exist_ok=True)
source=(R/'scripts/grid_canvas.gd').read_text();start=source.index('elif actor == "branforth":');block=source[start:source.index('\nfunc ',start)]
catalog_root=R/'character/chief-engineer-branforth-v2';catalog=json.loads((catalog_root/'catalog.json').read_bytes());selected={'bare':{},'helmet':{}}
inputs={}; records=[];checks=[]
def freeze(p): inputs[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
def add(path,mode):
    data=json.loads(path.read_bytes())
    for state in data['states']:selected[mode][state['id']]=(path,data,state)
for field,mode in [('body','bare'),('equipment','helmet')]:
    for rel in catalog[field]:add(catalog_root/rel,mode)
for kind,path in re.findall(r'player\.(load_manifest|load_equipment_manifest)\((?:"diving-helmet",\s*)?"res://([^"]+)"',block):add(R/path,'bare' if kind=='load_manifest' else 'helmet')
def frames(mode,key):
    path,pack,state=selected[mode][key];freeze(path);out=[]
    for rel in state['frameFiles']:
        file=R/rel.removeprefix('res://') if rel.startswith('res://') else (path.parent/rel).resolve();freeze(file);out.append(Image.open(file).convert('RGBA'))
    return out,pack,state,path
freeze(R/'scripts/grid_canvas.gd');freeze(R/'character/ACTIVE_ASSETS.json');freeze(catalog_root/'catalog.json')
head_boxes={}
for direction,folder,suffix in [('south','james-rest-south-identity-v2','v2'),('west','james-rest-west-identity-v2','v2'),('east','james-rest-east-identity-v2','v3')]:
    path=R/'character'/folder/('registration-'+suffix+'.json');freeze(path);reg=json.loads(path.read_bytes())
    head_boxes[direction]=[row['protectedHeadBox'] for row in reg['tracking']]
old=json.loads((R/'character/james-rest-material-continuity-v1/material-evidence.json').read_bytes())
clips={}
for direction in ['north','east','south','west']:
    board=Image.new('RGB',(7*256,6*280),'#303b40');bd=ImageDraw.Draw(board)
    heads=Image.new('RGB',(7*204,6*230),'#303b40');hd=ImageDraw.Draw(heads)
    for gi,mode in enumerate(['bare','helmet']):
        master,mp,ms,mf=frames(mode,'idle-'+direction);raw_master=master[0]
        bundles={action:frames(mode,action+'-'+direction) for action in ['lie-down','sleep','get-up']}
        restpack=bundles['lie-down'][1]
        factor=float(restpack['standingHeight'])/float(mp['standingHeight'])
        master=Image.new('RGBA',bundles['lie-down'][0][0].size)
        scaled=raw_master.resize((round(raw_master.width*factor),round(raw_master.height*factor)),Image.Resampling.LANCZOS) if factor!=1 else raw_master
        shift=[round(restpack['pivot'][i]-mp['pivot'][i]*factor) for i in range(2)]
        master.alpha_composite(scaled,tuple(shift))
        down=bundles['lie-down'][0];sleep=bundles['sleep'][0];up=bundles['get-up'][0]
        def visible_equal(a,b):
            aa,bb=np.array(a),np.array(b);return bool(np.array_equal(aa[:,:,3],bb[:,:,3]) and np.array_equal(aa[:,:,:3][aa[:,:,3]>0],bb[:,:,:3][aa[:,:,3]>0]))
        for label,ok in [('registered standing entry',visible_equal(down[0],master)),('registered standing return',visible_equal(up[-1],master)),('lie/sleep join',down[-1].tobytes()==sleep[0].tobytes()),('sleep/get-up join',sleep[0].tobytes()==up[0].tobytes()),('sleep loop seam',sleep[-1].tobytes()==sleep[0].tobytes()),('reverse get-up',all(a.tobytes()==b.tobytes() for a,b in zip(down,reversed(up))))]:
            checks.append({'mode':mode,'direction':direction,'label':label,'pass':ok})
        checks.append({'mode':mode,'direction':direction,'label':'3600ms looping sleep','pass':sum(bundles['sleep'][2]['frameDurationsMs'])==3600 and bundles['sleep'][2]['loop']})
        for ai,action in enumerate(['lie-down','sleep','get-up']):
            imgs,pack,state,path=bundles[action];row=gi*3+ai
            clips[mode+'-'+action+'-'+direction]={'manifest':path.relative_to(R).as_posix(),'frames':state['frameFiles'],'durations':state['frameDurationsMs'],'loop':state['loop'],'pivot':pack['pivot'],'standingHeight':pack['standingHeight']}
            for col,im in enumerate([master,*imgs]):
                label=mode+' '+('master' if col==0 else action+' '+str(col-1));at=(col*256,row*280+24);board.paste(im,at,im);bd.text((at[0]+4,at[1]-19),label,fill='white')
                pose=0 if col==0 else state['provenance']['sourcePoses'][col-1]
                if col==0:
                    box=next(r['protectedHead'] for r in old['records'] if r['mode']==mode and r['key']=='lie-down-'+direction and r['index']==0)
                elif direction=='north':
                    entry=next(r for r in old['records'] if r['mode']==mode and r['key']==('lie-down' if col==0 else action)+'-north' and r['index']==(0 if col==0 else col-1));box=entry['protectedHead']
                else:box=head_boxes[direction][5 if action=='sleep' and col!=0 else pose]
                cx=(box[0]+box[2])//2;cy=(box[1]+box[3])//2;crop=im.crop((cx-25,cy-25,cx+25,cy+25)).resize((200,200),Image.Resampling.NEAREST);ha=(col*204,row*230+24);heads.paste(crop,ha,crop);hd.text((ha[0]+4,ha[1]-19),label,fill='white')
                if col:records.append({'mode':mode,'direction':direction,'action':action,'index':col-1,'manifest':path.relative_to(R).as_posix(),'rgbaSha256':hashlib.sha256(im.tobytes()).hexdigest(),'alphaBounds':im.getchannel('A').getbbox(),'headReviewBox':box})
    board.save(P/(direction+'-selected-all-poses.png'));heads.save(P/(direction+'-selected-all-heads.png'))
(P/'selected-inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
(P/'selected-clips.json').write_text(json.dumps(clips,indent=2)+'\n')
(P/'source-evidence.json').write_text(json.dumps({'method':'Retained catalog followed by current source-loader order independently traced. All144 selected rest source references plus full idle frames frozen; same-pixel source and head boards. No new source edits or runtime/controller proof.','checks':checks,'failures':sum(not c['pass'] for c in checks),'records':records,'inputCount':len(inputs)},indent=2)+'\n')
print(len(records),'selected rest references;',len(checks),'join/clock checks;',sum(not c['pass'] for c in checks),'failures;',len(inputs),'frozen inputs')
