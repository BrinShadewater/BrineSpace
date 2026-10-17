import pathlib,subprocess,json,shutil,os,re
b=pathlib.Path('/Users/Shared/BrineSpace-native-validation-evidence-20261017');home=b/'release-benchmark-home';profile=home/'Library/Application Support/Godot/app_userdata/BrineSpace-NativeValidation-20261017';profile.mkdir(parents=True,exist_ok=True);rows=[]
for i in range(1,4):
 out=b/'release-benchmark'/str(i);out.mkdir(parents=True,exist_ok=True);shutil.copy2('/Users/Shared/BrineSpace-iPad-compact-evidence/checkpoint-before-update.save',profile/'input.save')
 layout=pathlib.Path('/Users/alexyesilcimen/Library/Application Support/Godot/app_userdata/BrineSpace/room_layouts.json')
 if layout.exists():shutil.copy2(layout,profile/'room_layouts.json')
 env=dict(os.environ,HOME=str(home),BRINE_EXPECTED_PROFILE=str(profile),BRINE_SILENT='1');result=out/'result.json';cmd=['/usr/bin/time','-l',str(b/'mac-qa/BrineSpace.app/Contents/MacOS/BrineSpace'),'--windowed','--resolution','1600x900','--',f'--user-dir={profile}',f'--save={profile/"input.save"}','--scenario=large','--width=1600','--height=900','--frames=180','--actions=idle,zoom,placement',f'--out={result}']
 with (out/'run.log').open('w') as f:
  try:r=subprocess.run(cmd,env=env,stdout=f,stderr=f,timeout=360);code=r.returncode
  except subprocess.TimeoutExpired:code=-1
 text=(out/'run.log').read_text(errors='replace');m=re.search(r'(\d+)\s+maximum resident set size',text);p=re.search(r'(\d+)\s+peak memory footprint',text);d=json.loads(result.read_text()) if result.exists() else {};valid=code==0 and 'RELEASE BENCHMARK COMPLETE' in text and 'ERROR:' not in text and d.get('debug') is False and d.get('automatic_reports_enabled') is False and d.get('automatic_reports_saved')==0
 rows.append({'visit':i,'code':code,'valid':valid,'debug':d.get('debug'),'max_rss_bytes':int(m[1]) if m else None,'peak_physical_footprint_bytes':int(p[1]) if p else None,'result':str(result)});(b/'release-benchmark-summary.json').write_text(json.dumps(rows,indent=2)+'\n');print(i,code,valid,flush=True)
 if not valid:print(text[-4000:],flush=True);break
