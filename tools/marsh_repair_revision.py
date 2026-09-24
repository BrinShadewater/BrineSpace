"""Explicit diagnostic maintenance chain; never changes welding/source aliases."""
from pathlib import Path
import contextlib,io,json,hashlib
from PIL import Image,ImageDraw
import rebuild_bill_art as shared
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/crew-repair-polish-v1'
OUT=BASE/'review/marsh-diagnostic-repair-01'
DIRECTIONS=['east','west','north','south']
STATES={a+'-'+d for a in ['kneel','repair','stand'] for d in DIRECTIONS}
_cache={}

def build(direction):
    from veld_scanner_revision import replacement as diagnostic
    with contextlib.redirect_stdout(io.StringIO()):
        source=diagnostic('marsh','interact-'+direction,False)['bare']
    idle_path=BASE/f'sources/marsh/idle-{direction}.png'
    idle=shared.image(idle_path).copy()
    draw=[idle,source[4].copy(),source[2].copy()]
    order=[2,1,2,3,2,2] if direction=='east' else [2,3,2,1,2,2]
    result={'kneel-'+direction:draw,'repair-'+direction:[source[i].copy() for i in order],
            'stand-'+direction:list(reversed(draw))}
    OUT.mkdir(parents=True,exist_ok=True)
    for state,row in result.items():
        for i,frame in enumerate(row):frame.save(OUT/f'{state}-{i:03}.png')
    assert draw[-1].tobytes()==result['repair-'+direction][0].tobytes()
    assert result['repair-'+direction][-1].tobytes()==result['stand-'+direction][0].tobytes()
    (OUT/f'{direction}-recipe.json').write_text(json.dumps(dict(status='selected_runtime_chain',idleSource=str(idle_path.relative_to(ROOT)),idleSha256=hashlib.sha256(idle_path.read_bytes()).hexdigest(),diagnosticSource='tools/veld_scanner_revision.py: interact-'+direction,draw=['canonical idle',4,2],work=order,stow='reverse draw',semantics='Equipment-check stages keep legacy kneel/repair/stand IDs; Marsh uses a handheld diagnostic controller.',limits=['Derived from preserved authored instrument poses; no newly generated motion','Not owner accepted']),indent=2)+'\n')
    return result

def replacement(actor,state,equipped):
    if actor!='marsh' or state not in STATES:return None
    direction=state.rsplit('-',1)[1]
    if direction not in _cache:_cache[direction]=build(direction)
    shared.OPS['marsh/'+state]={'method':'Explicit maintenance diagnostic chain, canonical idle, existing authored controller poses, exact joins; no welding alias mutation',
                              'recipe':f'character/crew-repair-polish-v1/review/marsh-diagnostic-repair-01/{direction}-recipe.json'}
    return {'bare':[f.copy() for f in _cache[direction][state]]}

def preview():
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
