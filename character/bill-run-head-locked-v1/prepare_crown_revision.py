from pathlib import Path
import shutil
P=Path(__file__).resolve().parent;R=P.parents[1]
for folder in [P,R/'character/bill-walk-north-master-head-v1']:
 archive=folder/'review-before-crown-v2';assert not archive.exists(),'Revision already prepared';archive.mkdir()
 for f in folder.iterdir():
  if f==archive:continue
  if f.is_file():shutil.copy2(f,archive/f.name)
  elif f.name in ['frames','sources']:shutil.copytree(f,archive/f.name)
 (archive/'README.md').write_text('Frozen pre-crown-repair exports and recipes. Original res paths in archived reports identify the historical revision; use archived local PNGs for its pixels. Current root exports are the revised selection.\n')
f=P/'build.py';t=f.read_text();old=';a=ref.copy();a[~mask]=0;yy,xx=np.where(mask);box='
new=';mastertop=int(np.where((ref[:,:,3]>180)&(y>=65)&(y<105)&(x>=100)&(x<166))[0].min());mask|=(ref[:,:,3]>0)&(y>=mastertop-2)&(y<mastertop+14)&(x>=105)&(x<145);a=ref.copy();a[~mask]=0;yy,xx=np.where(mask);box='
assert old in t;f.write_text(t.replace(old,new).replace('Native accepted head pixels segmented by warm per-row silhouette','Native accepted head pixels segmented by warm per-row silhouette plus complete gray crown and soft edges'))
f=P/'verify.py';t=f.read_text();needle=" for f,row in zip(s['frameFiles'],d['frames']):"
insert=" top=int(np.where((master[:,:,3]>180)&(y>=65)&(y<105)&(x>=100)&(x<166))[0].min());crown=(master[:,:,3]>0)&(y>=top)&(y<top+14)&(x>=105)&(x<145);full=np.zeros_like(master);full[y0:y1,x0:x1]=head;check(np.array_equal(full[crown],master[crown]),'Complete master crown coverage including gray and soft edges')\n"
assert needle in t;f.write_text(t.replace(needle,insert+needle))
f=R/'character/bill-walk-north-master-head-v1/verify.py';t=f.read_text();needle='original=json.loads'
insert="top=int(np.where((master[:,:,3]>180)&(yy>=65)&(yy<105)&(xx>=100)&(xx<166))[0].min());crown=(master[:,:,3]>0)&(yy>=top)&(yy<top+14)&(xx>=105)&(xx<145);full=np.zeros_like(master);full[y0:y1,x0:x1]=head;check(np.array_equal(full[crown],master[crown]),'Complete native master crown and soft edges')\n"
assert needle in t;f.write_text(t.replace(needle,insert+needle,1))
print('Archived preceding run/north-walk evidence; current builders now preserve complete native crown')
