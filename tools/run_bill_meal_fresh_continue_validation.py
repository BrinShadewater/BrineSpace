"""Twenty independent normal title-Continue processes, each on its own scratch copy."""
from pathlib import Path
import concurrent.futures,json,os,re,shutil,subprocess,sys,time
from run_bill_death_ground_normal_mortality_validation import fingerprint
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'output/bill-meal-fresh-continue-v1'
SOURCE=ROOT/'output/bill-meal-continue-producer-v1'
def run_case(godot,item):
 case=OUT/'cases'/item['id'];case.mkdir(parents=True,exist_ok=True)
 scratch=case/'scratch-appdata';profile=scratch/'Godot/app_userdata/BrineSpace';profile.mkdir(parents=True,exist_ok=True)
 source_profile=SOURCE/'scratch-appdata/Godot/app_userdata/BrineSpace'
 for source in source_profile.iterdir():
  if source.is_file() and source.suffix not in ['.tmp']:shutil.copy2(source,profile/source.name)
 before=fingerprint();(case/'profile-before.json').write_text(json.dumps(before,indent=2)+'\n')
 env=os.environ.copy();env['APPDATA']=str(scratch)
 start=time.monotonic();epoch=time.time()
 with (case/'native.log').open('w',encoding='utf-8') as log:
  try:code=subprocess.run([str(godot),'--path',str(ROOT),'--script','res://tests/test_bill_meal_fresh_continue.gd','--resolution','1280x900','--','--case='+item['id']],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=180).returncode
  except subprocess.TimeoutExpired:code=-1
 after=fingerprint();(case/'profile-after.json').write_text(json.dumps(after,indent=2)+'\n')
 changes=[key for key in before.keys()|after.keys() if before.get(key)!=after.get(key)]
 log=(case/'native.log').read_text(encoding='utf-8');counts=re.search(r'BILL MEAL FRESH CONTINUE: (\d+) checks,(\d+) failures',log)
 photo=OUT/(item['id']+'.png');fresh=photo.exists() and photo.stat().st_mtime>=epoch
 native=code==0 and counts is not None and int(counts[2])==0 and 'SCRIPT ERROR' not in log and 'ERROR:' not in log and fresh
 result={'id':item['id'],'nativePassed':native,'passed':native and not changes,'returnCode':code,'checks':int(counts[1]) if counts else None,'seconds':round(time.monotonic()-start,2),'scratchAPPDATA':str(scratch),'realProfileFileCount':len(before),'realProfileChanges':changes,'freshCapture':fresh}
 (case/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result),flush=True);return result
def main():
 godot=Path(sys.argv[1]);assert godot.is_file();OUT.mkdir(exist_ok=True)
 items=json.loads((SOURCE/'continue-cases.json').read_text());assert len(items)==20 and len({i['id'] for i in items})==20
 assert not (OUT/'validation.json').exists(), 'Preserve existing interval; make a new revision for further proof.'
 start=time.monotonic()
 # Validate the first real menu flow before spending on the rest of the matrix.
 results=[run_case(godot,items[0])]
 if results[0]['nativePassed']:
  with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
   results.extend(pool.map(lambda item:run_case(godot,item),items[1:]))
 report={'passed':len(results)==20 and all(r['passed'] for r in results),'nativePassed':len(results)==20 and all(r['nativePassed'] for r in results),'processes':len(results),'checks':sum(r['checks'] or 0 for r in results),'seconds':round(time.monotonic()-start,2),'scope':'normal loader; actual title Continue; fresh independent engine processes on separate scratch copies; two actual galley contacts/two bare actions/draw-use-stow-cancel-draw-cancel-use matrix','results':results}
 (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='results'}));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
