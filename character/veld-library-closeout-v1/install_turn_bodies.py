from pathlib import Path
import hashlib,json,time,os
P=Path(__file__).resolve().parent; R=P.parents[1]; D=P/'turn-body-fix'
assert json.loads((D/'BUILD_REVIEW.json').read_bytes())['failures']==0
rows=[]
for path in [R/'scripts/grid_canvas.gd',R/'character/ACTIVE_ASSETS.json']:
 original=path.read_bytes(); data=original
 for family in ['quarter','half']:
  old=f'character/veld-unified-turn-helmet-v1/{family}-helmet-manifest.json'.encode()
  new=f'character/veld-library-closeout-v1/turn-body-fix/{family}-helmet-manifest.json'.encode()
  count=data.count(old); assert count>0 or new in data,(path,family)
  data=data.replace(old,new); rows.append(dict(file=path.relative_to(R).as_posix(),family=family,replacements=count))
 assert path.read_bytes()==original
 if data!=original:
  temp=path.with_name(path.name+'.veld-temp');temp.write_bytes(data)
  for attempt in range(20):
   try:
    assert path.read_bytes()==original
    os.replace(temp,path);break
   except OSError:
    if attempt==19:raise
    time.sleep(0.2)
(D/'INSTALLATION.json').write_text(json.dumps(dict(changes=rows,scope='Only quarter/half helmet turn selection; bare poses, helmet art and timing preserved.'),indent=2)+'\n')
print(json.dumps(rows))
