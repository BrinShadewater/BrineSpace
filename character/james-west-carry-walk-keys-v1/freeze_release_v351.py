import sys,hashlib,json,shutil,subprocess
from pathlib import Path
r=Path.cwd();sys.path.insert(0,str(r));from tools.build_release_manifest import collect
o=r/'output/james-release-closeout-v351';f=o/'frozen-project';f.mkdir(parents=True,exist_ok=False)
selected,reasons=collect(r)
selected.update(['export_presets.cfg','addons/brine_raw_export/plugin.gd','addons/brine_raw_export/plugin.cfg','tools/export_release.ps1','tools/build_release_manifest.py','tools/set_raw_png_import_keep.py'])
for name in list(selected):
    uid=r/(name+'.uid')
    if uid.is_file():selected.add(name+'.uid')
for name in ['output/export-tools/4.7.2-stable/windows_release_x86_64.exe','output/export-tools/4.7.2-stable/windows_debug_x86_64.exe']:selected.add(name)
rows=[]
for name in sorted(selected):
    src=r/name;dest=f/name;dest.parent.mkdir(parents=True,exist_ok=True)
    data=src.read_bytes()
    if src.suffix.lower() in {'.png','.jpg','.jpeg','.webp'} and data.startswith(b'version https://git-lfs.github.com/spec/'):raise RuntimeError('LFS pointer: '+name)
    dest.write_bytes(data);digest=hashlib.sha256(data).hexdigest();assert hashlib.sha256(dest.read_bytes()).hexdigest()==digest
    rows.append({'path':name,'bytes':len(data),'sha256':digest})
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip()
digest=hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest()
(o/'frozen-inputs.json').write_text(json.dumps({'sourceProject':str(r),'frozenProject':str(f),'baseCommit':head,'frozenSha256':digest,'files':rows,'scope':'Physical selected dependency snapshot and maintained Windows exporter/tools/templates. Uses source Git metadata read-only during exporter; this directory is a dependency snapshot, not a Git checkout. No shared-source export mutation.'},indent=2))
print(json.dumps({'frozenProject':str(f),'files':len(rows),'bytes':sum(x['bytes'] for x in rows),'sha256':digest}),flush=True)
