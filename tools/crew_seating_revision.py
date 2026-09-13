"""Selected seating sources, rebuilt independently of exported runtime frames."""
from pathlib import Path
import contextlib, io, re
from extract_crew_seating_study import main as extract

SELECTED={(actor,direction) for actor in ['veld','branforth'] for direction in ['east','north','south','west']}
_frames={}

def matches(actor,path):
    path=Path(path);state,_,direction=path.parent.name.rpartition('-')
    return (actor,direction) in SELECTED and path.parent.parent.name==actor and 'crew-life-v1' in path.parts and state in ['sit-down','sit-idle']

def replacement(actor,path):
    if not matches(actor,path):return None
    path=Path(path);state,_,direction=path.parent.name.rpartition('-');key=(actor,direction)
    if key not in _frames:
        with contextlib.redirect_stdout(io.StringIO()):_frames[key]=extract(actor,direction)
    index=int(re.search(r'(\d+)\.png$',path.name)[1])
    return _frames[key][state][index].copy()
