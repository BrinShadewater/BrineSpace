"""Read-only profile fingerprint for isolated Marsh validation intervals."""
from pathlib import Path
import hashlib,json,os,sys
root=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
records={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file() and 'logs' not in p.relative_to(root).parts}
out=Path(sys.argv[1]);out.write_text(json.dumps(records,indent=2)+'\n')
print(len(records),'non-log profile fingerprints saved')
