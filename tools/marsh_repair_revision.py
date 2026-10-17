"""Explicit diagnostic maintenance chain; never changes welding/source aliases."""
from pathlib import Path
from PIL import Image,ImageDraw
import rebuild_bill_art as shared
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-maintenance-match-v1'
OUT=BASE/'review/canonical-chain'
DIRECTIONS=['east','west','north','south']
STATES={a+'-'+d for a in ['kneel','repair','stand'] for d in DIRECTIONS}
_cache={}

def build(direction):
    folder=ROOT/'character/marsh-controller-tone-v1/frames'
    result={state:[Image.open(folder/state/f'{i:03}.png').convert('RGBA') for i in range(6 if state.startswith('repair-') else 3)]
            for state in ('kneel-'+direction,'repair-'+direction,'stand-'+direction)}
    draw=result['kneel-'+direction];work=result['repair-'+direction];stow=result['stand-'+direction]
    assert draw[-1].tobytes()==work[0].tobytes()
    assert work[-1].tobytes()==stow[0].tobytes()
    return result


def replacement(actor,state,equipped):
    if actor!='marsh' or state not in STATES:return None
    direction=state.rsplit('-',1)[1]
    if direction not in _cache:_cache[direction]=build(direction)
    shared.OPS['marsh/'+state]={'method':'Selected identity-matched diagnostic chain, active idle endpoints and exact shared controller joins',
                              'recipe':f'character/marsh-maintenance-match-v1/review/{direction}/registration.json'}
    return {'bare':[f.copy() for f in _cache[direction][state]]}

def preview():
    OUT.mkdir(parents=True,exist_ok=True)
    rows={d:build(d) for d in DIRECTIONS}
    frames=[]
    # Controller dwell: 1s draw, 4s checking, 1s stow (clips hold their endpoints).
    for sample in range(180):
        t=sample/30;board=Image.new('RGB',(368,428),'#17212a');draw=ImageDraw.Draw(board)
        action='kneel' if t<1 else ('repair' if t<5 else 'stand')
        elapsed=t if t<1 else (t-1 if t<5 else t-5)
        i=min(5,int((elapsed%.9)/.15)) if action=='repair' else min(2,int(elapsed/.2))
        for col,d in enumerate(DIRECTIONS):
            x=(col%2)*184;y=(col//2)*214
            f=rows[d][action+'-'+d][i];board.paste(f,(x,y+30),f);draw.text((x+5,y+5),d+' / '+action,fill='white')
        frames.append(board)
    frames[0].save(OUT/'chain.gif',save_all=True,append_images=frames[1:],duration=[33]*180,loop=0)
    frames[50].save(OUT/'contact.png')
    print('48 candidate frames; four connected diagnostic chains; no runtime writes')

if __name__=='__main__':preview()
