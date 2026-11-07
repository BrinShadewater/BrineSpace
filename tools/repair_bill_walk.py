"""Rebuild Bill's local side-view walk from existing, independently reconstructed pixels."""
from pathlib import Path
import json,hashlib,math
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/bill-walk-repair-2026-09-12'

def part(source,poly):
    mask=Image.new('L',source.size);ImageDraw.Draw(mask).polygon(poly,fill=255)
    a=np.array(source);a[np.array(mask)==0]=0
    return Image.fromarray(a)

def place(source,a,b,c,d):
    """Rigid source bone a->b onto destination c->d, nearest pixel sampling."""
    a,b,c,d=map(lambda v:np.array(v,dtype=float),(a,b,c,d));u=b-a;v=d-c
    angle=math.atan2(v[1],v[0])-math.atan2(u[1],u[0]);co,si=math.cos(angle),math.sin(angle)
    yy,xx=np.mgrid[:source.height,:source.width];dx,dy=xx+.5-c[0],yy+.5-c[1]
    sx=np.floor(dx*co+dy*si+a[0]).astype(int);sy=np.floor(-dx*si+dy*co+a[1]).astype(int)
    inside=(sx>=0)&(sy>=0)&(sx<source.width)&(sy<source.height);result=np.zeros((source.height,source.width,4),np.uint8)
    pixels=np.array(source);result[inside]=pixels[sy[inside],sx[inside]]
    return Image.fromarray(result)

def knee(hip,ankle,l1,l2,heading=1):
    hip=np.array(hip,float);ankle=np.array(ankle,float);v=ankle-hip;dist=np.linalg.norm(v);u=v/dist
    along=(l1*l1-l2*l2+dist*dist)/(2*dist);perp=math.sqrt(max(0,l1*l1-along*along))
    return hip+u*along+np.array([u[1],-u[0]])*perp*heading

def close_joint_pinholes(image):
    """Fill enclosed lower-body cutout gaps; preserve every existing opaque pixel."""
    from PIL import ImageOps
    pixels=np.array(image)
    solid=pixels[:,:,3]>0
    # Flood the transparent exterior with four-connectivity. Remaining transparent
    # islands are enclosed gaps, not the open space between the legs.
    exterior=Image.fromarray((solid*255).astype(np.uint8))
    exterior=ImageOps.expand(exterior,border=1,fill=0)
    ImageDraw.floodfill(exterior,(0,0),128)
    holes=np.array(exterior)[1:-1,1:-1]==0
    holes[:119]=False
    if int(holes.sum())>32:
        raise ValueError("Unexpected lower-body alpha gaps require visual review")
    yy,xx=np.nonzero(solid)
    for y,x in zip(*np.nonzero(holes)):
        nearest=np.argmin((yy-y)**2+(xx-x)**2)
        pixels[y,x]=pixels[yy[nearest],xx[nearest]]
    return Image.fromarray(pixels)

def repair_knee_contour(image, direction, phase):
    """Reviewed east passing-knee edge only; retain pose, palette and all other pixels."""
    if direction == 'east' and phase == 4:
        pixels=np.array(image)
        for y,old,last in [(138,109,108),(139,110,108),(142,108,107)]:
            actual=int(np.where(pixels[y,:,3]>0)[0].max())
            if actual != old:
                raise ValueError(f"East swing-knee source changed at row {y}: {actual} != {old}")
            edge=pixels[y,old].copy()
            pixels[y,last:old+1]=0
            pixels[y,last]=edge
        return Image.fromarray(pixels)
    if direction != 'east' or phase != 2:
        return image
    pixels=np.array(image)
    # Source-space endpoint pairs are intentionally explicit, not a cast-wide filter.
    # Preserve the existing dark edge when trimming; bridge the notch from the row above.
    for y,old,last in [(132,113,112),(133,114,112),(134,113,112),
                       (135,112,111),(137,110,111),(138,113,111),(140,113,112)]:
        actual=int(np.where(pixels[y,:,3]>0)[0].max())
        if actual != old:
            raise ValueError(f"East passing-knee source changed at row {y}: {actual} != {old}")
        edge=pixels[y,old].copy()
        if last < old:
            pixels[y,last:old+1]=0
            pixels[y,last]=edge
        else:
            pixels[y,old+1:last+1]=pixels[y-1,last]
    return Image.fromarray(pixels)


def repair_ankle_contour(image, direction, phase):
    """Remove the reviewed west contact-pose cutout spur, keeping the planted boot."""
    if direction != 'west' or phase != 0:
        return image
    pixels=np.array(image)
    edge=pixels[150,70].copy()
    if edge.tolist() != [28,26,31,255]:
        raise ValueError('West contact ankle source outline changed')
    for y,old,left in [(151,65,70),(152,64,70),(153,64,70),(154,65,70),
                       (155,65,69),(156,66,69),(157,67,68)]:
        actual=int(np.where(pixels[y,:,3]>0)[0].min())
        if actual != old:
            raise ValueError(f'West contact ankle source changed at row {y}: {actual} != {old}')
        pixels[y,:left]=0
        pixels[y,left]=edge
    return Image.fromarray(pixels)


def restore_upper_motion(frames, preserved):
    """Restore authored arm/shoulder phases without changing selected leg pixels."""
    source=preserved[0]
    result=[]
    for phase,body_index in enumerate([0,1,2,5,2,1]):
        frame=frames[phase].copy();body=preserved[body_index]
        bob=-1 if phase in (1,4) else 0
        shift=source.getbbox()[1]-body.getbbox()[1]+bob
        frame.paste((0,0,0,0),(0,0,184,119+bob))
        frame.alpha_composite(body.crop((0,0,184,119-shift+bob)),(0,shift))
        frame.paste(source.crop((0,0,184,60)),(0,bob))
        assert np.array_equal(np.array(frame)[119+bob:],np.array(frames[phase])[119+bob:])
        result.append(frame)
    return result

def build(source,direction='east'):
    recipes={
      'far':{'hip':(78,119),'knee':(63,143),'ankle':(50,158),
        'upper':[(71,122),(86,122),(83,136),(71,151),(55,143),(61,131)],
        'lower':[(55,135),(72,144),(65,155),(54,164),(42,160),(44,149)],
        'foot':[(42,152),(54,154),(55,160),(65,161),(71,165),(71,173),(52,173),(43,166)]},
      'near':{'hip':(90,114),'knee':(102,139),'ankle':(109,158),
        'upper':[(81,117),(101,117),(106,123),(111,135),(109,146),(94,151),(83,131)],
        'lower':[(93,134),(108,132),(116,151),(115,163),(102,170),(91,144)],
        'foot':[(100,153),(112,150),(116,155),(124,151),(132,153),(132,162),(117,170),(103,173),(99,162)]}}
    if direction=='west':
        recipes={
          'far':{'hip':(83,117),'knee':(72,141),'ankle':(63,159),
            'upper':[(75,119),(90,119),(88,131),(80,144),(70,150),(61,142),(66,128)],
            'lower':[(65,134),(81,140),(75,153),(67,166),(56,164),(56,151)],
            'foot':[(43,147),(53,148),(57,153),(68,155),(70,168),(62,172),(43,162),(39,156)]},
          'near':{'hip':(99,116),'knee':(111,141),'ankle':(125,158),
            'upper':[(90,119),(110,118),(114,132),(121,141),(116,150),(100,147),(90,133)],
            'lower':[(104,134),(118,136),(127,146),(133,156),(127,166),(113,163),(106,151)],
            'foot':[(122,149),(132,152),(138,154),(136,161),(124,172),(107,172),(107,164),(118,161)]}}
    torso=part(source,[(0,0),(184,0),(184,112),(106,112),(106,121),(102,126),(84,126),(81,119),(0,119)] if direction=='east' else [(0,0),(184,0),(184,121),(111,121),(108,127),(89,127),(87,120),(0,120)])
    # Contact/stance/toe-off occupy half a cycle; the other half lifts and returns.
    # Half-cycle stance travels 46 source pixels. The original durations are
    # asymmetric, so source x must be proportional to cumulative time, not index.
    durations=[170,130,150,170,130,150]
    path=[(23,172),(23-92*170/900,172),(23-92*300/900,172),(-23,169),(-10,166),(12,169)]
    layers={name:{k:part(source,r[k]) for k in ['upper','lower','foot']} for name,r in recipes.items()}
    frames=[];joints=[]
    for phase in range(6):
        out=Image.new('RGBA',source.size);poses={}
        bob=-1 if phase in [1,4] else 0
        for name in ['far','near']:
            r=recipes[name];step=(phase+(3 if name=='far' else 0))%6;x,sole=path[step]
            heading=1 if direction=='east' else -1
            hip=np.array(((84,120) if name=='far' else (90,117)) if direction=='east' else ((94,121) if name=='far' else (99,117)),float)
            hip[1]+=bob
            ankle=np.array((hip[0]+x*heading,158),float)
            angle=([-.25,-.25,-.25,-.1,-.3,-.25] if name=='far' else [.25,.25,.25,.1,-.05,.1])[step]
            vector=np.array([10*math.cos(angle),10*math.sin(angle)])
            foot=place(layers[name]['foot'],r['ankle'],np.array(r['ankle'])+[10,0],ankle,ankle+vector)
            ankle[1]+=sole-foot.getbbox()[3]
            l1=np.linalg.norm(np.array(r['knee'])-r['hip']);l2=np.linalg.norm(np.array(r['ankle'])-r['knee'])
            # Preserve lengths. A raised swing foot must bend the knee, not shorten the leg.
            if np.linalg.norm(ankle-hip)>l1+l2-.2:
                ankle=hip+(ankle-hip)/np.linalg.norm(ankle-hip)*(l1+l2-.2)
            bend=knee(hip,ankle,l1,l2,heading)
            upper=place(layers[name]['upper'],r['hip'],r['knee'],hip,bend)
            upper.paste((0,0,0,0),(0,0,184,119+bob))
            out.alpha_composite(upper)
            out.alpha_composite(place(layers[name]['lower'],r['knee'],r['ankle'],bend,ankle))
            foot=place(layers[name]['foot'],r['ankle'],np.array(r['ankle'])+[10,0],ankle,ankle+vector)
            out.alpha_composite(foot)
            poses[name]={'phase':step,'hip':hip.tolist(),'knee':bend.tolist(),'ankle':ankle.tolist(),'soleTarget':sole,'soleActual':foot.getbbox()[3]}
        out.alpha_composite(torso,(0,bob))
        out.paste(source.crop((0,0,184,119)),(0,bob))
        frames.append(repair_ankle_contour(repair_knee_contour(close_joint_pinholes(out),direction,phase),direction,phase));joints.append(poses)
    return frames,layers,torso,joints

def legacy_main():
    OUT.mkdir(exist_ok=True)
    # Never feed the repaired production frames back into their own source rig.
    from rebuild_bill_art import base_frames, HelmetRebaker, WATER
    preserved=base_frames(repair_walk=False)
    helmets=HelmetRebaker(None)
    audit={}
    manifests={variant:{'name':'bill-walk-candidate-'+variant,'frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'precomposed':True,'strideDistanceCells':{'walk':92*65.28/148/384},'states':[]} for variant in ['bare','helmet']}
    for direction in ['east','west']:
        source=preserved[f'character/major-bill-v2/frames/walk-{direction}/frame_000.png']
        src=OUT/f'{direction}-reconstructed-source.png';source.save(src)
        frames,layers,torso,joints=build(source,direction)
        authored=[preserved[f'character/major-bill-v2/frames/walk-{direction}/frame_{i:03}.png'] for i in range(6)]
        frames=restore_upper_motion(frames,authored)
        from build_bill_limb_candidate import repair as repair_limb_surfaces
        frames=repair_limb_surfaces(direction,source,frames)
        registration=json.loads((WATER/'equipment/dry'/f'bill-walk-{direction}'/'registration.json').read_text())
        overlay=helmets.overlay(Path(registration['overlay']).parent.name)
        equipped=[]
        for i,im in enumerate(frames):
            bob=-1 if i in [1,4] else 0
            pos=np.array(registration['frames'][0]['overlayTopLeft'])*2
            pos[1]+=bob
            gear=im.copy();gear.alpha_composite(overlay,tuple(pos));gear.save(OUT/f'{direction}-helmet-{i:02}.png');equipped.append(gear)
        for variant,suffix in [('bare','candidate'),('helmet','helmet')]:
            manifests[variant]['states'].append({'id':'walk-'+direction,'frameFiles':[f'{direction}-{suffix}-{i:02}.png' for i in range(6)],'frameDurationsMs':[170,130,150,170,130,150],'loop':True})
        for i,im in enumerate(frames):im.save(OUT/f'{direction}-candidate-{i:02}.png')
        sheet=Image.new('RGBA',(6*368,390),'#26383c');draw=ImageDraw.Draw(sheet)
        for i,im in enumerate(frames):
            sheet.alpha_composite(im.resize((368,368),Image.Resampling.NEAREST),(i*368,22));draw.text((i*368+8,4),str(i)+' / '+('near stance' if i<3 else 'far stance'),fill='white')
        sheet.save(OUT/f'{direction}-candidate-sheet.png')
        sheet=Image.new('RGBA',(8*184,184),'#26383c')
        for i,im in enumerate([source,torso]+[layers[n][p] for n in ['far','near'] for p in ['upper','lower','foot']]):sheet.alpha_composite(im,(i*184,0))
        sheet.save(OUT/f'{direction}-source-layers.png')
        frames[0].save(OUT/f'{direction}-candidate.gif',save_all=True,append_images=frames[1:],duration=[170,130,150,170,130,150],loop=0,disposal=2)
        (OUT/f'{direction}-provenance.json').write_text(json.dumps({'source':str(src.relative_to(ROOT)),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'method':'Existing pixel regions articulated with rigid nearest-sampled bones; no recoloring or mirroring','joints':joints},indent=2)+'\n')
        original=np.array(source);palette=set(map(tuple,original[original[:,:,3]>0,:3]))
        ground_errors=[];plant_drift=[];identity=True;new_colors=set()
        for i,frame in enumerate(frames):
            pixels=np.array(frame);bob=-1 if i in [1,4] else 0
            identity &= np.array_equal(pixels[:60+bob],original[-bob:60])
            new_colors |= set(map(tuple,pixels[pixels[:,:,3]>0,:3]))-palette
            for pose in joints[i].values():
                if pose['phase']<3:ground_errors.append(pose['soleActual']-pose['soleTarget'])
        for name,phases in [('near',[0,1,2]),('far',[3,4,5])]:
            times=[0,170,300,450,620,750];heading=1 if direction=='east' else -1
            contacts=[joints[i][name]['ankle'][0]+heading*92*times[i]/900 for i in phases]
            plant_drift.append(max(contacts)-min(contacts))
        audit[direction]={'headPixelsPreservedWithOnePixelBob':bool(identity),'newColors':len(new_colors),'stanceSoleErrorsSourcePixels':ground_errors,'stanceAnchorDriftSourcePixels':plant_drift,'proposedStrideCells':92*65.28/148/384}
    (OUT/'candidate-checks.json').write_text(json.dumps(audit,indent=2)+'\n')
    for variant,data in manifests.items():(OUT/(variant+'-manifest.json')).write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(audit))
    print('Twelve repaired poses and registered source-layer reviews written; production files untouched by this command.')
def main():
    # Keep the established review command aligned with selected runtime art.
    # build()/legacy_main() remain available to reproduce historical rig studies.
    from build_bill_connected_walk import build as export_connected
    export_connected(OUT)

if __name__=='__main__':main()
