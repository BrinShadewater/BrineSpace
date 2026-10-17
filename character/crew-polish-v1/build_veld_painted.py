"""Register authored Veld sources into a coherent core-action candidate.

Saved source art only. Sources and the production catalog are never overwritten.
"""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,find_objects

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'veld-painted-v2'
DIRS=['east','west','south','north']
RECORDS=[]

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def extract(name,cols,rows):
    path=ROOT/'sources'/f'{name}.png'
    image=Image.open(path).convert('RGBA');a=np.array(image)
    ids,_=label(a[:,:,3]>=128);sizes=np.bincount(ids.ravel())
    boxes=[(s[1].start,s[0].start,s[1].stop,s[0].stop) for i,s in enumerate(find_objects(ids)) if sizes[i+1]>1500]
    assert len(boxes)==cols*rows,(name,len(boxes))
    boxes.sort(key=lambda b:(b[1]+b[3])/2)
    ordered=[]
    for row in range(rows):ordered+=sorted(boxes[row*cols:(row+1)*cols],key=lambda b:b[0])
    result=[]
    for i,b in enumerate(ordered):
        crop=(max(0,b[0]-2),max(0,b[1]-2),min(image.width,b[2]+2),min(image.height,b[3]+2))
        tile=np.array(image.crop(crop));tile[:,:,3]=np.where(tile[:,:,3]>=128,255,0);tile[tile[:,:,3]==0]=0
        result.append((Image.fromarray(tile),crop))
    RECORDS.append(dict(source=path.relative_to(ROOT).as_posix(),sha256=digest(path),boxes=[b for _,b in result]))
    return result

def head_axis(tile):
    a=np.array(tile)[:,:,3]>0;b=tile.getbbox();height=b[3]-b[1]
    ys,xs=np.where(a[b[1]:b[1]+max(3,round(height*.11))])
    return (float(xs.min())+float(xs.max()))/2

def registered(tile,scale,anchor):
    resized=tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.LANCZOS)
    resized.putalpha(resized.getchannel('A').point(lambda a:255 if a>=128 else 0))
    xy=(round(128-anchor[0]*scale),round(224-anchor[1]*scale))
    b=resized.getbbox()
    assert b and xy[0]+b[0]>0 and xy[1]+b[1]>0 and xy[0]+b[2]<256 and xy[1]+b[3]<256,(tile.size,scale,xy,b)
    frame=Image.new('RGBA',(256,256));frame.alpha_composite(resized,xy)
    a=np.array(frame);a[a[:,:,3]==0]=0
    return Image.fromarray(a),xy

def main():
    OUT.mkdir(exist_ok=True)
    states=[];calibration={};clips={}
    baseline=json.loads((ROOT/'review/baseline.json').read_text())['veld']['bodyStates']
    def add(key,frames,durations,loop=True,provenance='authored'):
        assert len(frames)==len(durations)
        paths=[]
        for i,im in enumerate(frames):
            p=OUT/f'frames/{key}/{i:03}.png';p.parent.mkdir(parents=True,exist_ok=True);im.save(p)
            paths.append(p.relative_to(OUT).as_posix())
        states.append(dict(id=key,frameFiles=paths,frameDurationsMs=durations,loop=loop,provenance=provenance))
        clips[key]=frames
    for direction in DIRS:
        walk=extract(f'veld-{direction}-v'+('3' if direction in ['north','south'] else '2'),3,2)
        heights=[tile.getbbox()[3]-tile.getbbox()[1] for tile,_ in walk]
        scale=140/max(heights)
        # One scale per directional sheet. Head/neck x anchors exclude swinging limbs.
        # Shared row contact lines retain vertical source differences between poses.
        grounds=[max(box[3]-2 for _,box in walk[row*3:(row+1)*3]) for row in range(2)]
        walk_frames=[];walk_at=[]
        for i,(tile,box) in enumerate(walk):
            anchor=(head_axis(tile),grounds[i//3]-box[1])
            frame,at=registered(tile,scale,anchor);walk_frames.append(frame);walk_at.append(dict(anchor=anchor,offset=at))
        add('walk-'+direction,walk_frames,baseline['walk-'+direction]['durations'])
        action=extract(f'veld-{direction}-actions-v1',4,3)
        scale_a=140/(action[0][0].getbbox()[3]-action[0][0].getbbox()[1])
        frames=[];action_at=[]
        # Stationary actions anchor the same planted boot, not the entire silhouette.
        # For axial views the source head axis is the actor's centreline.
        for i,(tile,box) in enumerate(action):
            b=tile.getbbox();mask=np.array(tile)[:,:,3]>0
            if direction in ['east','west']:
                floor=mask[max(b[1],b[3]-max(3,round(7/scale_a))):b[3]]
                _,xs=np.where(floor)
                ax=float(xs.max()-17/scale_a) if direction=='east' else float(xs.min()+17/scale_a)
            else:ax=head_axis(tile)
            anchor=(ax,b[3]);frame,at=registered(tile,scale_a,anchor)
            frames.append(frame);action_at.append(dict(anchor=anchor,offset=at))
        idle=[frames[0],frames[1],frames[0]]
        idle_ms=sum(baseline['idle-'+direction]['durations'])
        add('idle-'+direction,idle,[idle_ms*.45,idle_ms*.2,idle_ms*.35])
        # Shared full images ensure exact endpoint equality across each chain.
        lower=[frames[i] for i in [0,2,3,4,7]]
        rise=[frames[i] for i in [7,4,3,2,0]]
        k_ms=sum(baseline['kneel-'+direction]['durations'])
        s_ms=sum(baseline['stand-'+direction]['durations'])
        add('kneel-'+direction,lower,[k_ms*v for v in [.12,.18,.24,.24,.22]],False,'authored lowering; shared idle/work endpoints')
        add('stand-'+direction,rise,[s_ms*v for v in [.22,.24,.24,.18,.12]],False,'reverse lowering; shared work/idle endpoints')
        loop_name=f'veld-{direction}-sample-loop-v'+('2' if direction=='south' else '1')
        loop_path=ROOT/'sources'/f'{loop_name}.png'
        if loop_path.exists():
            work=extract(loop_name,3,2)
            # Calibrate the work sheet against its own supplied kneeling reference,
            # never against standing height. This keeps the crouch naturally low.
            ref_height=action[7][0].getbbox()[3]-action[7][0].getbbox()[1]
            work_scale=ref_height*scale_a/(work[0][0].getbbox()[3]-work[0][0].getbbox()[1])
            work_frames=[];work_at=[]
            for tile,box in work:
                b=tile.getbbox();anchor=(head_axis(tile),b[3])
                # Head aligns with the exact original kneeling endpoint; y uses boot contact.
                target_head=head_axis(action[7][0])*scale_a+action_at[7]['offset'][0]
                anchor=(head_axis(tile)+(128-target_head)/work_scale,b[3])
                im,at=registered(tile,work_scale,anchor);work_frames.append(im);work_at.append(dict(anchor=anchor,offset=at))
            # Use the authored work-loop entry in both connected chains.
            lower[-1]=work_frames[0];rise[0]=work_frames[0]
            for key,imgs in [('kneel-'+direction,lower),('stand-'+direction,rise)]:
                clips[key]=imgs
                for i,im in enumerate(imgs):im.save(OUT/f'frames/{key}/{i:03}.png')
            add('repair-'+direction,work_frames,baseline['repair-'+direction]['durations'])
        else:
            work_scale=None;work_at=[]
            add('repair-'+direction,[frames[7]],[sum(baseline['repair-'+direction]['durations'])],True,'temporary held pose; loop source pending')
        calibration[direction]=dict(walkScale=scale,walkGrounds=grounds,walk=walk_at,actionScale=scale_a,action=action_at,workScale=work_scale,work=work_at)
    pack=dict(name='Veld painted core candidate v2',frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,
        strideDistanceCells={'walk':.12,'walk-east':.11716216216216217,'walk-west':.12405405405405405},states=states,status='candidate; native integration pending')
    (OUT/'manifest.json').write_text(json.dumps(pack,indent=2)+'\n')
    (OUT/'provenance.json').write_text(json.dumps(dict(sources=RECORDS,calibration=calibration),indent=2)+'\n')
    board=Image.new('RGBA',(6*256,4*282),'#242b2e');draw=ImageDraw.Draw(board)
    for row,d in enumerate(DIRS):
        keys=['idle-'+d,'walk-'+d,'kneel-'+d,'repair-'+d,'stand-'+d,'idle-'+d]
        for col,key in enumerate(keys):
            index=2 if key.startswith(('walk','kneel','stand')) else 0
            im=clips[key][min(index,len(clips[key])-1)]
            board.alpha_composite(im,(col*256,row*282+22));draw.text((col*256+10,row*282+6),key,fill='white')
    board.save(OUT/'core-contact.png')
    for d in DIRS:
        assert np.array_equal(clips['idle-'+d][0],clips['kneel-'+d][0])
        assert np.array_equal(clips['kneel-'+d][-1],clips['repair-'+d][0])
        assert np.array_equal(clips['repair-'+d][0],clips['stand-'+d][0])
        assert np.array_equal(clips['stand-'+d][-1],clips['idle-'+d][0])
    print(json.dumps(dict(states=len(states),references=sum(len(s['frameFiles']) for s in states),sharedEndpointChecks=16,
                         maxSourceScale=max(max(v['walkScale'],v['actionScale'],v['workScale'] or 0) for v in calibration.values()))))

if __name__=='__main__':main()
