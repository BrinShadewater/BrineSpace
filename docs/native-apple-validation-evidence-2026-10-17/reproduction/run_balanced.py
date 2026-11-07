import pathlib,sys,subprocess,json,shutil,time,os,re,hashlib
base=pathlib.Path('/Users/Shared/BrineSpace-native-validation-evidence-20261017');sys.path.insert(0,'/Users/Shared/BrineSpace-native-validation-20261017/tools');from run_release_benchmark import isolated_environment,require_storage
editor='/Users/alexyesilcimen/Desktop/Mac Test/Brinespace/qa-sdk/Godot.app/Contents/MacOS/Godot';roots={'A':pathlib.Path('/Users/Shared/BrineSpace-native-parent-20261017'),'B':pathlib.Path('/Users/Shared/BrineSpace-native-validation-20261017')};frozen=pathlib.Path('/Users/Shared/BrineSpace-iPad-compact-evidence/checkpoint-before-update.save');rows=[]
for i,label in enumerate('ABBAAB'):
 require_storage(base)
 out=base/'balanced'/f'{i+1}-{label}';out.mkdir(parents=True,exist_ok=True);env,profile=isolated_environment(base/'balanced'/('profile-'+label));env['BRINESPACE_TEST_USER_DIR']=str(profile);save=profile/'input.save';shutil.copy2(frozen,save)
 layout=pathlib.Path('/Users/alexyesilcimen/Library/Application Support/Godot/app_userdata/BrineSpace/room_layouts.json')
 if layout.exists():shutil.copy2(layout,profile/layout.name)
 result=out/'result.json';cmd=['/usr/bin/time','-l',editor,'--path',str(roots[label]),'-s','res://tools/release_benchmark.gd','--',f'--user-dir={profile}',f'--save={save}','--scenario=large','--width=1600','--height=900','--frames=180','--actions=idle,zoom,placement',f'--out={result}']
 with (out/'run.log').open('w') as log:
  try:r=subprocess.run(cmd,env=env,stdout=log,stderr=log,timeout=480);code=r.returncode
  except subprocess.TimeoutExpired:code=-1
 text=(out/'run.log').read_text(errors='replace');valid=code==0 and result.exists() and 'RELEASE BENCHMARK COMPLETE' in text and 'ERROR:' not in text;match=re.search(r'(\d+)\s+maximum resident set size',text)
 rows.append({'order':i+1,'build':label,'code':code,'valid':valid,'max_rss_bytes':int(match[1]) if match else None,'result':str(result),'scope':'native editor fixture; 40-room deterministic workload; fitted camera; 1x/2x/4x simulation speeds; same frozen checkpoint/layouts; first profile then learned order'});(base/'balanced-summary.json').write_text(json.dumps(rows,indent=2)+'\n');print(label,i+1,code,valid,flush=True)
 if not valid:print(text[-3000:],flush=True);break
