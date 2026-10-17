from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json, hashlib

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent.parent
sources=json.loads((ROOT/'sources.json').read_text())
for source in sources['sources']:
    assert hashlib.sha256((REPO/source['path']).read_bytes()).hexdigest()==source['sha256']
files=['index.html','neutral-comparison.png','sources.json','HANDOFF.md','walk.mp4','tablet.mp4']
with ZipFile(ROOT/'Kris-Krug-current-family-review.zip','w',ZIP_DEFLATED) as z:
    for name in files:z.write(ROOT/name,name)
with ZipFile(ROOT/'Kris-Krug-current-family-review.zip') as z:
    assert z.testzip() is None and len(z.namelist())==6
print('Four source hashes verified; six-file review ZIP verified. Original art unchanged.')
