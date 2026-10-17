"""Candidate player check with isolated profile and exact evidence hashes."""
from pathlib import Path
import hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent
real=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fingerprint():return {str(p.relative_to(real)):sha(p) for p in real.rglob('*') if p.is_file()}
before=fingerprint();(H/'profile-before-candidate-v1.json').write_text(json.dumps(before,indent=2))
env=os.environ.copy();env['APPDATA']=str(R/'output/veld-water-material-scratch-cargo-south-v1');Path(env['APPDATA']).mkdir(exist_ok=True)
run=subprocess.run(['C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe','--path',str(R),'-s','res://tools/review_veld_swim_carry_south_coherent_v1.gd'],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
(H/'native-candidate-v1.log').write_bytes(run.stdout);after=fingerprint();log=run.stdout.decode(errors='replace')
errors=[x.strip() for x in log.splitlines() if x.startswith(('SCRIPT ERROR:','ERROR:'))]
match=re.search(r'VELD SOUTH WATER CARGO CANDIDATE: (\d+) checks, (\d+) failures',log)
manifests={};frames={}
for gear in ['bare','helmet']:
 p=H/(gear+'-manifest.json');manifests[p.name]=sha(p)
 for s in json.loads(p.read_text())['states']:
  for f in s['frameFiles']:frames[f]=sha(H/f)
report=dict(exit_code=run.returncode,checks=int(match[1]) if match else None,failures=int(match[2]) if match else None,engine_errors=errors,real_profile_changed_files=[k for k in set(before)|set(after) if before.get(k)!=after.get(k)],scratch_appdata=env['APPDATA'],candidateLoadedExplicitly=True,installed=False,manifestHashes=manifests,frameHashes=frames,fixtureSha256=sha(R/'tools/review_veld_swim_carry_south_coherent_v1.gd'),logSha256=sha(H/'native-candidate-v1.log'),scope='Paired candidate loading, exact pixels, metadata, every elapsed/distance phase, two loop seams, pause and player snapshot; not world routing or cargo pickup/turn handoffs')
(H/'native-candidate-v1-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(log[-650:]);print('real profile changes',len(report['real_profile_changed_files']))
assert not errors and run.returncode==0 and match and report['failures']==0 and not report['real_profile_changed_files']
