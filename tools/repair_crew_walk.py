"""Character-specific local gait rigs using independently reconstructed source pixels."""
from pathlib import Path
import json
import math
import hashlib
import base64
import io
import copy
import numpy as np
from PIL import Image, ImageDraw
from repair_bill_walk import part, place, knee

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'character/crew-gait-v2/review'
VELD_EAST={
    'direction':'east','sourceFrame':2,'travel':38,'durations':[170,130,150,170,130,150],
    'torso':[(0,0),(184,0),(184,119),(112,119),(110,123),(102,124),(96,121),(85,125),(80,119),(0,119)],
    'far':{'hip':(83,118),'knee':(70,140),'ankle':(61,158),'targetHip':(84,120),
        'upper':[(76,116),(88,118),(83,133),(76,146),(65,147),(61,138),(69,124)],
        'lower':[(63,135),(77,142),(72,152),(67,162),(56,165),(52,157)],
        'foot':[(54,153),(65,156),(66,162),(75,163),(80,167),(78,172),(64,172),(54,165)]},
    'near':{'hip':(90,113),'knee':(106,136),'ankle':(114,157),'targetHip':(90,117),
        'upper':[(82,111),(99,111),(105,122),(111,138),(107,147),(93,149),(83,131)],
        'lower':[(98,134),(109,133),(116,149),(120,159),(109,166),(101,151)],
        'foot':[(108,151),(118,148),(121,153),(127,151),(133,155),(133,162),(117,169),(109,172),(104,163)]}}
VELD_WEST={
    'direction':'west','sourceFrame':1,'travel':38,'durations':[170,130,150,170,130,150],
    'torso':[(0,0),(184,0),(184,119),(110,119),(105,125),(88,125),(82,119),(0,119)],
    'far':{'hip':(87,118),'knee':(77,140),'ankle':(69,160),'targetHip':(87,120),
        'upper':[(79,113),(94,116),(90,130),(84,143),(78,148),(66,143),(71,128)],
        'lower':[(70,134),(83,139),(79,151),(74,164),(62,165),(61,154)],
        'foot':[(53,159),(66,157),(72,157),(75,164),(73,172),(60,172),(49,168),(49,162)]},
    'near':{'hip':(97,117),'knee':(110,139),'ankle':(121,158),'targetHip':(97,119),
        'upper':[(90,115),(105,115),(111,129),(118,142),(113,150),(99,144),(91,133)],
        'lower':[(104,133),(117,136),(124,147),(127,159),(118,167),(109,160),(105,148)],
        'foot':[(116,152),(127,153),(132,159),(129,166),(117,173),(104,173),(104,166),(115,162)]}}
BRANFORTH_EAST={
    'direction':'east','sourceFrame':0,'travel':38,'durations':[170,130,150,170,130,150],
    'torso':[(0,0),(184,0),(184,119),(113,119),(109,125),(97,122),(84,125),(79,119),(0,119)],
    'far':{'hip':(83,117),'knee':(70,139),'ankle':(61,156),'targetHip':(84,121),
        'upper':[(76,114),(89,116),(85,131),(77,145),(66,146),(60,137),(69,123)],
        'lower':[(62,132),(78,140),(73,151),(67,161),(56,163),(52,154)],
        'foot':[(53,151),(64,151),(67,158),(73,160),(80,165),(78,171),(64,170),(54,162)]},
    'near':{'hip':(91,114),'knee':(104,138),'ankle':(113,157),'targetHip':(91,118),
        'upper':[(82,111),(99,111),(107,123),(113,138),(108,148),(95,148),(84,131)],
        'lower':[(97,133),(111,135),(116,148),(121,159),(108,169),(100,151)],
        'foot':[(105,153),(116,151),(120,155),(129,154),(134,159),(132,165),(115,171),(104,171),(103,162)]}}
BRANFORTH_WEST={
    'direction':'west','sourceFrame':1,'travel':38,'durations':[170,130,150,170,130,150],
    'torso':[(0,0),(184,0),(184,119),(114,119),(108,125),(87,125),(81,119),(0,119)],
    'far':{'hip':(84,117),'knee':(75,140),'ankle':(64,160),'targetHip':(86,121),
        'upper':[(77,113),(91,116),(85,132),(81,144),(73,149),(63,142),(68,128)],
        'lower':[(67,134),(82,139),(75,154),(68,166),(56,166),(57,151)],
        'foot':[(49,160),(59,157),(68,157),(74,164),(73,171),(60,172),(46,167),(46,162)]},
    'near':{'hip':(96,116),'knee':(110,138),'ankle':(124,158),'targetHip':(98,120),
        'upper':[(88,113),(105,114),(113,129),(121,142),(115,152),(100,146),(91,133)],
        'lower':[(104,132),(119,136),(127,148),(132,159),(121,167),(109,159),(105,147)],
        'foot':[(118,151),(129,153),(136,158),(131,166),(119,173),(106,173),(105,165),(116,161)]}}
RIGS={('veld','walk-east'):VELD_EAST,('veld','walk-west'):VELD_WEST,('branforth','walk-east'):BRANFORTH_EAST,('branforth','walk-west'):BRANFORTH_WEST}
MARSH_EAST={
    'direction':'east','sourceFrame':0,'travel':36,'durations':[150]*6,
    'torso':[(0,0),(184,0),(184,119),(108,119),(102,125),(86,125),(80,119),(0,119)],
    'far':{'hip':(83,117),'knee':(74,140),'ankle':(69,157),'targetHip':(84,122),
        'upper':[(76,113),(90,115),(88,130),(82,145),(73,149),(64,141),(67,127)],
        'lower':[(65,134),(81,138),(79,150),(74,162),(62,164),(60,152)],
        'foot':[(61,151),(72,152),(74,157),(80,159),(86,163),(83,171),(70,171),(59,164)]},
    'near':{'hip':(93,116),'knee':(101,138),'ankle':(105,158),'targetHip':(94,121),
        'upper':[(86,111),(101,113),(105,126),(109,140),(104,148),(91,145),(85,130)],
        'lower':[(95,133),(108,133),(111,148),(114,161),(102,166),(95,152)],
        'foot':[(100,153),(111,153),(113,160),(119,160),(124,165),(122,171),(104,172),(97,166)]}}
from marsh_east_geometry import apply as apply_marsh_east_geometry
apply_marsh_east_geometry(MARSH_EAST)
MARSH_RUN_EAST=copy.deepcopy(MARSH_EAST)
MARSH_RUN_EAST.update({'sourceClip':'walk-east','travel':48,'durations':[100]*6,
    'solePath':[172,172,167,160,154,164],'bodyBob':[0,-2,-5,0,-2,-5],'stancePhases':2})
MARSH_RUN_EAST['far']['targetHip']=(85,110)
MARSH_RUN_EAST['near']['targetHip']=(95,110)
RIGS.update({('marsh','walk-east'):MARSH_EAST,('marsh','run-east'):MARSH_RUN_EAST})
MARSH_WEST={
    'direction':'west','sourceFrame':0,'travel':36,'durations':[150]*6,
    'torso':[(0,0),(184,0),(184,119),(110,119),(106,125),(87,125),(81,119),(0,119)],
    'far':{'hip':(99,117),'knee':(105,138),'ankle':(114,158),'targetHip':(99,123),
        'upper':[(92,112),(105,114),(109,128),(115,141),(107,149),(96,143),(90,129)],
        'lower':[(99,132),(111,133),(117,147),(121,160),(110,167),(102,152)],
        'foot':[(108,152),(120,153),(125,161),(121,168),(110,172),(99,172),(99,165),(109,161)]},
    'near':{'hip':(89,116),'knee':(83,139),'ankle':(77,159),'targetHip':(89,123),
        'upper':[(83,110),(97,113),(95,130),(92,144),(83,150),(74,143),(76,128)],
        'lower':[(77,133),(90,135),(88,151),(82,163),(70,164),(70,153)],
        'foot':[(70,153),(82,153),(84,164),(80,172),(65,172),(58,168),(59,162),(70,161)]}}
from marsh_west_geometry import apply as apply_marsh_west_geometry
apply_marsh_west_geometry(MARSH_WEST)
MARSH_RUN_WEST=copy.deepcopy(MARSH_WEST)
MARSH_RUN_WEST.update({'sourceClip':'walk-west','travel':48,'durations':[100]*6,
    'solePath':[172,172,167,160,154,164],'bodyBob':[0,-2,-5,0,-2,-5],'stancePhases':2})
MARSH_RUN_WEST['far']['targetHip']=(99,110)
MARSH_RUN_WEST['near']['targetHip']=(89,110)
RIGS.update({('marsh','walk-west'):MARSH_WEST,('marsh','run-west'):MARSH_RUN_WEST})
SELECTED_GAITS={('veld','walk-east'),('veld','walk-west'),('branforth','walk-east'),('branforth','walk-west'),('marsh','walk-east'),('marsh','run-east')}
SELECTED_GAITS.update({('marsh','walk-west'),('marsh','run-west')})

# Front/back views foreshorten limbs in image space; the side-view IK rig is
# inappropriate here. Each side keeps its original costume pixels and width.
for _direction in ['north','south']:
    for _state in ['walk','run']:
        _run=_state=='run'
        RIGS['marsh',_state+'-'+_direction]={
            'projection':'axial','direction':_direction,'sourceClip':'walk-'+_direction,
            'sourceFrame':0,'travel':48 if _run else 36,'durations':[100 if _run else 150]*6,
            'bodyBob':[0,-2,-4,0,-2,-4] if _run else [0,-1,0,0,-1,0],
            'solePath':([172,166,157,154,151,164] if _run else [172,168,164,160,156,164]),
            'legs':{'left':{'box':[68,121,93,184]},'right':{'box':[93,121,116,184]}}}
SELECTED_GAITS.update({('marsh','walk-north'),('marsh','run-north'),
                       ('marsh','walk-south'),('marsh','run-south')})


def build_axial(source,rig):
    """Preserve original leg pixels under explicit projected length changes.

    These are foreshortening controls, not side-view bone/contact measurements.
    Never report their image-space coordinates as a world-space planting proof.
    """
    torso=source.copy()
    for spec in rig['legs'].values():
        torso.paste((0,0,0,0),tuple(spec['box']))
    lower_top=max(spec['box'][1] for spec in rig['legs'].values())
    if torso.crop((0,lower_top,source.width,source.height)).getbbox() is not None:
        raise ValueError('Axial leg masks leave stationary lower-body pixels')
    layers={name:source.crop(tuple(spec['box'])) for name,spec in rig['legs'].items()}
    frames=[];records=[]
    for phase in range(6):
        canvas=Image.new('RGBA',source.size);poses={};bob=rig['bodyBob'][phase]
        for name,offset in [('left',0),('right',3)]:
            step=(phase+offset)%6
            # Reverse progression for travel away from the camera, without
            # mirroring either character view or exchanging costume sides.
            if rig['direction']=='north':step=(3-step)%6
            sole=rig['solePath'][step]
            tile=layers[name];bounds=tile.getbbox()
            top=rig['legs'][name]['box'][1]+bob
            h=sole-top
            # Crop transparent tails before setting the projected sole position.
            tile=tile.crop((0,0,tile.width,bounds[3]))
            tile=tile.resize((tile.width,h),Image.Resampling.NEAREST)
            x=rig['legs'][name]['box'][0]
            canvas.alpha_composite(tile,(x,top))
            poses[name]={'phase':step,'soleActual':top+tile.getbbox()[3],
                         'soleTarget':sole,'projectedLength':h}
        canvas.alpha_composite(torso,(0,bob))
        frames.append(canvas);records.append(poses)
    return frames,records


def build(source,rig):
    if rig.get('projection')=='axial':return build_axial(source,rig)
    travel=rig['travel']; half=travel/2; durations=rig['durations']; total=sum(durations)
    if len(durations)!=6 or sum(durations[:3])!=sum(durations[3:]):
        raise ValueError('This rig requires six phases with equal-duration half cycles')
    path=[(half,172),(half-2*travel*durations[0]/total,172),(half-2*travel*sum(durations[:2])/total,172),(-half,169),(-half*.43,166),(half*.52,169)]
    if 'solePath' in rig:path=[(pose[0],rig['solePath'][i]) for i,pose in enumerate(path)]
    torso=part(source,rig['torso'])
    layers={name:{kind:part(source,rig[name][kind]) for kind in ['upper','lower','foot']} for name in ['far','near']}
    for name in ['far','near']:
        center=np.array(rig[name]['knee'])
        layers[name]['joint']=part(source,[(center+[7*math.cos(a),7*math.sin(a)]).tolist() for a in np.linspace(0,2*math.pi,20)])
    frames=[]; records=[]
    for phase in range(6):
        canvas=Image.new('RGBA',source.size); poses={}; bob=rig.get('bodyBob',[0,-1,0,0,-1,0])[phase]
        heading=1 if rig['direction']=='east' else -1
        for name in ['far','near']:
            r=rig[name]; step=(phase+(3 if name=='far' else 0))%6
            x,sole=path[step]; hip=np.array(r['targetHip'],float)+[0,bob]
            ankle=np.array([hip[0]+heading*x,158.0])
            angle=([-.22,-.22,-.22,-.1,-.3,-.2] if name=='far' else [.18,.18,.18,.1,-.05,.1])[step]
            vec=np.array([10*math.cos(angle),10*math.sin(angle)])
            foot=place(layers[name]['foot'],r['ankle'],np.array(r['ankle'])+[10,0],ankle,ankle+vec)
            ankle[1]+=sole-foot.getbbox()[3]
            l1=np.linalg.norm(np.array(r['knee'])-r['hip']); l2=np.linalg.norm(np.array(r['ankle'])-r['knee'])
            l1*=rig.get('legLengthScale',1.0);l2*=rig.get('legLengthScale',1.0)
            distance=np.linalg.norm(ankle-hip)
            if distance>l1+l2-.2: ankle=hip+(ankle-hip)/distance*(l1+l2-.2)
            bend=knee(hip,ankle,l1,l2,heading)
            canvas.alpha_composite(place(layers[name]['upper'],r['hip'],r['knee'],hip,bend))
            canvas.alpha_composite(place(layers[name]['lower'],r['knee'],r['ankle'],bend,ankle))
            upper_delta=math.atan2(*(bend-hip)[::-1])-math.atan2(*(np.array(r['knee'])-r['hip'])[::-1])
            lower_delta=math.atan2(*(ankle-bend)[::-1])-math.atan2(*(np.array(r['ankle'])-r['knee'])[::-1])
            joint_angle=(upper_delta+lower_delta)/2
            joint_vector=np.array([10*math.cos(joint_angle),10*math.sin(joint_angle)])
            canvas.alpha_composite(place(layers[name]['joint'],r['knee'],np.array(r['knee'])+[10,0],bend,bend+joint_vector))
            foot=place(layers[name]['foot'],r['ankle'],np.array(r['ankle'])+[10,0],ankle,ankle+vec)
            canvas.alpha_composite(foot)
            poses[name]={'phase':step,'hip':hip.tolist(),'knee':bend.tolist(),'ankle':ankle.tolist(),'soleTarget':sole,'soleActual':foot.getbbox()[3]}
        canvas.alpha_composite(torso,(0,bob))
        canvas.paste(source.crop((0,0,184,rig.get('torsoCutY',119))),(0,bob))
        frames.append(canvas);records.append(poses)
    return frames,records


def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--actor',choices=['veld','branforth','marsh'],default='veld')
    parser.add_argument('--state',choices=['walk','run'],default='walk')
    parser.add_argument('--direction',choices=['east','west','north','south'],default='east')
    parser.add_argument('--cleaned-legs',action='store_true',help='Review generated seam repair below the preserved original torso')
    args=parser.parse_args()
    if args.cleaned_legs and (args.actor,args.direction)!=('veld','east'):parser.error('The generated lower-leg study is Veld east only')
    clip=args.state+'-'+args.direction
    if (args.actor,clip) not in RIGS:parser.error('This character/clip rig is not authored yet')
    rig=RIGS[args.actor,clip]
    from rebuild_human_crew_art import base_frames,PACKS
    if args.actor=='marsh':
        from rebuild_marsh_art import source_clips
        source=source_clips()[rig.get('sourceClip',clip)][rig['sourceFrame']]
    else:source=base_frames(args.actor,repair_walk=False)[f'character/{PACKS[args.actor]}/frames/{clip}/frame_{rig["sourceFrame"]:03}.png']
    frames,joints=build(source,rig)
    source_edit=None
    if args.cleaned_legs:
        import rebuild_bill_art as shared
        source_edit=ROOT/'character/crew-gait-v2/sources/veld-walk-east-rig-cleanup-02.png'
        raw=shared.chroma(source_edit)
        # This wide edit has ample empty space between six equally spaced poses.
        crops=[]
        for i in range(6):
            tile=raw.crop((i*raw.width//6,0,(i+1)*raw.width//6,raw.height))
            crops.append(tile.crop(tile.getbbox()))
        scale=140/float(np.median([crop.height for crop in crops]))
        colors=sorted(set(tuple(c) for c in np.array(source)[np.array(source)[:,:,3]>0,:3].tolist()))
        palette=Image.new('P',(1,1));palette.putpalette([v for color in colors for v in color]+list(colors[0])*(256-len(colors)))
        for i,crop in enumerate(crops):
            head=crop.crop((0,0,crop.width,round(20/scale))).getbbox()
            head_center=(head[0]+head[2])/2
            dense=shared.binary(crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.BOX),True)
            alpha=dense.getchannel('A')
            dense=dense.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');dense.putalpha(alpha)
            normalized=Image.new('RGBA',(184,184));normalized.alpha_composite(dense,(round(92-head_center*scale),172-dense.height))
            normalized.paste(frames[i].crop((0,0,184,132)),(0,0))
            frames[i]=normalized
    label=args.direction if args.state=='walk' else clip
    out=OUT/('veld-east-cleaned-02' if args.cleaned_legs else f'{args.actor}-{label}-local-01');out.mkdir(parents=True,exist_ok=True)
    source.save(out/'reconstructed-source.png')
    sheet=Image.new('RGB',(184*6,208),'#293b40')
    for i,frame in enumerate(frames):
        frame.save(out/f'{i:03}.png');sheet.paste(frame,(i*184,20),frame)
        ImageDraw.Draw(sheet).text((i*184+4,3),str(i),fill='white')
    sheet.save(out/'contact.png')
    elapsed=np.r_[0,np.cumsum(rig['durations'])[:-1]]
    cycle_travel=rig['travel']*2
    world_travel=elapsed/sum(rig['durations'])*cycle_travel*(1 if args.direction=='east' else -1)
    checks={}
    stance=rig.get('stancePhases',3)
    for leg,phases in ([] if rig.get('projection')=='axial' else [('near',list(range(stance))),('far',list(range(3,3+stance)))]):
        contact=[joints[i][leg]['ankle'][0]+world_travel[i] for i in phases]
        checks[leg+'StanceDriftPx']=float(max(contact)-min(contact))
        checks[leg+'SoleErrorPx']=max(abs(joints[i][leg]['soleActual']-172) for i in phases)
    if rig.get('projection')=='axial':
        checks['projectedSoleErrorPx']=max(abs(p['soleActual']-p['soleTarget']) for row in joints for p in row.values())
    assert max(checks.values())<=1, checks
    selected=not args.cleaned_legs and (args.actor,clip) in SELECTED_GAITS
    (out/'rig.json').write_text(json.dumps({'status':'selected_motion_revision' if selected else 'candidate','sourcePixelSha256':hashlib.sha256(source.tobytes()).hexdigest(),'recipe':rig,'joints':joints,'strideDistanceCells':cycle_travel*65.28/148/384,'guideChecks' if args.cleaned_legs else 'checks':checks,'editedSource':None if source_edit is None else {'path':source_edit.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(source_edit.read_bytes()).hexdigest(),'scale':scale,'region':'y >= 132; original upper body and rigged thighs restored'}},indent=2)+'\n')
    def uri(im):
        stream=io.BytesIO();im.save(stream,format='PNG')
        return 'data:image/png;base64,'+base64.b64encode(stream.getvalue()).decode()
    page='''<!doctype html><meta charset="utf-8"><title>Veld local walk study</title>
<style>body{background:#24343b;color:#ddd;font:16px system-ui}canvas{background:#293b40;image-rendering:pixelated}input{width:500px}</style>
<h1>Veld — alternating walk study</h1><p>Candidate only. Both legs alternate stance and swing. Moving playback uses the proposed stride; scrub to inspect knee seams and planted feet. Left: source-density travel. Middle: stationary source density. Right: station scale.</p>
<button id="play">Pause</button><input id="scrub" type="range" min="0" max="3599" value="0"><span id="stamp"></span><br><canvas id="view" width="700" height="280"></canvas>
<script>const frames=FRAMES.map(src=>{let i=new Image();i.src=src;return i});const durations=[170,130,150,170,130,150];let elapsed=0,last=performance.now(),playing=true;
play.onclick=()=>{playing=!playing;play.textContent=playing?'Pause':'Play'};scrub.oninput=()=>{elapsed=Number(scrub.value);playing=false;play.textContent='Play'};
function draw(now){if(playing)elapsed=(elapsed+now-last)%3600;last=now;let time=elapsed%900,n=0;while(n<5&&time>=durations[n])time-=durations[n++];let ctx=view.getContext('2d');ctx.clearRect(0,0,700,280);ctx.imageSmoothingEnabled=false;ctx.fillStyle='#65777a';for(let x=0;x<700;x+=32)ctx.fillRect(x,240,1,10);if(frames[n].complete){ctx.drawImage(frames[n],60+elapsed/900*76-92,240-172);ctx.drawImage(frames[n],480-92,240-172);const s=65.28/148;ctx.drawImage(frames[n],620-92*s,240-172*s,184*s,184*s)}scrub.value=elapsed;stamp.textContent='frame '+n+' / '+(elapsed/1000).toFixed(2)+'s';requestAnimationFrame(draw)}requestAnimationFrame(draw);</script>'''.replace('FRAMES',json.dumps([uri(frame) for frame in frames]))
    if selected:page=page.replace('Candidate only.','Selected local source-pixel repair. Native validation is recorded separately.').replace('proposed stride','selected stride')
    page=page.replace('Veld local walk study',f'{args.actor.title()} {args.direction} {args.state} study')
    page=page.replace('[170,130,150,170,130,150]',json.dumps(rig['durations']))
    page=page.replace('900',str(sum(rig['durations']))).replace('/'+str(sum(rig['durations']))+'*76','/'+str(sum(rig['durations']))+'*'+str(cycle_travel))
    page=page.replace('Veld — alternating walk study',f'{args.actor.title()} {args.direction} — alternating {args.state} study')
    if args.direction=='west':page=page.replace(f'60+elapsed/{sum(rig["durations"])}*{cycle_travel}-92',f'360-elapsed/{sum(rig["durations"])}*{cycle_travel}-92')
    if rig.get('projection')=='axial':
        sign='-' if args.direction=='north' else '+'
        page=page.replace(f'60+elapsed/{sum(rig["durations"])}*{cycle_travel}-92,240-172',
                          f'160-92,205-172{sign}(elapsed/{sum(rig["durations"])}*{cycle_travel})%40')
        page=page.replace('Both legs alternate stance and swing.',
                          'Front/back projected leg lengths alternate. Sole checks measure image-space registration only.')
    (out/'motion.html').write_text(page,encoding='utf-8')
    print(json.dumps(checks))
    print(out.relative_to(ROOT))


if __name__=='__main__':main()
