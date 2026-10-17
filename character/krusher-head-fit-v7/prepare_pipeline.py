"""Stage the established deterministic builders without changing prior revisions."""
raise SystemExit('Historical one-time bootstrap. Use rebuild_all.py with the maintained staged builders.')
from pathlib import Path
import json,re,shutil

H=Path(__file__).resolve().parent
R=H.parents[1]
OLD=H.with_name('krusher-head-fit-v4')
mapping={
 'krusher-james-canonical-v7':'krusher-james-canonical-v9',
 **{f'krusher-{name}-v4':f'krusher-{name}-v5' for name in ['inspection-family','repair-family','torch-family','seated-family','cargo-family','cargo-settle-profile','meal-family','meal-service','helmet-transition','water-family','water-cargo-turns']},
 'krusher-rest-family-v5':'krusher-rest-family-v6',
 'krusher-recovery-salvage-v3':'krusher-recovery-salvage-v4',
 'krusher-death-family-v3':'krusher-death-family-v4',
 'krusher-water-interruptions-v3':'krusher-water-interruptions-v4',
}
def output(match):
 text=match.group(0)
 for old,new in mapping.items():text=text.replace(old,new)
 return text
names=['build_actions','build_inspection','build_cargo','build_meals','build_equipment','build_rest','build_recovery','build_death','build_water','build_package','validate_actions','validate_cargo','validate_meals','validate_equipment','validate_rest','validate_recovery_death','validate_water','validate_package']
for name in names:
 text=(OLD/(name+'.py')).read_text()
 text=text.replace('krusher-james-canonical-v7','krusher-james-canonical-v9')
 text=text.replace('res://character/krusher-head-fit-v4/sources/','res://character/krusher-head-fit-v7/sources/')
 text=re.sub(r"(?:P|profile|O)=R/(?:f)?'[^']+'",output,text)
 text=text.replace("P=R/f'character/krusher-{family}-family-v4'","P=R/f'character/krusher-{family}-family-v5'")
 if name=='build_water':
  text=text.replace("('water-family',1,3,4,","('water-family',1,3,5,").replace("('water-cargo-turns',2,3,4,","('water-cargo-turns',2,3,5,").replace("('water-interruptions',1,2,3,","('water-interruptions',1,2,4,")
  text=text.replace("('krusher-recovery-salvage-v1','krusher-recovery-salvage-v3')","('krusher-recovery-salvage-v1','krusher-recovery-salvage-v4')")
 if name=='validate_water':text=text.replace("newVersion=3 if family=='water-interruptions' else 4","newVersion=4 if family=='water-interruptions' else 5")
 if name=='validate_recovery_death':text=text.replace("P=R/f'character/krusher-{family}-v3'","P=R/f'character/krusher-{family}-v4'")
 if name=='validate_meals':text=text.replace("P=R/('character/krusher-'+family+'-v4')","P=R/('character/krusher-'+family+'-v5')")
 if name=='validate_cargo':text=text.replace("krusher-cargo-settle-profile-v4","krusher-cargo-settle-profile-v5")
 if name=='validate_package':text=text.replace("krusher-animation-package-v4","krusher-animation-package-v5")
 if name=='build_package':text=text.replace('krusher-animation-package-v4','krusher-animation-package-v5').replace('krusher-head-fit-v4/build_package.py','krusher-head-fit-v7/build_package.py')
 (H/(name+'.py')).write_text(text)
for kind in ['action','quarter','rest','rear']:
 text=(OLD/('extract_'+kind+'_sources.py')).read_text()
 # Keep each cell's primary opaque component; this excludes external matte halo.
 if kind in ['action','quarter']:
  text=text.replace('import numpy as np,json,hashlib','import numpy as np,json,hashlib\nfrom scipy.ndimage import label')
  text=text.replace("arr[:,:,3]=np.where(arr[:,:,3]>240,255,0).astype('uint8')", "opaque=arr[:,:,3]>240;labs,_=label(opaque,np.ones((3,3)));sizes=np.bincount(labs.ravel());sizes[0]=0;opaque=labs==int(sizes.argmax());arr[:,:,3]=np.where(opaque,255,0).astype('uint8')")
 (H/('extract_'+kind+'_sources.py')).write_text(text)
index=json.loads((OLD/'candidate-bank-index.json').read_text())
for gear,paths in index['candidatePacks'].items():
 for i,path in enumerate(paths):
  for old,new in mapping.items():path=path.replace(old,new)
  paths[i]=path
(H/'candidate-bank-index.json').write_text(json.dumps(index,indent=2)+'\n')
(H/'revision-map.json').write_text(json.dumps(mapping,indent=2)+'\n')
print(json.dumps({'stagedScripts':len(names)+4,'candidateManifests':sum(map(len,index['candidatePacks'].values()))}))
