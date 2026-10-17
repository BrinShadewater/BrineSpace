from pathlib import Path
import shutil
P=Path(__file__).resolve().parent;archive=P/'revisions/material-v3'
assert not archive.exists(),'Revision already archived; rebuild directly'
archive.mkdir(parents=True)
for name in ['frames','build.py','prepare_tools.py','source-rulers.json','registration.json','manifest.json','frame-hashes.json','verification.json','candidate-evidence.json','HANDOFF.md','contact-sheet.png']:
    f=P/name
    if f.is_dir():shutil.copytree(f,archive/name)
    elif f.exists():shutil.copy2(f,archive/name)
s=(P/'build.py').read_text(encoding='utf-8')
s=s.replace('from scipy.ndimage import binary_dilation','from scipy.ndimage import binary_dilation\nfrom grade_materials import apply')
s=s.replace("prepared={key:module.prepare(P/s['source'],s['heads'],s['count'],s['density']) for key,s in cfg['sources'].items()}","prepared={key:apply(module.prepare(P/s['source'],s['heads'],s['count'],s['density']),s,module.IDLE) for key,s in cfg['sources'].items()}")
(P/'build.py').write_text(s,encoding='utf-8')
s=(P/'prepare_tools.py').read_text(encoding='utf-8')
s=s.replace("if name=='build_preview.py':", "if name=='build.py':\n  s=s.replace('from scipy.ndimage import binary_dilation','from scipy.ndimage import binary_dilation\\nfrom grade_materials import apply')\n  s=s.replace(\"prepared={key:module.prepare(P/s['source'],s['heads'],s['count'],s['density']) for key,s in cfg['sources'].items()}\",\"prepared={key:apply(module.prepare(P/s['source'],s['heads'],s['count'],s['density']),s,module.IDLE) for key,s in cfg['sources'].items()}\")\n if name=='build_preview.py':")
(P/'prepare_tools.py').write_text(s,encoding='utf-8')
