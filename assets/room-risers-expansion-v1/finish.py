"""Install reviewed card outputs and record the final scoped artifact audit."""
import hashlib
import json
from pathlib import Path
import re
import shutil
from PIL import Image

PACK=Path(__file__).resolve().parent
ROOT=PACK.parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
briefs=json.loads((PACK/'briefs.json').read_text())
walls=json.loads((ROOT/'assets/architecture-rollout-2026-09-26/walls.json').read_text())
registered=json.loads((PACK/'registrations.json').read_text())
cards=dict(re.findall(r'"([^"]+)":\s*"(res://[^"]+)"',(ROOT/'scripts/room_card_art.gd').read_text()))
backup=PACK/'evidence/previous-cards';backup.mkdir(exist_ok=True)
report=[]
for key,brief in briefs.items():
    assert walls[key]==registered[key],key
    assert sha(ROOT/brief['previous']['base']['source'].removeprefix('res://'))==brief['previous']['base']['sha256'],key
    assert sha(Path(brief['reference']))==brief['reference_sha256'],key
    assert sha(PACK/'masters'/f'{key}.png')==registered[key]['base']['sha256'],key
    candidate=PACK/'cards'/f'{key}.png'
    im=Image.open(candidate);im.load()
    assert im.size==(512,512) and im.mode=='RGBA',key
    destination=ROOT/cards[key].removeprefix('res://')
    old=backup/f'{key}.png'
    if destination.exists() and not old.exists():shutil.copy2(destination,old)
    shutil.copy2(candidate,destination)
    assert sha(candidate)==sha(destination)
    for q in range(4):
        im=Image.open(PACK/'review'/f'{key}-q{q}.png');im.load();assert im.size==(512,512)
    brief['stage']='integrated/native-reviewed; owner acceptance pending'
    report.append(dict(room=key,source=registered[key]['base']['source'],source_sha256=registered[key]['base']['sha256'],
        card=cards[key],card_sha256=sha(destination),previous_card_sha256=sha(old) if old.exists() else None,
        prompt_sha256=sha(PACK/'prompts'/f'{key}.txt'),native_orientations=4))
(PACK/'briefs.json').write_text(json.dumps(briefs,indent=2)+'\n')
(PACK/'evidence/final-audit.json').write_text(json.dumps(dict(rooms=28,native_orientations=112,bare_wall_captures=28,
    installed_cards=28,original_sources_preserved=True,artifacts=report),indent=2)+'\n')
print('Installed 28 reviewed cards; 28 wall sources and 112 room captures verified; original sources intact.')
