"""Compose unmodified native room crops; preserve original full captures."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-seated-north-station-v1'
validation=json.loads((O/'validation.json').read_text());assert validation['runtimePassed']
phases=['entry','down-1','down-2','down-3','down-4','down-5','held','rise-0','rise-1','rise-2','rise-3','rise-4','rise-5','exit']
for phase in ['entry','down-3','held','rise-2','exit','legacy-depth']:
    board=Image.new('RGB',(820,1980),'#202a30');d=ImageDraw.Draw(board)
    for rotation in range(4):
        for gear_index,gear in enumerate(['bare','helmet']):
            path=O/f'rotation-{rotation}-{gear}-{phase}.png'
            image=Image.open(path).convert('RGB').crop((250,215,660,690))
            x=gear_index*410;y=rotation*495
            board.paste(image,(x,y+20));d.text((x+6,y+4),f'Rotation {rotation} / {gear} / {phase}',fill='white')
    board.save(O/f'{phase}-room-board.png')
for rotation in range(4):
    board=Image.new('RGB',(14*156,2*264),'#202a30');d=ImageDraw.Draw(board)
    for row,gear in enumerate(['bare','helmet']):
        for col,phase in enumerate(phases):
            image=Image.open(O/f'rotation-{rotation}-{gear}-{phase}.png').convert('RGB').crop((270,280,348,402)).resize((156,244),Image.Resampling.NEAREST)
            board.paste(image,(col*156,row*264+20));d.text((col*156+3,row*264+3),f'{gear} {phase}',fill='white')
    board.save(O/f'rotation-{rotation}-all-poses.png')
contacts=json.loads((O/'contacts.json').read_text())
names={record['screenshot'] for record in contacts['records']}
names.update(f'rotation-{i}-{gear}-legacy-depth.png' for i in range(4) for gear in ['bare','helmet'])
names.update(f'{phase}-room-board.png' for phase in ['entry','down-3','held','rise-2','exit','legacy-depth'])
names.update(f'rotation-{i}-all-poses.png' for i in range(4))
names.update(['native.log','validation.json','profile-before.json','profile-after.json','contacts.json','final.png'])
files=[O/name for name in sorted(names)]+[R/'tests/test_veld_seated_north_station.gd',R/'tests/test_veld_seated_north_station.gd.uid',R/'tools/run_veld_seated_north_station.py']
evidence={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(P/'station-capture-evidence.json').write_text(json.dumps({'scope':'Native default lounge, fixture-only marked candidate, registered chair-front minimum depth; corrected vs unmarked held captures, full source slots/endpoints; controlled interruption/pose admission, not natural service-loss/fresh Continue/owner acceptance','ownerAccepted':False,'files':evidence},indent=2)+'\n')
print(f'{len(evidence)} evidence files, six room phase boards and four complete pose boards')
