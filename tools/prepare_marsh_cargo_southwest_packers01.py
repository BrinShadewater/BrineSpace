"""Adapt whole packers with explicit facing-specific boot registration."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
base=(ROOT/'tools/pack_marsh_cargo_east_unload01.py').read_text()
for f in ['south','west']:
    s=base.replace('East',f.title()).replace('east',f)
    if f=='south':
        s=s.replace('stop=b[0]+round((b[2]-b[0])*.45)','stop=b[2]')
        s=s.replace('Body boots occupy left 45% of the action silhouette; exclude floor case.','Front-facing body boots span both sides; floor band uses whole span.')
        s=s.replace('left boot floor-band midpoint','both front boots floor-band midpoint')
    else:
        s=s.replace('sy,sx=np.nonzero(aa[b[3]-5:b[3],b[0]:stop]>=128)','begin=b[2]-round((b[2]-b[0])*.45)\n        sy,sx=np.nonzero(aa[b[3]-5:b[3],begin:b[2]]>=128)')
        s=s.replace('anchor=b[0]+(sx.min()+sx.max())/2','anchor=begin+(sx.min()+sx.max())/2')
        s=s.replace('Body boots occupy left 45% of the action silhouette; exclude floor case.','West body boots occupy right45% of silhouette; exclude floor case on left.')
        s=s.replace('left boot floor-band midpoint','right boot floor-band midpoint')
    (ROOT/f'tools/pack_marsh_cargo_{f}_unload01.py').write_text(s)
print('South/West whole packers prepared; no mirror or individual pose fit')
