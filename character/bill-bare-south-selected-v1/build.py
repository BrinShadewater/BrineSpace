"""Freeze the owner-selected bare south whole figures."""
import hashlib,json,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'bill-bare-south-coherent-v1'
manifest=json.loads((SOURCE/'manifest.json').read_text())
manifest.update(name='Bill selected bare south actions',status='owner_visual_accepted_2026_09_29')
hashes={}
for state in manifest['states']:
    for rel in state['frameFiles']:
        dest=HERE/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(SOURCE/rel,dest)
        hashes[rel]=hashlib.sha256(dest.read_bytes()).hexdigest()
for name,data in [('manifest.json',manifest),('frame-hashes.json',hashes)]:
    (HERE/name).write_text(json.dumps(data,indent=2)+'\n')
print('Selected bare south: 24 frames, four states')
