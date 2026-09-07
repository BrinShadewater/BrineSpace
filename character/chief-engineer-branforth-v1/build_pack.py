"""Package reference-generated Branforth rows; reuse Bill's deterministic registration."""
from pathlib import Path
import importlib.util
import json
import hashlib
import sys
import math
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('bill_pack', ROOT.parent / 'major-bill-v2/build_pack.py')
packing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packing)
packing.ROOT = ROOT
SIZE = 92
DIRECTIONS = ['south', 'north', 'east', 'west']
STATES = [f'{state}-{direction}' for state in ['idle', 'walk'] for direction in DIRECTIONS]
STATES += ['interact-east', 'kneel-east', 'repair-east', 'stand-east']

def main():
    partial = '--partial' in sys.argv
    for folder in ['final', 'qa/previews', 'rotations']:
        (ROOT / folder).mkdir(parents=True, exist_ok=True)
    animations = {}
    for state in STATES:
        if state == 'stand-east':
            if 'kneel-east' in animations:
                animations[state] = list(reversed(animations['kneel-east']))
            continue
        if partial and not (ROOT / 'generated' / (state + '.png')).exists(): continue
        animations[state] = packing.extract(state, target=50 if state.startswith('repair') else 74)
    if 'kneel-east' in animations and 'repair-east' in animations:
        animations['kneel-east'][0] = animations['idle-east'][0].copy()
        animations['kneel-east'][-1] = animations['repair-east'][0].copy()
        animations['repair-east'][-1] = animations['repair-east'][0].copy()
        animations['stand-east'] = list(reversed(animations['kneel-east']))
    if 'interact-east' in animations:
        animations['interact-east'][0] = animations['idle-east'][0].copy()
        animations['interact-east'][-1] = animations['idle-east'][0].copy()
    report = packing.finish_palette(animations)
    states = list(animations)
    atlas = Image.new('RGBA', (SIZE * 6, SIZE * len(states)))
    contact = Image.new('RGB', (SIZE * 12, (SIZE * 2 + 22) * len(states)), (43, 48, 52))
    draw = ImageDraw.Draw(contact)
    manifest = dict(name='chief-engineer-branforth-v1', frameWidth=SIZE, frameHeight=SIZE, pivot=[46, 86], standingHeight=74,
                    background='transparent', generator='built-in imagegen', requiredMovementStates=['idle','walk'],
                    requiredDirections=DIRECTIONS, strideDistanceCells={'walk':0.12},
                    actionChain=['idle-east','kneel-east','repair-east','stand-east','idle-east'],
                    actionMeaning={'interact':'diagnostic meter reading','repair':'equipment repair'}, cleanup=report, states=[])
    for row, state in enumerate(states):
        frames = animations[state]
        folder = ROOT / 'frames' / state
        folder.mkdir(parents=True, exist_ok=True)
        strip = Image.new('RGBA', (SIZE * 6, SIZE))
        for i, frame in enumerate(frames):
            frame.save(folder / f'frame_{i:03}.png')
            strip.alpha_composite(frame, (i * SIZE, 0))
            atlas.alpha_composite(frame, (i * SIZE, row * SIZE))
            large = frame.resize((SIZE * 2, SIZE * 2), Image.Resampling.NEAREST)
            contact.paste(large, (i * SIZE * 2, row * (SIZE * 2 + 22) + 22), large)
        draw.text((8, row * (SIZE * 2 + 22) + 5), state, fill='white')
        strip.save(ROOT / 'final' / f'{state}-strip.png')
        timing = packing.durations(state)
        loop = state.split('-')[0] not in ['interact','kneel','stand']
        sources = [state] if state != 'stand-east' else ['kneel-east','idle-east','repair-east']
        if state == 'kneel-east': sources += ['idle-east','repair-east']
        if state == 'interact-east': sources += ['idle-east']
        manifest['states'].append(dict(id=state, frameCount=6, frameDurationsMs=timing, fps=round(6000/sum(timing),5), loop=loop,
            frameFiles=[f'../frames/{state}/frame_{i:03}.png' for i in range(6)],
            sources=[f'../generated/{name}.png' for name in sources],
            sourceSha256={name:hashlib.sha256((ROOT/'generated'/f'{name}.png').read_bytes()).hexdigest() for name in sources},
            mirroredFrom=None, reversedFrom='kneel-east' if state=='stand-east' else None,
            notes='Reference-generated poses; no mirrored directions. Shared palette and ground baseline. Work endpoints shared.'))
        packing.save_gif(frames, ROOT/'qa/previews'/f'{state}.gif', timing)
    for direction in DIRECTIONS:
        if f'idle-{direction}' in animations: animations[f'idle-{direction}'][0].save(ROOT/'rotations'/f'{direction}.png')
    atlas.save(ROOT/'final/spritesheet.png')
    contact.save(ROOT/'qa/contact-sheet.png')
    (ROOT/'final/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (ROOT/'qa/cleanup-metrics.json').write_text(json.dumps(report,indent=2)+'\n')
    resource = [f'[gd_resource type="SpriteFrames" load_steps={len(states)*6+2} format=3]', '',
                '[ext_resource type="Texture2D" path="res://character/chief-engineer-branforth-v1/final/spritesheet.png" id="1"]','']
    for row in range(len(states)):
        for col in range(6):
            resource += [f'[sub_resource type="AtlasTexture" id="a{row}_{col}"]', 'atlas = ExtResource("1")',
                         f'region = Rect2({col*SIZE}, {row*SIZE}, {SIZE}, {SIZE})', '']
    resource += ['[resource]', 'animations = [']
    for row, entry in enumerate(manifest['states']):
        frames = ', '.join('{"duration": %.3f, "texture": SubResource("a%d_%d")}'%(ms/100,row,col) for col,ms in enumerate(entry['frameDurationsMs']))
        resource += ['{"frames": [%s], "loop": %s, "name": &"%s", "speed": 10.0},'%(frames,str(entry['loop']).lower(),entry['id'])]
    resource += [']']
    (ROOT/'final/chief-engineer-branforth.tres').write_text('\n'.join(resource)+'\n')
    if not partial:
        chain = manifest['actionChain']
        packing.save_gif([frame for state in chain for frame in animations[state]], ROOT/'qa/engineering-sequence.gif',
                         [ms for state in chain for ms in packing.durations(state)])
        gallery=[]
        for tick in range(60):
            canvas=Image.new('RGB',(SIZE*2*4,(SIZE*2+22)*math.ceil(len(states)/4)),(43,48,52))
            labels=ImageDraw.Draw(canvas)
            for row,state in enumerate(states):
                durations=packing.durations(state)
                t=(tick*50)%sum(durations)
                index=0
                while t>=durations[index] and index<5:
                    t-=durations[index];index+=1
                x=(row%4)*SIZE*2;y=(row//4)*(SIZE*2+22)
                frame=animations[state][index].resize((SIZE*2,SIZE*2),Image.Resampling.NEAREST)
                canvas.paste(frame,(x,y+22),frame)
                labels.text((x+8,y+5),state,fill='white')
            gallery.append(canvas)
        gallery[0].save(ROOT/'qa/animation-preview.gif',save_all=True,append_images=gallery[1:],duration=50,loop=0,disposal=2)
    print(json.dumps({'states':len(states),'frames':len(states)*6,'partial':partial}))

if __name__ == '__main__': main()

