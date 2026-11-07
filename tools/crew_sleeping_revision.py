"""Selected sleeping sources; source extraction is independent of runtime exports."""
from pathlib import Path
import contextlib,io,re
from extract_crew_seating_study import main as extract

SELECTED={(actor,direction) for actor in ['veld','branforth'] for direction in ['north','east','west','south']}
SIDE_POSES=[(129,93,0),(141,127,-15),(102,159,0),(71,168,15),(65,189,40),(63,210,85)]
SIDE_FITS={('veld','east'):SIDE_POSES,('branforth','east'):[(129,91,0),(139,140,-15),(118,155,0),(75,172,15),(59,182,40),(55,208,85)],('veld','west'):[(128,89,0),(116,151,15),(156,160,0),(183,173,-15),(175,187,-40),(202,207,-85)]}
_frames={}
_south_equipment={}
SIDE_FITS[('branforth','west')]=[(128,89,0),(102,134,15),(152,156,0),(139,173,-25),(208,200,-75),(207,200,-75)]
def matches(actor,path):
    path=Path(path);state,_,direction=path.parent.name.rpartition('-')
    return (actor,direction) in SELECTED and path.parent.parent.name==actor and 'crew-life-v1' in path.parts and state in ['lie-down','sleep']
def replacement(actor,path):
    if not matches(actor,path):return None
    path=Path(path);state,_,direction=path.parent.name.rpartition('-');key=(actor,direction)
    if key not in _frames:
        with contextlib.redirect_stdout(io.StringIO()):
            if key==('veld','east'):
                _frames[key]=extract(actor,direction,'06','sleeping','gutter',True)
            elif key in [('branforth','east'),('veld','west'),('branforth','west')]:
                from repair_branforth_side_sleep import main as breathing
                _frames[key]=extract(actor,direction,'01','sleeping','gutter')
                _frames[key]['sleep']=breathing(actor,direction)
            elif direction=='south':_frames[key]=extract(actor,direction,'01','sleeping','gutter')
            else:_frames[key]=extract(actor,direction,family='sleeping')
    index=int(re.search(r'(\d+)\.png$',path.name)[1])
    return _frames[key][state][index].copy()

def south_equipped(actor,path):
    if not matches(actor,path) or not Path(path).parent.name.endswith('-south'):return None
    if actor not in _south_equipment:
        from extract_south_sleep_equipment import main as equipment
        with contextlib.redirect_stdout(io.StringIO()):_south_equipment[actor]=equipment(actor)
    path=Path(path);state=path.parent.name.rsplit('-',1)[0]
    index=int(re.search(r'(\d+)\.png$',path.name)[1])
    return _south_equipment[actor][state][index].copy()

def side_equipped(actor,path,body,overlay):
    from PIL import Image
    path=Path(path)
    key=(actor,path.parent.name.rsplit('-',1)[-1])
    if not matches(actor,path) or key not in SIDE_FITS:return None
    index=int(re.search(r'(\d+)\.png$',path.name)[1])
    poses=SIDE_FITS[key]
    x,y,angle=poses[index] if path.parent.name.startswith('lie-down') else poses[-1]
    helmet=overlay.rotate(angle,Image.Resampling.NEAREST,expand=True)
    out=body.copy();out.alpha_composite(helmet,(round(x-helmet.width/2),round(y-helmet.height/2)))
    return out
