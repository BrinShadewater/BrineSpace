"""Rebuild Bill's animation assets from repository-local generated source art."""
from pathlib import Path
import json
import math
import hashlib
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
SIZE = 92
PIVOT = (46, 86)
DIRECTIONS = ['south', 'north', 'east', 'west']
STATES = [f'{state}-{direction}' for state in ['idle', 'walk', 'run'] for direction in DIRECTIONS]
STATES += ['interact-east', 'kneel-east', 'repair-east', 'stand-east', 'walk-south-east']
CLEANUP = json.loads((ROOT/'cleanup-sources.json').read_text())['sources']
# Authored phase ordering after reviewing the contact/passing poses.
POSE_ORDER = {'walk-north': [0,2,4,1,3,5], 'run-north': [0,2,5,1,3,4],
              'repair-east': [0,1,2,3,1,0]}

def extract(name, count=6, target=74):
    source = ROOT / 'generated' / f'{name}.png'
    data = np.array(Image.open(source).convert('RGBA'))
    rgb = data[:,:,:3].astype(np.int16)
    key = (rgb[:,:,0] > rgb[:,:,1]+35) & (rgb[:,:,2] > rgb[:,:,1]+35) & (rgb[:,:,0] > 95) & (rgb[:,:,2] > 95)
    data[key | (data[:,:,3] < 128)] = 0
    if name == 'cleanup-walk-south':
        # This source returned an opaque light checker backdrop. Remove only
        # the connected exterior, keeping enclosed metal/skin highlights.
        light = (rgb.min(axis=2)>220) & (rgb.max(axis=2)-rgb.min(axis=2)<18)
        mask = Image.fromarray((light*255).astype(np.uint8)).copy()
        ImageDraw.floodfill(mask,(0,0),128)
        data[np.array(mask)==128] = 0
    occupied = (data[:,:,3] > 0).sum(axis=0) > 3
    edges = np.diff(np.r_[False, occupied, False].astype(int))
    groups = [(int(a),int(b)) for a,b in zip(np.where(edges==1)[0],np.where(edges==-1)[0]) if b-a>25]
    if len(groups) != count:
        raise ValueError(f'{name}: expected {count} separated poses, got {groups}')
    poses = []
    for left,right in groups:
        image = Image.fromarray(data[:,left:right])
        box = image.getbbox()
        poses.append((image.crop(box),box))
    top = min(box[1] for _,box in poses)
    baseline = max(box[3] for _,box in poses)
    scale = target/(baseline-top)
    head_widths=[]
    for image,_ in poses:
        _,xs=np.where(np.array(image.getchannel('A'))[:max(1,round(image.height*.17))]>0)
        head_widths.append(float(xs.max()-xs.min()+1))
    median_head=float(np.median(head_widths))
    frames = []
    for pose_index,(image,box) in enumerate(poses):
        alpha = np.array(image.getchannel('A'))
        _,head_x = np.where(alpha[:max(1,round(image.height*.17))] > 0)
        anchor = (float(head_x.min())+float(head_x.max())+1)/2
        # Small uniform registration correction for generated head-size drift;
        # never independently warp limbs or replace body parts.
        pose_scale=scale*float(np.clip(median_head/head_widths[pose_index],0.97,1.03))
        # Generated sources have dense subpixel texture rather than a true
        # 92px pixel grid. Area downsampling removes that texture before the
        # shared palette is applied; final pixels remain hard-edged.
        resized = image.resize((round(image.width*pose_scale),round(image.height*pose_scale)),Image.Resampling.BOX)
        resized.putalpha(resized.getchannel('A').point(lambda value: 255 if value>=128 else 0))
        x = round(PIVOT[0]-anchor*pose_scale)
        # Shared row baseline preserves airborne feet and crouching height.
        y = PIVOT[1]-round((baseline-box[1])*pose_scale)
        if x<1 or x+resized.width>=SIZE or y<1 or y+resized.height>=SIZE:
            raise ValueError(f'{name}: clipping at {x,y,resized.size}')
        frame = Image.new('RGBA',(SIZE,SIZE))
        frame.alpha_composite(resized,(x,y))
        frames.append(frame)
    return frames

def finish_palette(animations):
    """One non-dithered palette and isolated-alpha cleanup for the entire pack."""
    pixels=[]
    removed=0
    before_colors=set()
    for frames in animations.values():
        for frame in frames:
            arr=np.array(frame)
            mask=arr[:,:,3]>0
            visited=np.zeros(mask.shape,dtype=bool)
            for y,x in zip(*np.where(mask)):
                if visited[y,x]: continue
                stack=[(int(y),int(x))]; component=[]; visited[y,x]=True
                while stack:
                    cy,cx=stack.pop(); component.append((cy,cx))
                    for dy,dx in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
                        ny,nx=cy+dy,cx+dx
                        if 0<=ny<SIZE and 0<=nx<SIZE and mask[ny,nx] and not visited[ny,nx]:
                            visited[ny,nx]=True; stack.append((ny,nx))
                if len(component)<=2:
                    for cy,cx in component: arr[cy,cx]=0
                    removed+=len(component)
            frame.paste(Image.fromarray(arr))
            opaque=arr[arr[:,:,3]>0,:3]
            pixels.extend(opaque.tolist())
            before_colors.update(map(tuple,opaque.tolist()))
    sample=Image.fromarray(np.asarray(pixels,dtype=np.uint8).reshape(1,-1,3))
    palette=sample.quantize(colors=64,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    after_colors=set()
    for state,frames in animations.items():
        for i,frame in enumerate(frames):
            alpha=frame.getchannel('A')
            quantized=frame.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA')
            quantized.putalpha(alpha)
            frames[i]=quantized
            arr=np.array(quantized)
            after_colors.update(map(tuple,arr[arr[:,:,3]>0,:3].tolist()))
    return {'opaqueColorsBefore':len(before_colors),'opaqueColorsAfter':len(after_colors),
            'isolatedAlphaPixelsRemoved':removed,'dither':False,'paletteColors':64}

def durations(state):
    if state.startswith('idle'): return [260,220,240,220,240,260]
    if state.startswith('walk'): return [170,130,150,170,130,150]
    if state.startswith('run'): return [110,85,105,110,85,105]
    if state.startswith('interact'): return [180,120,140,260,140,180]
    if state.startswith('repair'): return [160,140,180,140,160,180]
    return [140,140,160,180,180,200]

def save_gif(frames,path,timing):
    images=[]
    for frame in frames:
        bg=Image.new('RGBA',(SIZE,SIZE),(43,48,52,255))
        bg.alpha_composite(frame)
        images.append(bg.convert('RGB').resize((SIZE*3,SIZE*3),Image.Resampling.NEAREST))
    images[0].save(path,save_all=True,append_images=images[1:],duration=timing,loop=0,disposal=2)

def main():
    for folder in ['final','qa/previews','rotations']:
        (ROOT/folder).mkdir(parents=True,exist_ok=True)
    animations={}
    for state in STATES:
        if state=='stand-east':
            animations[state]=list(reversed(animations['kneel-east']))
        else:
            source='cleanup-'+state if state in CLEANUP else state
            target=50 if state.startswith('repair') else 68 if state in ['run-east','run-west'] else 74
            animations[state]=extract(source,target=target)
            if state in POSE_ORDER:
                animations[state]=[animations[state][i] for i in POSE_ORDER[state]]
    # Shared endpoints make action transitions join without a one-frame pose jump.
    animations['kneel-east'][0]=animations['idle-east'][0].copy()
    animations['kneel-east'][-1]=animations['repair-east'][0].copy()
    animations['stand-east']=list(reversed(animations['kneel-east']))
    animations['interact-east'][0]=animations['idle-east'][0].copy()
    animations['interact-east'][-1]=animations['idle-east'][0].copy()
    # Let the repair action settle back to the same endpoint before standing.
    animations['repair-east'][-1]=animations['repair-east'][0].copy()
    # Quantize before sharing endpoints again: all exported frames use one palette.
    finish_report=finish_palette(animations)
    animations['kneel-east'][0]=animations['idle-east'][0].copy()
    animations['kneel-east'][-1]=animations['repair-east'][0].copy()
    animations['stand-east']=list(reversed(animations['kneel-east']))
    manifest=dict(name='major-bill-v2',frameWidth=SIZE,frameHeight=SIZE,pivot=list(PIVOT),
        standingHeight=74,background='transparent',generator='built-in imagegen',
        requiredMovementStates=['idle','walk','run'],requiredDirections=DIRECTIONS,
        actionChain=['idle-east','kneel-east','repair-east','stand-east','idle-east'],
        states=[])
    manifest['cleanup']=finish_report
    manifest['strideDistanceCells']={'walk':0.12,'run':0.168}
    atlas=Image.new('RGBA',(SIZE*6,SIZE*len(STATES)))
    for row,state in enumerate(STATES):
        frames=animations[state]
        frame_dir=ROOT/'frames'/state
        frame_dir.mkdir(parents=True,exist_ok=True)
        strip=Image.new('RGBA',(SIZE*6,SIZE))
        for index,frame in enumerate(frames):
            frame.save(frame_dir/f'frame_{index:03}.png')
            strip.alpha_composite(frame,(SIZE*index,0))
            atlas.alpha_composite(frame,(SIZE*index,SIZE*row))
        strip.save(ROOT/'final'/f'{state}-strip.png')
        timing=durations(state)
        loop=state.split('-')[0] not in ['interact','kneel','stand']
        source_names=['cleanup-'+state if state in CLEANUP else state]
        notes='Reference-generated; no mirroring; shared ground baseline, head-size registration and 64-color non-dithered palette.'
        if state in POSE_ORDER: notes+=' Authored source pose order: '+str(POSE_ORDER[state])+'.'
        if state=='stand-east':
            source_names=['kneel-east','idle-east','cleanup-repair-east']
            notes+=' Reversed kneel frames, ending with tool stowed.'
        if state=='kneel-east':
            source_names+=['idle-east','cleanup-repair-east']
            notes+=' Endpoints shared with idle and repair.'
        if state=='interact-east': source_names+=['idle-east']
        manifest['states'].append(dict(id=state,frameCount=6,frameDurationsMs=timing,
            fps=round(6000/sum(timing),5),loop=loop,
            frameFiles=[f'../frames/{state}/frame_{i:03}.png' for i in range(6)],
            sources=[f'../generated/{n}.png' for n in source_names],
            sourceSha256={n:hashlib.sha256((ROOT/'generated'/f'{n}.png').read_bytes()).hexdigest() for n in source_names},
            mirroredFrom=None,reversedFrom='kneel-east' if state=='stand-east' else None,notes=notes))
        save_gif(frames,ROOT/'qa/previews'/f'{state}.gif',timing)
    for direction in DIRECTIONS:
        animations[f'idle-{direction}'][0].save(ROOT/'rotations'/f'{direction}.png')
    atlas.save(ROOT/'final/spritesheet.png')
    (ROOT/'final/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (ROOT/'qa/cleanup-metrics.json').write_text(json.dumps(finish_report,indent=2)+'\n')
    resource=[f'[gd_resource type="SpriteFrames" load_steps={len(STATES)*6+2} format=3]',
        '', '[ext_resource type="Texture2D" path="res://character/major-bill-v2/final/spritesheet.png" id="1"]','']
    for row in range(len(STATES)):
        for col in range(6):
            resource += [f'[sub_resource type="AtlasTexture" id="a{row}_{col}"]','atlas = ExtResource("1")',f'region = Rect2({col*SIZE}, {row*SIZE}, {SIZE}, {SIZE})','']
    resource += ['[resource]','animations = [']
    for row,state in enumerate(manifest['states']):
        # At 10 FPS a duration multiplier of milliseconds/100 is exact.
        frames=', '.join('{"duration": %.3f, "texture": SubResource("a%d_%d")}'%(ms/100,row,col) for col,ms in enumerate(state['frameDurationsMs']))
        resource += ['{"frames": [%s], "loop": %s, "name": &"%s", "speed": 10.0},'%(frames,str(state['loop']).lower(),state['id'])]
    resource += [']']
    (ROOT/'final/major-bill.tres').write_text('\n'.join(resource)+'\n')
    chain=['idle-east','kneel-east','repair-east','repair-east','stand-east','idle-east']
    chain_frames=[frame for state in chain for frame in animations[state]]
    chain_timing=[ms for state in chain for ms in durations(state)]
    save_gif(chain_frames,ROOT/'qa/repair-sequence.gif',chain_timing)
    # A real-time gallery: each animation advances on its own durations.
    gallery=[]
    for tick in range(60):
        canvas=Image.new('RGB',(SIZE*3*4,(SIZE*3+25)*math.ceil(len(STATES)/4)),(43,48,52))
        draw=ImageDraw.Draw(canvas)
        for row,state in enumerate(STATES):
            timing=durations(state)
            t=(tick*50)%sum(timing)
            index=0
            while t>=timing[index] and index<5:
                t-=timing[index]; index+=1
            x=(row%4)*SIZE*3; y=(row//4)*(SIZE*3+25)
            frame=animations[state][index].resize((SIZE*3,SIZE*3),Image.Resampling.NEAREST)
            canvas.paste(frame,(x,y+25),frame)
            draw.text((x+12,y+7),state,fill='white')
        gallery.append(canvas)
    gallery[0].save(ROOT/'qa/animation-preview.gif',save_all=True,append_images=gallery[1:],duration=50,loop=0,disposal=2)
    print(json.dumps({'states':len(STATES),'frames':len(STATES)*6,'frameSize':[SIZE,SIZE]}))

if __name__=='__main__': main()
