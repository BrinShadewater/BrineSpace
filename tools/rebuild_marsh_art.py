"""Rebuild every active Marsh body state from original v2/v5 authored sheets.

Preserves old packs; emits a separate dense candidate and verifies legacy source
reproduction before claiming provenance. Android gameplay does not need helmets.
"""
from pathlib import Path
import copy, hashlib, json
import numpy as np
from PIL import Image
import build_sprite_polish as polish
import build_companion_cleanup as clean
import rebuild_bill_art as shared
from rebuild_human_crew_art import write_candidate

ROOT=shared.ROOT
V2=ROOT/'character/sprite-polish-v2'
if not (V2/'sources/marsh-locomotion.png').exists():
    V2=ROOT/'archive/character/sprite-polish-v2'
V5=ROOT/'character/animation-expansion-v5'
QA=ROOT/'output/crew-replacement-2026-09-12/marsh'
OUT=ROOT/'character/marsh-v2'
DIRS=['south','west','north','east']
PROVENANCE={}


def source(path):
    PROVENANCE[path.relative_to(ROOT).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
    return Image.open(path).convert('RGBA')


def frame(tile,scale,density):
    tile=tile.resize((round(tile.width*scale*density),round(tile.height*scale*density)),Image.Resampling.BOX)
    tile.putalpha(tile.getchannel('A').point(lambda a:255 if a>=128 else 0))
    result=Image.new('RGBA',(92*density,92*density))
    result.alpha_composite(tile,((92*density-tile.width)//2,86*density-tile.height))
    return result


def slices(name,cols,density):
    im=source(V2/'sources'/f'marsh-{name}.png'); result={}
    for row,d in enumerate(['south','north','east','west']):
        strip=im.crop((0,round(row*im.height/4),im.width,round((row+1)*im.height/4)))
        ink=np.asarray(strip); rgb=ink[:,:,:3].astype(int)
        mask=(ink[:,:,3]>=128)&~((rgb[:,:,0]>rgb[:,:,1]+55)&(rgb[:,:,2]>rgb[:,:,1]+55))
        edges=[0]
        for col in range(1,cols):
            start=round(col*im.width/cols)-85; counts=mask.sum(axis=0)[start:start+170]
            edges.append(start+int(np.median(np.where(counts==counts.min())[0])))
        edges.append(im.width); tiles=[]
        for col in range(cols):
            tile=strip.crop((edges[col],0,edges[col+1],strip.height)); a=np.array(tile); rgb=a[:,:,:3].astype(int)
            a[(a[:,:,3]<128)|((rgb[:,:,0]>rgb[:,:,1]+55)&(rgb[:,:,2]>rgb[:,:,1]+55))]=0
            tile=Image.fromarray(a); tiles.append((tile,tile.getbbox()))
        baseline=max(b[3] for _,b in tiles); top=min(b[1] for _,b in tiles)
        scale=min(74/(baseline-top),88/max(b[2]-b[0] for _,b in tiles)); poses=[]
        for tile,b in tiles:
            body=tile.crop(b).resize((round((b[2]-b[0])*scale*density),round((b[3]-b[1])*scale*density)),Image.Resampling.BOX)
            body.putalpha(body.getchannel('A').point(lambda a:255 if a>=128 else 0))
            out=Image.new('RGBA',(92*density,92*density))
            out.alpha_composite(body,(46*density-body.width//2,86*density-round((baseline-b[1])*scale*density)))
            poses.append(out)
        result[d]=poses
    return result


def quantize(clips,palette=None):
    if palette is None:
        polish.quantize(clips)
    else:
        for row in clips.values():
            for i,im in enumerate(row):
                out=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA')
                out.putalpha(im.getchannel('A')); row[i]=shared.binary(out)


def base(density,palette):
    manifest=shared.read(ROOT/'character/marsh-v1/final/manifest.json')
    sheets={name:slices(name,cols,density) for name,cols in [('locomotion',8),('work',8),('swim',8),('death',6)]}
    clips={}
    for s in manifest['states']:
        state,d=s['id'].rsplit('-',1)
        if state=='idle': frames=sheets['locomotion'][d][:2]
        elif state in ['walk','run']: frames=sheets['locomotion'][d][2:]
        else:
            frames=[]
            for p in s['frameFiles']:
                family=Path(p).parent.name.rsplit('-',1)[0]; i=int(Path(p).stem.split('_')[-1])
                indices=[1,2,3,4,5,6] if family=='swim' else [0,1,2,3,4,7] if family=='work' else list(range(6))
                frames.append(sheets[family][d][indices[i]].copy())
            if state in ['death-ground','death-water','kneel','sit-down','lie-down']: frames[0]=sheets['locomotion'][d][0].copy()
            if state in ['stand','sit-rise','get-up']: frames[-1]=sheets['locomotion'][d][0].copy()
        clips[s['id']]=[f.copy() for f in frames]
    quantize(clips,palette)
    return clips


def expansion_sheet(name,density,dirs=DIRS):
    path=V5/'sources'/(name+'.png'); source(path)
    rows=clean.rows(path,4,8,gutter_fraction=.4); result={}
    for d,tiles in zip(dirs,rows):
        scale=min(74/tiles[0].height,87/max(t.width for t in tiles),83/max(t.height for t in tiles))
        result[d]=[frame(t,scale,density) for t in tiles]
    return result


def expanded(density,palette):
    clips=base(density,palette)
    sit=expansion_sheet('marsh-sit',density,['south','east','north','west'])
    rest=expansion_sheet('marsh-rest',density,['south','east','north','west'])
    cargo=expansion_sheet('marsh-cargo',density)
    image=source(V5/'sources/marsh-water-spaced.png'); ys=[0,131,248,370,475,621,761,892,1024]; raw=[]
    for r in range(8):
        row=[]
        for col in range(4):
            tile=clean.clean(image.crop((col*384,ys[r],(col+1)*384,ys[r+1])))
            row.append(tile.crop(tile.getbbox()))
        raw.append(row)
    west=[raw[5][0],raw[5][1],raw[7][2],raw[5][1]]
    east=[raw[7][0],raw[7][1],raw[5][2],raw[5][3]]
    raw[5]=west; raw[7]=east
    scale=87/max(t.width for row in raw for t in row)
    for i,d in enumerate(DIRS):
        s,r,g=sit[d],rest[d],cargo[d]
        w=[frame(t,scale,density) for t in raw[i]+raw[i+4]]
        idle=clips['idle-'+d][0]; entry=[idle,s[1],s[2],s[3]]; lie=[idle,r[2],r[3],r[4]]
        for action,frames in [('sit-down',entry),('sit-rise',entry[::-1]),('sit-idle',s[3:5]),('read-seated',s[5:8]),
                ('lie-down',lie),('get-up',[r[5],r[6],r[7],idle]),('sleep',r[4:6]),('pickup',[idle,g[1],g[2],g[3]]),
                ('carry',g[4:8]),('cargo-unload',[g[3],g[2],g[1],idle]),('unload',[g[3],g[2],g[1],idle]),('swim',w[:4]),('tread',w[4:])]:
            clips[action+'-'+d]=[f.copy() for f in frames]
    quantize(clips,palette)
    return clips


class MarshRebaker:
    actor='marsh'
    def __init__(self,clips,welding=None):
        self.clips=clips
        self.welding=welding or {}
    def packed(self,path):
        return self.clips[path.parent.name][int(path.stem)].copy()
    def state_override(self,key):
        if key=='walk-step-north':
            manifest=ROOT/'character/marsh-north-step-v1/sequence-v2/manifest.json'
            state=json.loads(manifest.read_text())['states'][0]
            return [source(manifest.parent/p) for p in state['frameFiles']]
        if key.startswith('walk-stop-p') and key.endswith('-north'):
            manifest=ROOT/'character/marsh-north-stop-v1/phase-bank-v3/manifest.json'
            state=next(s for s in json.loads(manifest.read_text())['states'] if s['id']==key)
            return [source(manifest.parent/p) for p in state['frameFiles']]
        if key=='walk-start-north':
            manifest=ROOT/'character/marsh-north-walk-material-v1/candidate-01/north-start/manifest.json'
            state=json.loads(manifest.read_text())['states'][0]
            return [source(manifest.parent/p) for p in state['frameFiles']]
        north_path=ROOT/'character/marsh-north-walk-material-v1/selection.json'
        if north_path.exists():
            selected=json.loads(north_path.read_text())
            if key in selected['changedStates']:
                return [source(ROOT/p) for p in selected['states'][key]]
        repair_path=ROOT/'character/marsh-master-repair-v1/selection.json'
        if repair_path.exists():
            selected=json.loads(repair_path.read_text())
            if key in selected['changedStates']:
                return [source(ROOT/p) for p in selected['states'][key]]
        fullset_path=ROOT/'character/marsh-quality-pass-v4/selection.json'
        if fullset_path.exists():
            selected=json.loads(fullset_path.read_text())
            if key in selected['changedStates']:
                return [source(ROOT/p) for p in selected['states'][key]]
        if key.split('-')[0] in ('interact','repair','inspect','salvage','kneel','stand'):
            folder=ROOT/'character/marsh-diagnostics-v7/frames'/key
            if folder.exists():return [source(p) for p in sorted(folder.glob('*.png'))]
        if key.startswith('crew-chat-'):
            folder=ROOT/'character/marsh-crew-chat-v2/frames'/key
            return [source(folder/f'{i:03}.png') for i in range(8)]
        if key=='tread-north':
            folder=ROOT/'character/marsh-quality-pass-v2/frames/tread-north'
            if folder.exists():return [source(folder/f'{i:03}.png') for i in range(4)]
        if key.startswith(('injury-ground-','injury-rise-')):
            folder=ROOT/'character/marsh-injury-runtime-v1/frames'/key
            return [source(folder/f'{i:03}.png') for i in range(6)]
        polish_path=ROOT/'character/marsh-full-polish-v1/selection.json'
        if polish_path.exists():
            polish=json.loads(polish_path.read_text())
            if key in polish['changedStates']:
                return [source(ROOT/p) for p in polish['states'][key]]
        from repair_crew_walk import SELECTED_GAITS
        from repair_marsh_carry import SELECTED as CARRY
        action, _, direction=key.rpartition('-')
        if action in ('interact','kneel','repair','stand') and direction in ('south','north','east','west'):
            source_dir=ROOT/'character/marsh-controller-tone-v1/frames'/key
            return [source(source_dir/f'{i:03}.png') for i in range(6 if action in ('interact','repair') else 3)]
        if action in ('eat','drink') and direction in ('south','north','east','west'):
            source_dir=ROOT/'character/marsh-galley-match-v1/frames'/key
            return [source(source_dir/f'{i:03}.png') for i in range(6)]
        if action in ('death-water','swim-distress','recover-air') and direction in ('south','north','east','west'):
            source_dir=ROOT/'character/marsh-water-recovery-match-v1/frames'/key
            return [source(source_dir/f'{i:03}.png') for i in range(6)]
        if action=='death-ground' and direction in ('south','north','east','west'):
            source_dir=ROOT/'character/marsh-shutdown-injury-match-v1/frames'/key
            return [source(source_dir/f'{i:03}.png') for i in range(6)]
        if action in ('swim','tread') and direction in ('south','north','east','west'):
            source_dir=ROOT/'character/marsh-water-match-v1/frames'/key
            return [source(source_dir/f'{i:03}.png') for i in range(4)]
        if action=='carry' and direction in ('south','north','east','west'):
            source_dir=ROOT/'character/marsh-carry-match-v1/frames'/direction
            return [source(source_dir/f'{i:03}.png') for i in range(4)]
        if action in ('pickup','unload','cargo-unload') and direction in ('south','north','east','west'):
            source_dir=ROOT/'character/marsh-carry-chain-v1/frames'/key
            return [source(source_dir/f'{i:03}.png') for i in range(4)]
        if action in ('salvage','inspect') and direction in ('south','north','east','west'):
            source_dir=ROOT/'character/marsh-salvage-match-v1/frames'/('salvage-'+direction)
            return [source(source_dir/f'{i:03}.png') for i in range(6)]
        if key in [f'run-{direction}' for direction in ('south','north','east','west')]:
            direction=key.split('-')[-1]
            source_dir=ROOT/'character/marsh-run-match-v1/frames'/direction
            return [source(source_dir/f'{i:03}.png') for i in range(6)]
        if action in ('lie-down','sleep','get-up') and direction in ('south','north','east','west'):
            source_dir=ROOT/'character/marsh-rest-match-v1/frames'/key
            return [source(source_dir/f'{i:03}.png') for i in range(2 if action=='sleep' else 4)]
        if action in ('sit-down','sit-idle','read-seated','sit-rise') and direction in ('south','north','east','west'):
            source_dir=ROOT/'character/marsh-seated-match-v1/frames'/key
            return [source(source_dir/f'{i:03}.png') for i in range(3 if action=='read-seated' else 2 if action=='sit-idle' else 4)]
        if action in ('torch-draw','weld','torch-stow') and direction in ('south','north','east','west'):
            source_dir=ROOT/'character/marsh-welding-match-v1/frames'/key
            return [source(source_dir/f'{i:03}.png') for i in range(6)]
        if key in self.welding:return [frame.copy() for frame in self.welding[key]]
        if key in ['carry-'+d for d in CARRY]:return [frame.copy() for frame in self.clips[key]]
        if ('marsh',key) in SELECTED_GAITS:return [frame.copy() for frame in self.clips[key]]
        return None


def original_palette(contract=None):
    if contract is None:contract=shared.read(ROOT/'tools/crew-art-source-contracts/marsh.json')
    colors=set()
    for path,record in contract['sourceFrames'].items():
        if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=record['sha256']: raise ValueError('Original changed: '+path)
        a=np.array(shared.image(ROOT/path)); colors.update(map(tuple,a[a[:,:,3]>0,:3].tolist()))
    colors=sorted(colors); assert len(colors)<=256
    palette=Image.new('P',(1,1)); palette.putpalette([v for c in colors for v in c]+list(colors[0])*(256-len(colors)))
    return palette,len(colors)


def source_clips():
    palette,_=original_palette()
    return expanded(2,palette)


def main():
    QA.mkdir(parents=True,exist_ok=True)
    contract=shared.read(ROOT/'tools/crew-art-source-contracts/marsh.json')
    palette,color_count=original_palette(contract)
    legacy=expanded(1,None); unmatched=[]
    for path in contract['sourceFrames']:
        p=ROOT/path
        if shared.sig(legacy[p.parent.name][int(p.stem)])!=shared.sig(shared.image(p)): unmatched.append(path)
    (QA/'source-reproduction.json').write_text(json.dumps({'checked':len(contract['sourceFrames']),'unmatched':unmatched},indent=2)+'\n')
    if unmatched: raise ValueError(f'{len(unmatched)} Marsh source frames failed legacy reproduction; inspect source-reproduction.json')
    clips=expanded(2,palette)
    from repair_crew_walk import RIGS,SELECTED_GAITS,build
    donors={key:clips[rig.get('sourceClip',key)][rig['sourceFrame']].copy()
            for (owner,key),rig in RIGS.items() if owner=='marsh' and (owner,key) in SELECTED_GAITS}
    for key,donor in donors.items():
        rig=RIGS['marsh',key]
        clips[key],joints=build(donor,rig)
        shared.OPS['marsh/'+key+'/local-rig']={'sourceClip':rig.get('sourceClip',key),'sourcePixelSha256':shared.sig(donor),'recipe':rig,'joints':joints,'method':'Independent source parts with explicit runtime state override'}
    from repair_marsh_carry import SELECTED as CARRY,main as carry_build
    for direction in sorted(CARRY):clips['carry-'+direction]=carry_build(direction)
    from marsh_welding_revision import SELECTED as WELDING,REVISIONS,build_selected as welding_build
    welding={}
    if WELDING:
        revised=welding_build()
        for group,revision in REVISIONS.items():
            source(ROOT/f'character/crew-action-detail-v2/sources/marsh-welding-{group}-candidate-{revision}.png')
        from marsh_low_welding import SELECTED as LOW_SELECTED
        if LOW_SELECTED:source(ROOT/'character/crew-action-detail-v2/sources/marsh-welding-low-south-candidate-01.png')
        from marsh_low_welding import REACH_SELECTED
        if LOW_SELECTED and REACH_SELECTED:
            for name in ['pose-candidate-04','transition-candidate-01','intermediate-candidate-01','loop-candidate-01']:
                source(ROOT/f'character/crew-action-detail-v2/sources/marsh-low-reach-{name}.png')
        # Frozen repair/eat/etc aliases also reference old weld paths. Keep that
        # source dictionary intact and override only the requested runtime states.
        welding={key:revised[key] for key in WELDING}
    states,records,padding=write_candidate(OUT,QA,contract,MarshRebaker(clips,welding),False)
    from build_marsh_ground_transitions import build as build_ground_transitions
    build_ground_transitions()
    from build_marsh_berth import build as build_berth
    build_berth()
    from build_marsh_bunk import build as build_bunk
    build_bunk()
    from finalize_crew_art import finalize
    from build_marsh_swim_transitions import build as build_swim_transitions
    for direction in ['east','west','north','south']:build_swim_transitions(install=True,direction=direction)
    from build_marsh_swim_turns import build as build_swim_turns, PAIRS as SWIM_TURN_PAIRS
    for pair in SWIM_TURN_PAIRS:build_swim_turns(install=True,pair=pair)
    from build_marsh_opposite_swim_turns import build as build_opposite_turns, PAIRS as OPPOSITE_PAIRS
    for pair in OPPOSITE_PAIRS:build_opposite_turns(install=True,pair=pair)
    from build_marsh_carry_turns import build as build_carry_turns, PAIRS as CARRY_TURN_PAIRS
    for pair in CARRY_TURN_PAIRS:build_carry_turns(install=True,pair=pair)
    from build_marsh_opposite_carry_turns import build as build_opposite_carry, PAIRS as OPPOSITE_CARRY_PAIRS
    for pair in OPPOSITE_CARRY_PAIRS:build_opposite_carry(install=True,pair=pair)
    from install_marsh_carry_chain import install_turns as install_matched_carry_turns
    install_matched_carry_turns(backup=False)
    from build_marsh_loaded_swim import build as build_loaded_swim, DIRECTIONS as LOADED_DIRECTIONS
    for direction in LOADED_DIRECTIONS:build_loaded_swim(install=True,direction=direction)
    from install_marsh_swim_pickup_match import install as install_matched_swim_pickup
    install_matched_swim_pickup(backup=False)
    from build_marsh_swim_carry_turns import build as build_loaded_turns, PAIRS as LOADED_TURN_PAIRS
    for pair in LOADED_TURN_PAIRS:build_loaded_turns(install=True,pair=pair)
    from build_marsh_opposite_swim_carry_turns import build as build_loaded_half_turns, PAIRS as LOADED_HALF_PAIRS
    for pair in LOADED_HALF_PAIRS:build_loaded_half_turns(install=True,pair=pair)
    from build_marsh_cargo_drain import build as build_cargo_drain, DIRECTIONS as CARGO_DRAIN_DIRECTIONS
    for direction in CARGO_DRAIN_DIRECTIONS:build_cargo_drain(install=True,direction=direction)
    from install_marsh_cargo_drain_endpoint import install as install_cargo_drain_endpoint
    install_cargo_drain_endpoint(backup=False)
    from install_marsh_cargo_drain_match import install as install_matched_cargo_drain
    install_matched_cargo_drain(backup=False)
    finalize('marsh')
    from install_marsh_water_match import install as install_matched_water
    install_matched_water(backup=False)
    from install_marsh_water_turn_match import install as install_matched_water_turns
    install_matched_water_turns(backup=False)
    from install_marsh_loaded_water_match import install as install_matched_loaded_water
    install_matched_loaded_water(backup=False)
    from prepare_marsh_controller_tone import install as install_controller_tone
    install_controller_tone(backup=False)
    from prepare_marsh_full_polish import install as install_full_polish
    install_full_polish()
    from polish_marsh_swim_joins import build as build_swim_joins
    build_swim_joins(install=True)
    from build_marsh_swim_stroke import build as build_swim_stroke
    build_swim_stroke(install=True)
    from polish_marsh_locomotion_joins import build as build_locomotion_joins
    build_locomotion_joins(install=True)
    from register_marsh_east_run import build as register_east_run
    register_east_run(install=True)
    from polish_marsh_work_joins import build as build_work_joins
    build_work_joins(install=True)
    from build_marsh_torch_tips import build as build_torch_tips
    build_torch_tips()
    from build_marsh_south_chat_polish import build as build_south_chat
    build_south_chat(install=True)
    from build_marsh_rest_polish import build as build_rest_polish
    build_rest_polish(install=True)
    from build_marsh_meal_polish import build as build_meal_polish
    build_meal_polish(install=True)
    from build_marsh_water_actions import build as build_water_actions
    build_water_actions(install=True)
    from build_marsh_underwater_mining import build as build_underwater_mining
    build_underwater_mining(install=True)
    (QA/'body-build.json').write_text(json.dumps({'states':states,'sourceHashes':{**shared.SOURCE_HASHES,**PROVENANCE},'operations':shared.OPS,'frames':records,'padding':padding,'legacyFramesReproduced':len(contract['sourceFrames'])},indent=2)+'\n')
    print(json.dumps({'bodyStates':len(states),'bodyReferences':sum(e['frames'] for e in states),'sourceFramesReproduced':len(contract['sourceFrames']),'paletteColors':color_count}))


if __name__=='__main__': main()
