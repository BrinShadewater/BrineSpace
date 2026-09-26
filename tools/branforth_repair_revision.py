"""Selected repair chains; explicit states avoid changing shared legacy aliases."""
from pathlib import Path
import contextlib
import io
import rebuild_bill_art as shared

STATES = {action+'-'+direction for action in ['kneel','repair','stand'] for direction in ['south','north','west']}
_rows = {}

def replacement(actor, state, equipped):
    global _rows
    if actor != 'branforth' or state not in STATES:
        return None
    direction = state.rsplit('-',1)[1]
    if direction not in _rows:
        if direction == 'south':
            from prepare_branforth_south_repair_chain import build
        elif direction == 'north':
            from prepare_branforth_north_repair_chain import build
        else:
            from prepare_branforth_west_repair_chain import build
        with contextlib.redirect_stdout(io.StringIO()):
            _rows[direction] = build()
    base = shared.ROOT / 'character/crew-repair-polish-v1/sources'
    sources = [f'branforth-repair-{direction}-01.png', f'branforth-kneel-{direction}-02.png',
               f'branforth-idle-{direction}-bare-endpoint.png', f'branforth-idle-{direction}-helmet-endpoint.png']
    if direction == 'west':
        from prepare_branforth_west_repair_chain import SOURCE_NAMES
        sources = SOURCE_NAMES
    for source in sources:
        shared.image(base / source)
    shared.OPS[actor + '/' + state] = {
        'method': 'Fixed source scale, planted boot, exact frozen idle and repair joins; stand reverses kneel. West preserves canonical face and helmet and uses authored pose holds.',
        'sources': [str((base / source).relative_to(shared.ROOT)) for source in sources],
    }
    result = {'bare': [frame.copy() for frame in _rows[direction][0][state]]}
    if equipped:
        result['helmet'] = [frame.copy() for frame in _rows[direction][1][state]]
    return result
