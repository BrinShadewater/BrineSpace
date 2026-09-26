"""Re-extract Veld/Branforth from preserved sources at Bill's accepted density.

Candidate outputs are isolated from existing runtime bindings. Bill's implementation
supplies deterministic extraction helpers; character-specific recipes live here.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import numpy as np
from PIL import Image, ImageDraw
import rebuild_bill_art as shared
import fitted_crew_helmets
import veld_cargo_revision

ROOT = shared.ROOT
WATER = shared.WATER

def marsh_south_seated_depth(state_id, count):
    """Reviewed furniture sorting for Marsh's south-facing seated sequence."""
    if state_id in ('read-seated-south', 'sit-idle-south'):
        return [40.0] * count
    if state_id in ('sit-down-south', 'sit-rise-south'):
        values=[40.0 * i / max(1,count-1) for i in range(count)]
        return values if state_id=='sit-down-south' else values[::-1]
    return None
PACKS = {'veld':'dr-veld-v1','branforth':'chief-engineer-branforth-v1'}
# Dense source-space fittings reviewed against each actor's authored tread heads.
# The old pilot helmets were much larger than the dry/action equipment.
TREAD_FITS = {
    'veld':{'east':((34,36),(84,29)), 'west':((34,36),(65,29)),
            'north':((34,36),(77,32)), 'south':((36,40),(74,28))},
    'branforth':{'east':((34,36),(86,33)), 'west':((34,36),(65,31)),
                 'north':((34,36),(77,34)), 'south':((40,44),(74,30))}}


def clean_palette(image, palette, threshold=8):
    pixels = np.array(image)
    mask = pixels[:,:,3]>0
    seen = np.zeros(mask.shape,bool)
    for y,x in zip(*np.where(mask)):
        if seen[y,x]: continue
        stack=[(int(y),int(x))]; component=[]; seen[y,x]=True
        while stack:
            cy,cx=stack.pop(); component.append((cy,cx))
            for dy,dx in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
                ny,nx=cy+dy,cx+dx
                if 0<=ny<mask.shape[0] and 0<=nx<mask.shape[1] and mask[ny,nx] and not seen[ny,nx]:
                    seen[ny,nx]=True; stack.append((ny,nx))
        if len(component)<=threshold:
            for cy,cx in component: pixels[cy,cx]=0
    clean=Image.fromarray(pixels)
    out=clean.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA')
    out.putalpha(clean.getchannel('A'))
    return shared.binary(out)


def base_frames(actor,repair_walk=True):
    pack=ROOT/'character'/PACKS[actor]
    builder=shared.module(pack/'build_pack.py',actor+'_base_builder')
    packing=builder.packing
    manifest=shared.read(pack/'final/manifest.json')
    colors=set()
    for state in manifest['states']:
        for rel in state['frameFiles']:
            pixels=np.array(shared.image(pack/'final'/rel))
            colors.update(map(tuple,pixels[pixels[:,:,3]>0,:3].tolist()))
    colors=sorted(colors)
    if len(colors)>256: raise ValueError('Unexpected source palette')
    palette=Image.new('P',(1,1))
    palette.putpalette([v for color in colors for v in color]+list(colors[0])*(256-len(colors)))
    packing.SIZE=184; packing.PIVOT=(92,172)
    rows={}
    for state in builder.STATES:
        if state=='stand-east': continue
        shared.image(pack/'generated'/(state+'.png'))
        rows[state]=packing.extract(state,target=100 if state.startswith('repair') else 148)
    rows['kneel-east'][0]=rows['idle-east'][0].copy()
    rows['kneel-east'][-1]=rows['repair-east'][0].copy()
    rows['repair-east'][-1]=rows['repair-east'][0].copy()
    rows['interact-east'][0]=rows['idle-east'][0].copy()
    rows['interact-east'][-1]=rows['idle-east'][0].copy()
    rows['stand-east']=list(reversed(rows['kneel-east']))
    frames={(pack/'frames'/key/f'frame_{i:03}.png').relative_to(ROOT).as_posix():clean_palette(im,palette)
            for key,poses in rows.items() for i,im in enumerate(poses)}
    if repair_walk:
        from repair_crew_walk import build,RIGS,SELECTED_GAITS
        for owner,clip in sorted(SELECTED_GAITS):
            if owner!=actor:continue
            rig=RIGS[owner,clip]
            donor=f'character/{PACKS[actor]}/frames/{clip}/frame_{rig["sourceFrame"]:03}.png'
            poses,joints=build(frames[donor],rig)
            shared.OPS[f'{actor}/{clip}/local-rig']={'source':donor,'sourcePixelSha256':shared.sig(frames[donor]),'recipe':rig,'joints':joints,'method':'Preserved source parts; alternating stance and swing'}
            for i,pose in enumerate(poses):frames[f'character/{PACKS[actor]}/frames/{clip}/frame_{i:03}.png']=pose
    return frames


class HumanRebaker(shared.SourceRebaker):
    def __init__(self,actor):
        self.actor=actor
        self.cache=base_frames(actor); self.rows={}; self.regs={}; self.match_count=0
        self.life=shared.module(ROOT/'character/crew-life-v1/build_pack.py',actor+'_life')
        self.actions=shared.module(ROOT/'character/crew-actions-v1/build_pack.py',actor+'_actions')
        self.construction=shared.module(ROOT/'character/crew-construction-v1/build_pack.py',actor+'_construction')

    def construction_frame(self,path,index):
        direction=path.stem.split('-')[1]; row=['east','south','west','north'].index(direction)
        source=shared.source_path(ROOT/'character/crew-construction-v1/source'/(self.actor+'.png'))
        shared.image(source); raw,rows=self.construction.clean(source); top,bottom=rows[row]
        crops=[raw.crop((i*raw.width//6,top,(i+1)*raw.width//6,bottom)) for i in range(6)]
        heights=[]
        for crop in crops:
            a=np.array(crop); body=np.argwhere((a[:,:,3]>0)&(a[:,:,:3].max(axis=2)<185))
            heights.append(crop.height-int(body[:,0].min()))
        scale=74/float(np.median(heights)); crop=crops[index]; a=np.array(crop)
        feet=np.argwhere(a[int(crop.height*.88):,:,3]>0)
        anchor=((float(feet[:,1].min())+float(feet[:,1].max())+1)/2,crop.height)
        resized=shared.binary(crop.resize((round(crop.width*scale*2),round(crop.height*scale*2)),Image.Resampling.NEAREST),True)
        out=Image.new('RGBA',(184,184))
        out.alpha_composite(resized,(round(92-anchor[0]*scale*2),round(172-anchor[1]*scale*2)))
        return out

    def packed(self,path):
        path=Path(path).resolve(); key=path.relative_to(ROOT).as_posix()
        if key in self.cache: return self.cache[key].copy()
        import crew_seating_revision
        import crew_sleeping_revision
        sleeping=crew_sleeping_revision.replacement(self.actor,path)
        if sleeping is not None:
            self.cache[key]=sleeping
            return sleeping.copy()
        seating=crew_seating_revision.replacement(self.actor,path)
        if seating is not None:
            self.cache[key]=seating
            return seating.copy()
        cargo=veld_cargo_revision.replacement(self.actor,path)
        if cargo is not None:
            self.cache[key]=cargo
            return cargo.copy()
        if '-helmet-east' in path.parent.name:
            fitted=fitted_crew_helmets.replacement(self.actor,path)
            if fitted is not None:
                self.cache[key]=fitted
                return fitted.copy()
        frame=shared.image(path); folder=path.parent
        index=int(re.search(r'(\d+)\.png$',path.name)[1])
        if '/crew-actions-v1/' in key or '/crew-life-v1/' in key:
            out=self.action_frame(path,index,frame)
        elif '/crew-construction-v1/' in key:
            out=self.construction_frame(path,index)
        elif (folder/'sources.json').exists():
            pose=shared.read(folder/'sources.json')[index]
            if 'sourceBounds' in pose:
                out=self.crop_frame(WATER/pose['source'].replace('\\','/'),pose['sourceBounds'],pose['scale'],pose['placement'],frame.size)
            else: out=self.packed(WATER/pose['source'].replace('\\','/'))
        elif '-pickup-helmet-' in folder.name:
            reg=shared.read(folder/'registration.json')
            if index>=len(reg['frames']): out=self.packed(WATER/reg['endpointSource'])
            else:
                pose=reg['frames'][index]
                out=self.crop_frame(WATER/reg['source'],pose['crop'],reg['scale'],pose['paste'],frame.size)
        elif (folder/'source-contract.json').exists():
            reg=shared.read(folder/'source-contract.json'); pose=reg['registration'][index]
            out=self.crop_frame(WATER/reg['source'],pose['crop'],reg['scale'],pose['paste'],frame.size)
        elif (folder/'registration.json').exists() and 'scale' in shared.read(folder/'registration.json'):
            reg=shared.read(folder/'registration.json'); pose=reg['frames'][index]
            out=self.crop_frame(WATER/reg['source'],pose['crop'],reg['scale'],pose['paste'],frame.size)
        elif (folder/'contract.json').exists() and isinstance(shared.read(folder/'contract.json').get('frames'),list):
            reg=shared.read(folder/'contract.json'); pose=reg['frames'][index]
            out=self.crop_frame(WATER/reg['source'].replace('\\','/'),pose['sourceCrop'],reg['scale'],pose['placement'],frame.size)
        elif folder.name==self.actor+'-death-ground-east':
            data=shared.read(folder/'manifest.json'); source=WATER/'generated'/(folder.name+'.png')
            raw=shared.chroma(source); boxes=self.column_boxes(raw); ground=max(b[3] for b in boxes)
            scale=data['scale']; box=boxes[index]
            pos=[(92-round((box[2]-box[0])*scale))//2,86-round((ground-box[1])*scale)]
            out=self.crop_frame(source,box,scale,pos,frame.size)
        elif folder.parent.name=='pilot':
            data=shared.read(folder/'contract.json'); source=WATER/data['source'].replace('\\','/')
            raw=shared.chroma(source); boxes=self.column_boxes(raw)
            reg=shared.read(WATER/'registration.json')[folder.name]; box=boxes[index]
            scale=data['scale']; sx,sy=reg['shoulders'][index]; px,py=reg['anchor']
            pos=[round(px-(sx-box[0])*scale),round(py-(sy-box[1])*scale)]
            out=self.crop_frame(source,box,scale,pos,frame.size)
        else:
            raise ValueError('No source recipe: '+key)
        self.cache[key]=out
        return out.copy()


class HumanHelmet(shared.HelmetRebaker):
    def __init__(self,body):
        super().__init__(body)
        self.actor=body.actor

    def packed(self,path):
        path=Path(path).resolve(); key=path.relative_to(ROOT).as_posix()
        if key in self.cache: return self.cache[key].copy()
        import crew_seating_revision
        import crew_sleeping_revision
        if veld_cargo_revision.matches(self.actor,path) or crew_seating_revision.matches(self.actor,path) or crew_sleeping_revision.matches(self.actor,path):
            south=crew_sleeping_revision.south_equipped(self.actor,path)
            if south is not None:
                self.cache[key]=south
                return south.copy()
            side_view='west' if path.parent.name.endswith('-west') else 'east'
            side=crew_sleeping_revision.side_equipped(self.actor,path,self.body.packed(path),self.overlay(side_view,(30,32) if self.actor=='veld' else (34,36)))
            if side is not None:
                self.cache[key]=side
                return side.copy()
            size=(34,36) if self.actor=='veld' else (38,40)
            direction=path.parent.name.rsplit('-',1)[-1]
            if direction=='south':size=(36,40) if self.actor=='veld' else (40,44)
            out=veld_cargo_revision.fitted(self.body.packed(path),self.overlay('front' if direction=='south' else direction,size))
            self.cache[key]=out
            return out.copy()
        if '/crew-actions-v1/' in key or '/crew-life-v1/' in key:
            return super().packed(path)
        body=self.body.packed(path); out=body.copy(); folder=path.parent
        index=int(re.search(r'(\d+)\.png$',path.name)[1])
        if '/'+PACKS[self.actor]+'/' in key:
            reg=shared.read(WATER/'equipment/dry'/(self.actor+'-'+folder.name)/'registration.json')
            view=Path(reg['overlay']).parent.name
            # Register each helmet to this character's dense head, not to the
            # old oversized shell's top-left. Restrict the crown region so a
            # raised sample/scanner cannot pull the helmet toward the hand.
            pixels=np.array(body); ys,xs=np.where(pixels[:,:,3]>0)
            crown=int(ys.min())
            cy,cx=np.where(pixels[crown:crown+12,60:120,3]>0)
            if not len(cx): raise ValueError('No crown anchor: '+key)
            center=(float(cx.min()+cx.max()+1)/2)+60
            size=(36,40) if view=='front' else (34,36)
            if self.actor=='branforth': size=(40,44) if view=='front' else (38,40)
            pos=(round(center-size[0]/2),crown-4)
            out.alpha_composite(self.overlay(view,size),pos)
            shared.OPS[key]={'helmetSourceView':view,'helmetSize':size,'helmetTopLeft':pos,'method':'Per-frame crown anchor on preserved dense body; fitted precomposition'}
        elif '-swim-' in folder.name:
            direction=folder.name.split('-')[2]
            if (folder/'helmet/registration.json').exists():
                reg=shared.read(folder/'helmet/registration.json'); pose=reg['frames'][index]
            else:
                original=shared.read(WATER/'equipment/fitting'/('swim-'+direction+'-registration.json'))
                legacy=original['characters'][self.actor]
                reg={'overlay':'equipment/'+original['overlayView']+'/overlay.png'}
                pos=legacy['overlayTopLeft']
                pose={'overlayTopLeft':pos[index] if isinstance(pos[0],list) else pos,'foregroundRects':legacy.get('foregroundRects',[[]]*6)[index]}
            view=Path(reg['overlay']).parent.name
            oldsize=np.array(shared.image(WATER/reg['overlay']).size)
            scale=.75 if direction in ['east','west'] else .85
            size=np.floor(oldsize*np.array([.82 if direction in ['east','west'] else scale,scale])+.5).astype(int)
            overlay=self.overlay(view,tuple(size*2))
            offset=np.array(pose['overlayTopLeft'])*2+np.trunc((oldsize-size)/2).astype(int)*2
            if direction in ['east','west']:
                fit=shared.read(WATER/'swim-head-fit.json')['clips'][self.actor+'-swim-'+direction][index]
                angle=np.deg2rad(fit['tiltDegrees']); w,h=overlay.size; pivot=np.array([w*.5,h*.85])
                edge=np.array([w*(21.5/23 if direction=='east' else 1.5/24),h*13/28])
                offset=np.array(fit['faceEdge'])*2-(shared.rotate(edge-pivot,angle)+pivot)
                out=shared.tilted(body,overlay,offset,angle,np.array(fit['headRect'])*2,direction)
            else: out.alpha_composite(overlay,tuple(offset))
            for rect in pose.get('foregroundRects',[]):
                rect=tuple(v*2 for v in rect); out.alpha_composite(body.crop(rect),rect[:2])
        elif folder.name==self.actor+'-tread-south-v2':
            reg=shared.read(folder/'registration.json'); pose=reg['frames'][index]
            size,pos=TREAD_FITS[self.actor]['south']
            out.alpha_composite(self.overlay(Path(reg['overlay']).parent.name,size),pos)
        elif folder.parent.name=='pilot':
            clip=folder.name.removeprefix(self.actor+'-')
            reg=shared.read(WATER/'equipment/fitting'/(clip+'-registration.json'))
            pose=reg['characters'][self.actor]; direction=clip.split('-')[-1]
            view=reg.get('overlayView','front' if direction=='south' else direction)
            overlay=self.overlay(view)
            angle=pose.get('overlayRotationDegrees',reg.get('overlayRotationDegrees',0))
            if isinstance(angle,list): angle=angle[index]
            if angle: overlay=overlay.rotate(angle,Image.Resampling.NEAREST,expand=True)
            pos=pose['overlayTopLeft']; pos=pos[index] if isinstance(pos[0],list) else pos
            if clip.startswith('tread-'):
                size,anchor=TREAD_FITS[self.actor][direction]
                overlay=self.overlay(view,size); pos=tuple(v/2 for v in anchor)
            out.alpha_composite(overlay,tuple(int(v*2) for v in pos))
            for rect in pose.get('foregroundRects',[[]]*6)[index]:
                rect=tuple(v*2 for v in rect); out.alpha_composite(body.crop(rect),rect[:2])
        else: raise ValueError('No helmet recipe: '+key)
        self.cache[key]=out
        return out.copy()


def write_candidate(out,qa,contract,rebaker,equipped):
    from repair_crew_walk import RIGS,SELECTED_GAITS
    from crew_sleeping_revision import SELECTED as SLEEPING
    helmets=HumanHelmet(rebaker) if equipped else None
    equipment_keys={e['id'] for e in contract['equipment']}
    profiles={}; records={}; coverage=[]; padding={}
    for entry in contract['states']:
        variants={'bare':rebaker}
        if helmets and entry['id'] in equipment_keys: variants['helmet']=helmets
        source_rows={variant:[builder.packed(ROOT/f['sourceFrame']) for f in entry['frames']] for variant,builder in variants.items()}
        if hasattr(rebaker,'state_override'):
            override=rebaker.state_override(entry['id'])
            if override is not None:
                if len(override)!=len(entry['frames']):raise ValueError('State override changes frame count: '+entry['id'])
                source_rows['bare']=override
        from veld_scanner_revision import replacement as scanner_replacement
        scanner=scanner_replacement(rebaker.actor,entry['id'],bool(helmets))
        if scanner is not None:source_rows.update(scanner)
        from branforth_repair_revision import replacement as repair_replacement
        repair = repair_replacement(rebaker.actor, entry['id'], bool(helmets))
        if repair is not None: source_rows.update(repair)
        from marsh_repair_revision import replacement as marsh_repair_replacement
        marsh_repair = marsh_repair_replacement(rebaker.actor, entry['id'], bool(helmets))
        if marsh_repair is not None: source_rows.update(marsh_repair)
        # Explicit pose sequences already own their identity-matched endpoints.
        if scanner is None and rebaker.actor in PACKS and entry['id'] in ['equip-helmet-east','remove-helmet-east']:
            idle=ROOT/'character'/PACKS[rebaker.actor]/'frames/idle-east/frame_000.png'
            bare=rebaker.packed(idle)
            worn=(helmets or HumanHelmet(rebaker)).packed(idle)
            endpoints=[]
            for pose in [bare,worn]:
                padded=Image.new('RGBA',(184,208))
                padded.alpha_composite(pose,(0,24)) # 172 -> 196 foot pivot.
                endpoints.append(padded)
            if entry['id']=='remove-helmet-east': endpoints.reverse()
            source_rows['bare'][0],source_rows['bare'][-1]=endpoints
            shared.OPS[rebaker.actor+'/'+entry['id']+'/endpoints']={
                'method':'Exact selected idle endpoints with pivot translation',
                'idleSource':idle.relative_to(ROOT).as_posix(),'offset':[0,24]}
            if rebaker.actor=='branforth':
                from build_branforth_locker_identity import build as locker_identity
                source_rows['bare']=locker_identity(ROOT,shared.read,shared.image,bare,worn)[entry['id']]
                shared.OPS['branforth/'+entry['id']+'/identity']='Coherent canonical-reference source, recorded empty-helmet cleanup and exact idle endpoints'
        width,height=[v*2 for v in entry['frames'][0]['size']]
        left=top=right=bottom=0
        for poses in source_rows.values():
            for im,frame in zip(poses,entry['frames']):
                x,y=[v*2 for v in frame['sourceOffset']]; box=im.getbbox()
                left=max(left,2-box[0]-x); top=max(top,2-box[1]-y)
                right=max(right,box[2]+x+2-width); bottom=max(bottom,box[3]+y+2-height)
        if any([left,top,right,bottom]): padding[entry['id']]=[left,top,right,bottom]
        pivot=[entry['frames'][0]['meta']['crew_pivot'][0]*2+left,entry['frames'][0]['meta']['crew_pivot'][1]*2+top]
        for variant,poses in source_rows.items():
            profile=f'{variant}-{width+left+right}x{height+top+bottom}-p{pivot[0]}-{pivot[1]}'
            pack=profiles.setdefault(profile,{'name':out.name+'-'+profile,'frameWidth':width+left+right,'frameHeight':height+top+bottom,'pivot':pivot,'standingHeight':148,'strideDistanceCells':contract['strides'],'precomposed':True,'states':[]})
            for owner,clip in sorted(SELECTED_GAITS):
                if owner==rebaker.actor:
                    pack['strideDistanceCells']={**pack['strideDistanceCells'],clip:RIGS[owner,clip]['travel']*2*65.28/148/384}
            for (owner,direction),travel in veld_cargo_revision.SELECTED.items():
                if owner==rebaker.actor:pack['strideDistanceCells']={**pack['strideDistanceCells'],'carry-'+direction:travel*65.28/148/384}
            if rebaker.actor=='veld':
                pack['strideDistanceCells']={**pack['strideDistanceCells'],'walk-east':102*65.28/148/384,'walk-west':108*65.28/148/384,'walk-south':0.12,'walk-north':0.12}
            if rebaker.actor=='branforth':
                pack['strideDistanceCells']={**pack['strideDistanceCells'],'walk-east':106*65.28/148/384,'walk-west':108*65.28/148/384,'walk-north':0.128,'walk-south':0.128}
            if rebaker.actor=='marsh':
                pack['strideDistanceCells']={**pack['strideDistanceCells'],'walk-east':96*65.28/148/384,'walk-west':126*65.28/148/384,'walk-north':0.128,'walk-south':0.128}
                from repair_marsh_carry import SELECTED as MARSH_CARRY
                for direction in sorted(MARSH_CARRY):
                    pack['strideDistanceCells']={**pack['strideDistanceCells'],'carry-'+direction:RIGS['marsh','walk-'+direction]['travel']*2*65.28/148/384}
            files=[]
            for i,(im,frame) in enumerate(zip(poses,entry['frames'])):
                canvas=Image.new('RGBA',(pack['frameWidth'],pack['frameHeight']))
                canvas.alpha_composite(im,(frame['sourceOffset'][0]*2+left,frame['sourceOffset'][1]*2+top))
                file=out/'frames'/variant/entry['id']/f'{i:03}.png'; shared.save_png_if_changed(canvas,file)
                files.append('../../'+file.relative_to(out).as_posix())
                records[file.relative_to(out).as_posix()]=hashlib.sha256(file.read_bytes()).hexdigest()
            state={'id':entry['id'],'frameFiles':files,'frameDurationsMs':entry['timing']['durations'],'loop':entry['timing']['loop']}
            if rebaker.actor=='branforth' and entry['id'] in ['walk-east','walk-west','walk-north','walk-south']:
                direction=entry['id'].split('-')[-1]
                motion_recipe=shared.read(ROOT/f'character/branforth-motion-polish-v1/{direction}-cycle-recipe.json')
                durations=motion_recipe['durations']
                if len(durations)!=len(files) or any(duration<=0 for duration in durations):raise ValueError('Invalid selected motion timing')
                # Preserve the frozen export's numeric representation as well as
                # values, so unchanged recipes do not churn evidence hashes.
                state['frameDurationsMs']=[float(duration) for duration in durations]
            from crew_sleeping_revision import SIDE_FITS
            rest_key=(rebaker.actor,entry['id'].removeprefix('sleep-'))
            if entry['id'].startswith('sleep-') and rest_key in SIDE_FITS:
                head_x,head_y,_=SIDE_FITS[rest_key][-1]
                offset=entry['frames'][0]['sourceOffset'];head_pivot=entry['frames'][0]['meta']['crew_pivot']
                state['restHeadOffset']=[(head_x+offset[0]*2-head_pivot[0]*2)*65.28/148,(head_y+offset[1]*2-head_pivot[1]*2)*65.28/148]
            if entry['id'] in ['sleep-north','sleep-south'] and (rebaker.actor,entry['id'].split('-')[-1]) in SLEEPING:
                # Prone head center from bare art, shared by both equipment variants.
                bare=source_rows['bare'][0];box=bare.getbbox()
                head=np.array(bare)[box[1]:box[1]+16,:,3]>0
                yy,xx=np.where(head)
                offset=entry['frames'][0]['sourceOffset']
                state['restHeadOffset']=[((float(xx.min()+xx.max()+1)/2)+offset[0]*2-entry['frames'][0]['meta']['crew_pivot'][0]*2)*65.28/148,
                    (box[1]+8+offset[1]*2-entry['frames'][0]['meta']['crew_pivot'][1]*2)*65.28/148]
            for dest,src in [('facings','crew_water_facing'),('waterKinds','crew_water_kind'),('waterPoses','crew_water_pose'),('depthOffsets','crew_depth_offset')]:
                state[dest]=[f['meta'][src] for f in entry['frames']]
            if rebaker.actor=='marsh':
                seated_depth=marsh_south_seated_depth(state['id'],len(files))
                if seated_depth is not None: state['depthOffsets']=seated_depth
            pack['states'].append(state)
        coverage.append({'id':entry['id'],'frames':len(entry['frames'])})
    catalog={'revision':out.name,'standingHeight':148,'body':[],'equipment':[],'status':'complete_source_revision'}
    for profile,pack in profiles.items():
        path=out/'packs'/profile/'manifest.json'; path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(pack,indent=2)+'\n')
        catalog['body' if profile.startswith('bare') else 'equipment'].append(path.relative_to(out).as_posix())
    (out/'catalog.json').write_text(json.dumps(catalog,indent=2)+'\n')
    return coverage,records,padding


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('actor',choices=PACKS)
    parser.add_argument('--base-only',action='store_true')
    parser.add_argument('--equipment',action='store_true')
    args=parser.parse_args()
    out=ROOT/'character'/(PACKS[args.actor].removesuffix('-v1')+'-v2')
    qa=ROOT/'output/crew-replacement-2026-09-12'/args.actor
    qa.mkdir(parents=True,exist_ok=True)
    contract=shared.read(ROOT/'tools/crew-art-source-contracts'/(args.actor+'.json'))
    for path,record in contract['sourceFrames'].items():
        if hashlib.sha256(shared.source_path(ROOT/path).read_bytes()).hexdigest()!=record['sha256']:
            raise ValueError('Original source changed: '+path)
    rebaker=HumanRebaker(args.actor)
    if args.base_only:
        contract['states']=[entry for entry in contract['states'] if all('/'+PACKS[args.actor]+'/' in f['sourceFrame'] for f in entry['frames'])]
    states,records,padding=write_candidate(out,qa,contract,rebaker,args.equipment)
    if not args.base_only and args.equipment and args.actor=="veld":
        from build_veld_bunk import build
        build()
    if not args.base_only and args.equipment and args.actor=="branforth":
        from build_branforth_bunk import build
        build()
    if not args.base_only and args.equipment:
        from finalize_crew_art import finalize
        finalize(args.actor)
    # Every candidate image is a source rebake, never enlarged shipped frame art.
    (qa/'body-build.json').write_text(json.dumps({'actor':args.actor,'states':states,'equipmentBuilt':args.equipment,'sourceCropsReproduced':rebaker.match_count,'sourceHashes':shared.SOURCE_HASHES,'operations':shared.OPS,'frames':records,'padding':padding},indent=2)+'\n')
    sheet=Image.new('RGB',(184*6,206*12),(36,43,46)); draw=ImageDraw.Draw(sheet)
    for y,key in enumerate([key for key in rebaker.cache if '/'+PACKS[args.actor]+'/' in key][::6]):
        state=Path(key).parent.name
        draw.text((5,y*206+3),state,fill='white')
        for i in range(6):
            im=rebaker.cache[(ROOT/'character'/PACKS[args.actor]/'frames'/state/f'frame_{i:03}.png').relative_to(ROOT).as_posix()]
            sheet.paste(im,(i*184,y*206+22),im)
    sheet.save(qa/'base-contact.png')
    print(json.dumps({'actor':args.actor,'bodyStates':len(states),'bodyReferences':sum(e['frames'] for e in states),'sourceCropsReproduced':rebaker.match_count,'candidate':str(out)}))


if __name__=='__main__': main()

