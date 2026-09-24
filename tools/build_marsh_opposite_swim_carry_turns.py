"""Compose loaded-swimming half-turns through exact shared cardinal poses."""
import argparse,hashlib
from build_marsh_swim_carry_turns import BASE,build as adjacent,write_clips
PAIRS={'east-west':('east-north','west-north','north'),
       'north-south':('east-north','east-south','east')}

def build(install=False,pair='east-west'):
    first,second,via=PAIRS[pair];origin,destination=pair.split('-')
    a=adjacent(pair=first)[f'swim-carry-turn-{origin}-{via}']
    b=adjacent(pair=second)[f'swim-carry-turn-{via}-{destination}']
    assert a[-1].tobytes()==b[0].tobytes(),'Shared cardinal join changed'
    row=a+b[1:];clips={f'swim-carry-turn-{pair}':row,f'swim-carry-turn-{destination}-{origin}':list(reversed(row))}
    write_clips(clips,[60,90,100,90,120,90,100,90,60],
        [origin,origin,via,via,via,via,destination,destination,destination],BASE/f'review/{pair}-01',
        dict(derived=f'Concatenated {origin}-{via} and {via}-{destination}; identical middle stored once with combined120ms duration. Return reverses poses. No new art or mirroring.',
             sourceManifests={p:hashlib.sha256((BASE/f'review/{p}-01/manifest.json').read_bytes()).hexdigest() for p in [first,second]}),install,pair)
    return clips

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--install',action='store_true');p.add_argument('--pair',choices=PAIRS,default='east-west');a=p.parse_args();build(a.install,a.pair)
