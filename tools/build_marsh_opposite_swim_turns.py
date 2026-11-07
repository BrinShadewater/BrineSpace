"""Compose half-turns from registered, independently authored quarter-turns."""
import argparse, hashlib, json, shutil
from PIL import Image, ImageDraw
from build_marsh_swim_turns import ROOT, BASE, build as adjacent

PAIRS={'east-west':('east-north','west-north','north'),
       'north-south':('east-north','east-south','east')}

def build(install=False,pair='east-west'):
    first,second,via=PAIRS[pair]
    origin,destination=pair.split('-')
    a=adjacent(pair=first)[f'swim-turn-{origin}-{via}']
    b=adjacent(pair=second)[f'swim-turn-{via}-{destination}']
    assert a[-1].tobytes()==b[0].tobytes(),'Shared cardinal join changed'
    row=a+b[1:]
    durations=[60,90,100,90,120,90,100,90,60]
    facings=[origin,origin,via,via,via,via,destination,destination,destination]
    clips={f'swim-turn-{pair}':row,f'swim-turn-{destination}-{origin}':list(reversed(row))}
    out=BASE/f'review/{pair}-01';out.mkdir(parents=True,exist_ok=True)
    states=[]
    for key,frames in clips.items():
        files=[]
        for i,frame in enumerate(frames):
            name=f'{key}-{i:03}.png';frame.save(out/name);files.append(name)
        states.append(dict(id=key,frameFiles=files,frameDurationsMs=durations,loop=False,
            facings=facings if key.endswith(pair) else list(reversed(facings)),
            waterKinds=['transition']*9,waterPoses=[True]*9,depthOffsets=[0.0]*9))
    manifest=dict(frameWidth=184,frameHeight=208,pivot=[92,172],standingHeight=148,states=states)
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    provenance=dict(derived=f'Concatenated {origin}-{via} and {via}-{destination}; identical center frame stored once with combined 120 ms duration. Return reverses poses. No new art or mirroring.',
        sourceManifests={p:hashlib.sha256((BASE/f'review/{p}-01/manifest.json').read_bytes()).hexdigest() for p in [first,second]})
    (out/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    board=Image.new('RGB',(184*9,232),'#17212a')
    for i,frame in enumerate(row):board.paste(frame,(184*i,24),frame)
    board.save(out/'contact.png')
    preview=[]
    for key,frames in clips.items():
        for frame in frames:
            board=Image.new('RGB',(240,244),'#17212a');ImageDraw.Draw(board).text((8,6),key,fill='white');board.paste(frame,(28,28),frame);preview.append(board)
    preview[0].save(out/'motion.gif',save_all=True,append_images=preview[1:],duration=[350,*durations[1:-1],350]*2,loop=0)
    if install:
        runtime=ROOT/'character/marsh-v2';relative=f'supplemental/swim-turn-{pair}';folder=runtime/relative;folder.mkdir(parents=True,exist_ok=True)
        for state in states:
            for name in state['frameFiles']:shutil.copyfile(out/name,folder/name)
        for name in ['manifest.json','provenance.json']:shutil.copyfile(out/name,folder/name)
        path=runtime/'catalog.json';catalog=json.loads(path.read_text())
        if relative+'/manifest.json' not in catalog['body']:catalog['body'].append(relative+'/manifest.json')
        path.write_text(json.dumps(catalog,indent=2)+'\n')
    print(pair+': 18 frames; '+('installed' if install else 'review only'))
    return clips

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--install',action='store_true');parser.add_argument('--pair',choices=PAIRS,default='east-west');args=parser.parse_args();build(args.install,args.pair)
