import pathlib,sys,subprocess,json,os,time
root=pathlib.Path('/Users/Shared/BrineSpace-native-validation-20261017');out=pathlib.Path('/Users/Shared/BrineSpace-native-validation-evidence-20261017');sys.path.insert(0,str(root/'tools'))
from run_release_benchmark import isolated_environment
editor='/Users/alexyesilcimen/Desktop/Mac Test/Brinespace/qa-sdk/Godot.app/Contents/MacOS/Godot';results=[]
tests=[('test_crew_router_pixels',[]),('test_room_art_prefetch_pixels',[]),('test_tablet_controls',[]),('test_tablet_space',[]),('test_tablet_refinement',[]),('test_tablet_compact_storage',['--compact-case=hull']),('test_tablet_compact_storage',['--compact-case=effect']),('test_tablet_compact_storage',['--compact-case=construction'])]
for i,(test,args) in enumerate(tests):
 label=test+('-'+args[0].split('=')[1] if args else '');env,profile=isolated_environment(out/'native-profiles'/label);env['BRINESPACE_TEST_USER_DIR']=str(profile)
 cmd=[editor,'--path',str(root),'-s','res://tests/'+test+'.gd']+(['--']+args if args else [])
 start=time.monotonic()
 try:
  r=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=180);text=r.stdout+r.stderr;code=r.returncode
 except subprocess.TimeoutExpired as e:text=(e.stdout or b'').decode(errors='replace')+(e.stderr or b'').decode(errors='replace');code=-1
 (out/(label+'.log')).write_text(text);results.append({'test':label,'code':code,'seconds':time.monotonic()-start,'script_errors':'SCRIPT ERROR' in text,'profile':str(profile)});print(label,code,flush=True)
 (out/'native-tests.json').write_text(json.dumps(results,indent=2)+'\n')
