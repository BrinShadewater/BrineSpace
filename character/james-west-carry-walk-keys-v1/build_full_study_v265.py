from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_full_gait_v242.py').read_text(encoding='utf-8').replace('full-gait-review-v242','full-gait-review-v265')
s=s.replace("return r/ledger['states'][i]['candidateSources'][mode]['file']", "\n    if i in [10,15]:return p/f'thigh-boundaries-v264/phase{i}/{mode}-head-protected.png'\n    study=next((row for row in ledger.get('thighConstructionStudies',[]) if row['phase']==i),None)\n    return r/(study['sources'][mode]['file'] if study else ledger['states'][i]['candidateSources'][mode]['file'])")
s=s.replace('Full49 staged source cycle, original timings, looping; normal selection unchanged.','Full49 mixed unselected garment studies and selected sources, original timings, looping; normal selection unchanged.')
(p/'prepare_full_gait_v265.py').write_text(s,encoding='utf-8')
for old,new in [('build_playback_v242.py','build_playback_v265.py'),('build_master_audit_v242.py','build_master_audit_v265.py')]:
 s=(p/old).read_text(encoding='utf-8').replace('full-gait-review-v242','full-gait-review-v265')
 if 'master_audit' in old:
  s=s.replace("def source(i,mode='bare'):return Image.open(r/j['states'][i]['candidateSources'][mode]['file']).convert('RGBA')", "def source(i,mode='bare'):\n manifest=json.loads((o/f'{mode}-manifest.json').read_bytes())\n return Image.open(r/manifest['states'][0]['frameFiles'][i].removeprefix('res://')).convert('RGBA')")
 if 'playback' in old:
  start=s.index('data={mode:');end=s.index(";data['master']",start)
  s=s[:start]+"data={mode:['data:image/png;base64,'+base64.b64encode((r/f.removeprefix('res://')).read_bytes()).decode() for f in json.loads((o/f'{mode}-manifest.json').read_bytes())['states'][0]['frameFiles']] for mode in ['bare','helmet']}"+s[end:]
 (p/new).write_text(s,encoding='utf-8')
