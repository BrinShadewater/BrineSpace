"""Rebuild the complete Bill revision from preserved authored sources, never generators.

The source contract records the real native consumer, including composed turns and
registered endpoints. Old art is read-only. New output lives in major-bill-v3.
"""
from pathlib import Path
import argparse, copy, hashlib, importlib.util, json, re
import numpy as np
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
WATER=ROOT/'character/crew-underwater-v1'
CONTRACT=ROOT/'tools/bill-art-source-contract.json'
OUT=ROOT/'character/major-bill-v3'
QA=ROOT/'output/bill-full-replacement-2026-09-12'
SOURCE_HASHES={}
OPS={}

def read(path):
    path=Path(path).resolve()
    SOURCE_HASHES[path.relative_to(ROOT).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
    return json.loads(path.read_text())

def image(path):
    path=Path(path).resolve()
    SOURCE_HASHES[path.relative_to(ROOT).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
    return Image.open(path).convert('RGBA')

def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    SOURCE_HASHES[path.relative_to(ROOT).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
    return m

def binary(im,fringe=False):
    a=np.array(im);mask=a[:,:,3]<128
    if fringe:
        r,g,b=a[:,:,:3].astype(float).transpose(2,0,1)
        mask|=(r>g*1.25)&(b>g*1.25)&(r>40)&(b>40)
    a[mask]=0;a[~mask,3]=255
    return Image.fromarray(a)

def chroma(path):
    im=image(path);a=np.array(im);r,g,b=a[:,:,:3].astype(int).transpose(2,0,1)
    a[(r>g+35)&(b>g+35)]=0
    return Image.fromarray(a)

def sig(im):
    a=np.array(im);a[a[:,:,3]==0]=0
    return hashlib.sha256(a.tobytes()).hexdigest()

def base_frames(repair_walk=True):
    pack=ROOT/'character/major-bill-v2'
    b=module(pack/'build_pack.py','bill_base_builder')
    b.SIZE=184;b.PIVOT=(92,172)
    a={}
    for state in b.STATES:
        if state=='stand-east':a[state]=list(reversed(a['kneel-east']));continue
        name='cleanup-'+state if state in b.CLEANUP else state
        image(pack/'generated'/f'{name}.png')
        target=50 if state.startswith('repair') else 68 if state in ['run-east','run-west'] else 74
        a[state]=b.extract(name,target=target*2)
        if state in b.POSE_ORDER:a[state]=[a[state][i] for i in b.POSE_ORDER[state]]
    def endpoints():
        a['kneel-east'][0]=a['idle-east'][0].copy();a['kneel-east'][-1]=a['repair-east'][0].copy()
        a['stand-east']=list(reversed(a['kneel-east']))
        a['interact-east'][0]=a['idle-east'][0].copy();a['interact-east'][-1]=a['idle-east'][0].copy()
        a['repair-east'][-1]=a['repair-east'][0].copy()
    endpoints()
    old=read(pack/'final/manifest.json');colors=set()
    for e in old['states']:
        for path in e['frameFiles']:
            px=np.array(image((pack/'final'/path).resolve()));colors.update(map(tuple,px[px[:,:,3]>0,:3].tolist()))
    colors=sorted(colors);assert len(colors)==64
    pal=Image.new('P',(1,1));pal.putpalette([c for rgb in colors for c in rgb]+list(colors[0])*(256-len(colors)))
    for key,poses in a.items():
        for i,im in enumerate(poses):
            # Preserve the existing world-area speckle rule at twice density.
            px=np.array(im);mask=px[:,:,3]>0;seen=np.zeros(mask.shape,bool)
            for y,x in zip(*np.where(mask)):
                if seen[y,x]:continue
                stack=[(int(y),int(x))];component=[];seen[y,x]=True
                while stack:
                    cy,cx=stack.pop();component.append((cy,cx))
                    for dy,dx in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
                        ny,nx=cy+dy,cx+dx
                        if 0<=ny<184 and 0<=nx<184 and mask[ny,nx] and not seen[ny,nx]:seen[ny,nx]=True;stack.append((ny,nx))
                if len(component)<=8:
                    for cy,cx in component:px[cy,cx]=0
            im=Image.fromarray(px);out=im.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE).convert('RGBA');out.putalpha(im.getchannel('A'))
            a[key][i]=binary(out)
    endpoints()
    # Accepted motion-v4 treatment, copied as explicit local pixel reuse rules.
    for key in [k for k in a if k.startswith('idle-')]:
        base=a[key][0].copy()
        for i,rise in enumerate([0,0,1,1,0,0]):
            im=base.copy()
            if rise:
                im.paste((0,0,0,0),(0,0,184,110));im.alpha_composite(base.crop((0,0,184,110)),(0,-1));im.paste(base.crop((0,109,184,110)),(0,109))
            a[key][i]=im
    for key in [k for k in a if k.startswith('walk-')]:
        base=a[key][0].copy();top=base.getbbox()[1];cut=top+34
        for i,src in enumerate(a[key]):
            dy=src.getbbox()[1]-top;im=src.copy();im.paste((0,0,0,0),(0,0,184,cut+dy));im.alpha_composite(base.crop((0,0,184,cut)),(0,dy));a[key][i]=im
    base=a['idle-east'][0]
    for i in range(1,5):
        src=a['interact-east'][i];dy=base.getbbox()[1]-src.getbbox()[1]
        im=Image.new('RGBA',(184,184));im.alpha_composite(src,(0,dy));im.paste(base.crop((0,0,184,59)),(0,0));im.paste(base.crop((0,119,184,184)),(0,119));a['interact-east'][i]=im
    if repair_walk:
        walker=module(ROOT/'tools/repair_bill_walk.py','bill_local_walk')
        for direction in ['east','west']:
            key='walk-'+direction
            a[key]=walker.build(a[key][0],direction)[0]
    return {(pack/'frames'/key/f'frame_{i:03}.png').relative_to(ROOT).as_posix():im for key,poses in a.items() for i,im in enumerate(poses)}

class SourceRebaker:
    def __init__(self):
        self.cache=base_frames();self.rows={};self.regs={};self.match_count=0
        self.life=module(ROOT/'character/crew-life-v1/build_pack.py','bill_life_builder')
        self.actions=module(ROOT/'character/crew-actions-v1/build_pack.py','bill_actions_builder')
        self.construction=module(ROOT/'character/crew-construction-v1/build_pack.py','bill_construction_builder')

    def packed(self,path):
        path=Path(path).resolve();key=path.relative_to(ROOT).as_posix()
        if key in self.cache:return self.cache[key].copy()
        frame=image(path);folder=path.parent;index=int(re.search(r'(\d+)\.png$',path.name)[1])
        if '/crew-actions-v1/' in key or '/crew-life-v1/' in key:
            out=self.action_frame(path,index,frame)
        elif '/crew-construction-v1/' in key:
            out=self.construction_frame(path,index)
        elif '/deposit-' in key or '/bill-deposit-' in key or folder.name=='bill-remove-helmet-east':
            records=read(folder/'sources.json');record=records[index]
            out=self.packed(WATER/record['source'])
        elif folder.name.startswith('bill-pickup-helmet-'):
            reg=read(folder/'registration.json')
            if index>=len(reg['frames']):out=self.packed(WATER/reg['endpointSource'])
            else:
                pose=reg['frames'][index];out=self.crop_frame(WATER/reg['source'],pose['crop'],reg['scale'],pose['paste'],frame.size)
        elif folder.name=='bill-equip-helmet-east':
            contract=read(folder/'contract.json');reg=read(folder/'clearance.json');pose=reg['frames'][index]
            source=WATER/contract['source'];raw=chroma(source);box=pose['sourceBounds'];crop=raw.crop(box)
            scale=reg['scale'];oldsize=[round(crop.width*scale),round(crop.height*scale)]
            boot=[187,528,853,1205,1534,1870][index]/2048*raw.width
            pos=[46-round((boot-box[0])*scale),98-oldsize[1]]
            out=self.crop_frame(source,box,scale,pos,frame.size)
        elif (folder/'source-contract.json').exists():
            reg=read(folder/'source-contract.json');pose=reg['registration'][index]
            out=self.crop_frame(WATER/reg['source'],pose['crop'],reg['scale'],pose['paste'],frame.size)
        elif (folder/'contract.json').exists() and isinstance(read(folder/'contract.json').get('frames'),list):
            reg=read(folder/'contract.json');pose=reg['frames'][index]
            out=self.crop_frame(WATER/reg['source'].replace('\\','/'),pose['sourceCrop'],reg['scale'],pose['placement'],frame.size)
        elif folder.name=='bill-death-ground-east':
            data=read(folder/'manifest.json');source=WATER/'generated'/f'{folder.name}.png';raw=chroma(source)
            boxes=self.column_boxes(raw);ground=max(b[3] for b in boxes);scale=data['scale'];box=boxes[index]
            oldwidth=round((box[2]-box[0])*scale);pos=[(92-oldwidth)//2,86-round((ground-box[1])*scale)]
            out=self.crop_frame(source,box,scale,pos,frame.size)
        elif folder.parent.name=='pilot':
            data=read(folder/'contract.json');source=WATER/data['source'].replace('\\','/');raw=chroma(source);boxes=self.column_boxes(raw)
            reg=read(WATER/'registration.json')[folder.name];box=boxes[index];scale=data['scale'];sx,sy=reg['shoulders'][index];px,py=reg['anchor']
            pos=[round(px-(sx-box[0])*scale),round(py-(sy-box[1])*scale)]
            out=self.crop_frame(source,box,scale,pos,frame.size)
        else:raise ValueError('No source rebake method: '+key)
        self.cache[key]=out
        return out.copy()

    @staticmethod
    def column_boxes(raw):
        a=np.array(raw);occupied=(a[:,:,3]>0).sum(axis=0)>3
        edges=np.diff(np.r_[False,occupied,False].astype(int));groups=[(a,b) for a,b in zip(np.where(edges==1)[0],np.where(edges==-1)[0]) if b-a>25]
        assert len(groups)==6
        boxes=[]
        for left,right in groups:
            b=raw.crop((int(left),0,int(right),raw.height)).getbbox();boxes.append([int(left)+b[0],b[1],int(left)+b[2],b[3]])
        return boxes

    def crop_frame(self,source,box,scale,pos,size):
        crop=chroma(source).crop(box)
        out=Image.new('RGBA',(size[0]*2,size[1]*2))
        high=binary(crop.resize((max(1,round(crop.width*scale*2)),max(1,round(crop.height*scale*2))),Image.Resampling.BOX),True)
        out.alpha_composite(high,(round(pos[0]*2),round(pos[1]*2)))
        OPS[str(source.relative_to(ROOT))]={'filter':'BOX','density':2}
        return out

    def action_frame(self,path,index,old):
        family_root=path.parents[2];reg=read(path.parent/'registration.json');source=family_root/reg['source'].replace('\\','/')
        source_key=source.as_posix()
        if source_key not in self.rows:
            image(source)
            if 'crew-life-v1' in source_key:
                rows=self.life.source_rows(source)
            else:
                im=self.actions.clean(source);a=np.array(im);groups=self.life.groups(np.flatnonzero((a[:,:,3]>128).sum(axis=1)>12),8);groups=[g for g in groups if len(g)>25]
                rows=[]
                for group in groups:
                    cols=self.life.groups(np.flatnonzero((a[group[0]:group[-1]+1,:,3]>128).sum(axis=0)>0),2)
                    row=[]
                    for c in cols:
                        crop=im.crop((c[0],group[0],c[-1]+1,group[-1]+1));row.append(crop.crop(crop.getbbox()))
                    rows.append(row)
            self.rows[source_key]=[crop for row in rows for crop in row]
        pose=reg['frames'][index];scale=reg['scale'];offset=pose['offset'];target=sig(old);found=None
        for crop in self.rows[source_key]:
            size=(max(1,round(crop.width*scale)),max(1,round(crop.height*scale)))
            test=Image.new('RGBA',old.size);test.alpha_composite(crop.resize(size,Image.Resampling.NEAREST),tuple(offset))
            if sig(test)==target:found=crop;break
        if found is None:raise ValueError('Source crop did not reproduce '+str(path.relative_to(ROOT)))
        self.match_count+=1
        high=binary(found.resize((max(1,round(found.width*scale*2)),max(1,round(found.height*scale*2))),Image.Resampling.NEAREST),True)
        out=Image.new('RGBA',(old.width*2,old.height*2));out.alpha_composite(high,(int(offset[0]*2),int(offset[1]*2)))
        OPS[path.relative_to(ROOT).as_posix()]={'source':source.relative_to(ROOT).as_posix(),'oldFrameReproduced':True,'scale':scale*2,'paste':[int(offset[0]*2),int(offset[1]*2)],'filter':'NEAREST'}
        return out

    def construction_frame(self,path,index):
        direction=path.stem.split('-')[1];row=['east','south','west','north'].index(direction)
        source=path.parents[1]/'source'/('bill-direction-v2.png' if row in [1,3] else 'bill.png')
        image(source);raw,rows=self.construction.clean(source);top,bottom=rows[row]
        crops=[raw.crop((i*raw.width//6,top,(i+1)*raw.width//6,bottom)) for i in range(6)]
        heights=[]
        for crop in crops:
            a=np.array(crop);body=np.argwhere((a[:,:,3]>0)&(a[:,:,:3].max(axis=2)<185));heights.append(crop.height-int(body[:,0].min()))
        scale=74/float(np.median(heights));crop=crops[index];a=np.array(crop);feet=np.argwhere(a[int(crop.height*.88):,:,3]>0)
        anchor=((float(feet[:,1].min())+float(feet[:,1].max())+1)/2,crop.height)
        resized=binary(crop.resize((round(crop.width*scale*2),round(crop.height*scale*2)),Image.Resampling.NEAREST),True)
        out=Image.new('RGBA',(184,184));out.alpha_composite(resized,(round(92-anchor[0]*scale*2),round(172-anchor[1]*scale*2)))
        return out

def rotate(v,angle):
    c,s=np.cos(angle),np.sin(angle)
    return np.array([v[0]*c-v[1]*s,v[0]*s+v[1]*c])

def tilted(body,overlay,offset,angle,rect,direction):
    # Same pixel-centre and occlusion contract as SwimHelmetFit, at source density.
    a=np.array(body);o=np.array(overlay);h,w=a.shape[:2];oh,ow=o.shape[:2]
    yy,xx=np.mgrid[:h,:w];pivot=np.array([ow*.5,oh*.85]);center=np.array(offset)+pivot
    dx,dy=xx+.5-center[0],yy+.5-center[1];c,s=np.cos(angle),np.sin(angle)
    sx=dx*c+dy*s+pivot[0];sy=-dx*s+dy*c+pivot[1];ix=np.floor(sx).astype(int);iy=np.floor(sy).astype(int)
    inside=(ix>=0)&(iy>=0)&(ix<ow)&(iy<oh)
    visor=inside&(sy>=oh*8/28)&(sy<oh*19/28)&((sx>ow*.58) if direction=='east' else (sx<ow*.42))
    scalp=(sy<oh*.32)|(~inside&(sy<oh*.65));x,y,rw,rh=rect
    a[(xx>=x)&(xx<x+rw)&(yy>=y)&(yy<y+rh)&scalp&~visor]=0
    pixels=o[np.clip(iy,0,oh-1),np.clip(ix,0,ow-1)];mask=inside&(pixels[:,:,3]>0);a[mask]=pixels[mask]
    return Image.fromarray(a)

class HelmetRebaker:
    def __init__(self,body):self.body=body;self.cache={};self.overlays={}

    def overlay(self,view,size=None):
        if view not in self.overlays:
            folder=WATER/'equipment'/view
            if (folder/'source-cutout.png').exists():src=image(folder/'source-cutout.png')
            else:
                reg=read(folder/'source-contract.json');src=chroma(WATER/reg['source']).crop(reg['crop'])
            self.overlays[view]=src
        if size is None:size=tuple(v*2 for v in image(WATER/'equipment'/view/'overlay.png').size)
        return binary(self.overlays[view].resize(size,Image.Resampling.BOX),True)

    def packed(self,path):
        path=Path(path).resolve();key=path.relative_to(ROOT).as_posix()
        if key in self.cache:return self.cache[key].copy()
        body=self.body.packed(path);out=body.copy();index=int(re.search(r'(\d+)\.png$',path.name)[1]);folder=path.parent
        if '/major-bill-v2/' in key:
            state=folder.name;reg=read(WATER/'equipment/dry'/('bill-'+state)/'registration.json')
            view=Path(reg['overlay']).parent.name;pos=np.array(reg['frames'][index]['overlayTopLeft'])*2
            if state.startswith('idle-'):
                pos=np.array(reg['frames'][0]['overlayTopLeft'])*2
                if index in [2,3]:pos[1]-=1
            if state in ['walk-east','walk-west']:
                pos=np.array(reg['frames'][0]['overlayTopLeft'])*2
                if index in [1,4]:pos[1]-=1
            out.alpha_composite(self.overlay(view),tuple(pos))
        elif '/crew-actions-v1/' in key or '/crew-life-v1/' in key:
            reg=read(folder/'registration.json');pose=reg['frames'][index];manifest=read(folder/'manifest.json')
            water=bool(manifest['states'][0].get('water',False));facing=pose['facing'];view=('swim-south' if water else 'front') if facing=='south' else facing
            head=np.array(pose['head'])*2;angle=np.deg2rad(pose.get('helmetAngle',(16 if facing=='east' else -16) if water and facing in ['east','west'] else 0))
            out=tilted(body,self.overlay(view,(34,40)),head-[16,18],angle,[*(head-[14,20]),28,34],facing)
        elif folder.name.startswith('bill-swim-') and '/revisions/' in key:
            reg=read(folder/'helmet/registration.json');pose=reg['frames'][index];direction=folder.name.split('-')[2];view=Path(reg['overlay']).parent.name
            oldsize=np.array(image(WATER/reg['overlay']).size);scale=.75 if direction in ['east','west'] else .85
            size=np.floor(oldsize*np.array([.82 if direction in ['east','west'] else scale,scale])+.5).astype(int)
            overlay=self.overlay(view,tuple(size*2));offset=np.array(pose['overlayTopLeft'])*2+np.trunc((oldsize-size)/2).astype(int)*2
            if direction in ['east','west']:
                fit=read(WATER/'swim-head-fit.json')['clips']['bill-swim-'+direction][index];angle=np.deg2rad(fit['tiltDegrees']);w,h=overlay.size;pivot=np.array([w*.5,h*.85])
                edge=np.array([w*(21.5/23 if direction=='east' else 1.5/24),h*13/28]);offset=np.array(fit['faceEdge'])*2-(rotate(edge-pivot,angle)+pivot)
                out=tilted(body,overlay,offset,angle,np.array(fit['headRect'])*2,direction)
            else:out.alpha_composite(overlay,tuple(offset))
            for rect in pose.get('foregroundRects',[]):
                rect=tuple(v*2 for v in rect);out.alpha_composite(body.crop(rect),rect[:2])
        elif '/pilot/' in key:
            clip=folder.name.removeprefix('bill-');reg=read(WATER/'equipment/fitting'/(clip+'-registration.json'));pose=reg['characters']['bill'];direction=clip.split('-')[-1]
            view=reg.get('overlayView','front' if direction=='south' else direction);overlay=self.overlay(view)
            angle=pose.get('overlayRotationDegrees',reg.get('overlayRotationDegrees',0))
            if isinstance(angle,list):angle=angle[index]
            if angle:overlay=overlay.rotate(angle,Image.Resampling.NEAREST,expand=True)
            pos=pose['overlayTopLeft'];pos=pos[index] if isinstance(pos[0],list) else pos
            if clip.startswith('tread-'):
                # Dense tread bodies retain the authored head anchor. Fit the visor
                # to that head, not the oversized legacy pilot equipment bounds.
                size,anchor={'east':((34,36),(76,28)),
                             'west':((34,36),(70,29)),
                             'north':((34,36),(74,32)),
                             'south':((36,40),(74,32))}[direction]
                overlay=self.overlay(view,size)
                pos=tuple(v/2 for v in anchor)
            out.alpha_composite(overlay,tuple(int(v*2) for v in pos))
            for rect in pose.get('foregroundRects',[[]]*6)[index]:
                rect=tuple(v*2 for v in rect);out.alpha_composite(body.crop(rect),rect[:2])
        else:raise ValueError('No helmet source recipe: '+key)
        self.cache[key]=out;return out.copy()

def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    OUT.mkdir(exist_ok=True);QA.mkdir(parents=True,exist_ok=True)
    contract=read(CONTRACT)
    for path,digest in contract['sourceManifests'].items():
        if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=digest:raise ValueError('Original manifest changed: '+path)
    for path,entry in contract['sourceFrames'].items():
        if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=entry['sha256']:raise ValueError('Original frame changed: '+path)
    rebaker=SourceRebaker();body={};entry_map={}
    for e in contract['states']:
        poses=[]
        for f in e['frames']:
            high=rebaker.packed(ROOT/f['sourceFrame']);offset=f['sourceOffset'];size=f['size']
            canvas=Image.new('RGBA',(size[0]*2,size[1]*2));canvas.alpha_composite(high,(offset[0]*2,offset[1]*2));poses.append(canvas)
        body[e['id']]=poses;entry_map[e['id']]=e
    equipment={}
    if contract['equipmentStates']:
        helmets=HelmetRebaker(rebaker)
        for key in contract['equipmentStates']:
            poses=[]
            for f in entry_map[key]['frames']:
                high=helmets.packed(ROOT/f['sourceFrame']);offset=f['sourceOffset'];size=f['size']
                canvas=Image.new('RGBA',(size[0]*2,size[1]*2));canvas.alpha_composite(high,(offset[0]*2,offset[1]*2));poses.append(canvas)
            equipment[key]=poses
    write_outputs(body,equipment,entry_map,contract,rebaker)

def write_outputs(body,equipment,entry_map,contract,rebaker):
    profiles={};frame_records={}
    strides={**contract['strides'],'walk-east':92*65.28/148/384,'walk-west':92*65.28/148/384}
    extents={'bare':{},'helmet':{}}
    for variant,collection in [('bare',body),('helmet',equipment)]:
        for key,poses in collection.items():
            old=entry_map[key];meta=old['frames'][0]['meta'];pivot=[round(v*2) for v in meta['crew_pivot']]
            boxes=np.array([im.getbbox() for im in poses]);bounds=[boxes[:,0].min(),boxes[:,1].min(),boxes[:,2].max(),boxes[:,3].max()]
            extents[variant][key]=[(float(v)-pivot[i%2])*65.28/148 for i,v in enumerate(bounds)]
            profile=f'{variant}-{poses[0].width}x{poses[0].height}-p{pivot[0]}-{pivot[1]}'
            pack=profiles.setdefault(profile,{'name':'major-bill-v3-'+profile,'frameWidth':poses[0].width,'frameHeight':poses[0].height,'pivot':pivot,'standingHeight':148,'strideDistanceCells':strides,'precomposed':True,'states':[]})
            files=[]
            for i,im in enumerate(poses):
                p=OUT/'frames'/variant/key/f'{i:03}.png';p.parent.mkdir(parents=True,exist_ok=True);im.save(p)
                files.append('../../'+p.relative_to(OUT).as_posix())
                frame_records[p.relative_to(OUT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
            entry={'id':key,'frameFiles':files,'frameDurationsMs':old['timing']['durations'],'loop':old['timing']['loop'],
                   'facings':[f['meta'].get('crew_water_facing',key.split('-')[-1]) for f in old['frames']],
                   'waterKinds':[f['meta'].get('crew_water_kind',key.split('-')[0]) for f in old['frames']],
                   'waterPoses':[f['meta'].get('crew_water_pose',False) for f in old['frames']],
                   'depthOffsets':[f['meta'].get('crew_depth_offset',0) for f in old['frames']]}
            pack['states'].append(entry)
            if variant=='bare' and key in ['equip-helmet-east','remove-helmet-east']:
                original=read(WATER/'locker'/('bill-'+key)/'manifest.json')['states'][0]
                entry['events']=original.get('events',[])
                folder=OUT/'locker'/key;folder.mkdir(parents=True,exist_ok=True)
                (folder/'manifest.json').write_text(json.dumps({**pack,'states':[entry]},indent=2)+'\n')
    catalog={'revision':'major-bill-v3','standingHeight':148,'body':[],'equipment':[]}
    for name,data in profiles.items():
        folder=OUT/'packs'/name;folder.mkdir(parents=True,exist_ok=True);(folder/'manifest.json').write_text(json.dumps(data,indent=2)+'\n')
        catalog['body' if name.startswith('bare') else 'equipment'].append((folder/'manifest.json').relative_to(OUT).as_posix())
    (OUT/'catalog.json').write_text(json.dumps(catalog,indent=2)+'\n')
    # Keep prior safe clearance while enclosing every new alpha bound in world units.
    clearance={}
    for kind,source in [('actions',ROOT/'character/crew-actions-v1/clearance.json'),('life',ROOT/'character/crew-life-v1/clearance.json')]:
        clearance[kind]=read(source)['bill']
        for variant,states in clearance[kind].items():
            for key,old in states.items():
                facing=key.split('-')[-1]
                candidates=[key] if key in extents[variant] else [k for k in extents[variant] if (k.startswith(('swim-start-','swim-stop-','swim-turn-')) if key.startswith('transition-') else 'carry-turn-' in k) and facing in k.split('-')]
                if not candidates:raise ValueError('Missing clearance family: '+key)
                for candidate in candidates:
                    new=extents[variant][candidate];old=[min(old[i],new[i]) if i<2 else max(old[i],new[i]) for i in range(4)]
                states[key]=old
    water=read(WATER/'swim-clearance.json')
    for kind,source in [('swim','actors'),('tread','treading')]:
        clearance[kind]=water[source]['bill']
        for variant,states in clearance[kind].items():
            for facing,old in states.items():
                new=extents[variant][kind+'-'+facing];states[facing]=[min(old[i],new[i]) if i<2 else max(old[i],new[i]) for i in range(4)]
    (OUT/'clearance.json').write_text(json.dumps(clearance,indent=2)+'\n')
    for direction in ['east','south','west','north']:
        folder=OUT/'rotations';folder.mkdir(exist_ok=True);body['idle-'+direction][0].save(folder/(direction+'.png'))
    (QA/'build-provenance.json').write_text(json.dumps({'sources':SOURCE_HASHES,'operations':OPS,'frames':frame_records},indent=2)+'\n')
    print(json.dumps({'bodyStates':len(body),'bodyFrames':sum(map(len,body.values())),'equipmentStates':len(equipment),'sourceCropsReproduced':rebaker.match_count,'profiles':len(profiles)}))

if __name__=='__main__':main()
