"""Install reviewed surface polishes while preserving registered placement frames."""
import argparse,hashlib,json,shutil
from pathlib import Path
from PIL import Image
from shapely.geometry import Polygon
from shapely.ops import unary_union
from register_full_wall_props import ROOT,register
from register_alpha_silhouette import polygons,open_holes
FOLDER=ROOT/'assets/room-style-polish-v1'
REG=ROOT/'rooms/full-wall-v1/registrations'
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--install',action='store_true')
    args=parser.parse_args()
    backup=FOLDER/'previous-registrations';backup.mkdir(exist_ok=True)
    candidate=FOLDER/'registrations';candidate.mkdir(exist_ok=True)
    records=[]
    for row in json.loads((FOLDER/'generation.json').read_text()):
        name='side-'+row['id']+'-south.json'
        if not (backup/name).exists(): shutil.copy2(REG/name,backup/name)
        old=json.loads((backup/name).read_text())
        source=FOLDER/(row['id']+'.png')
        fresh=register(source)
        old_source=ROOT/old['source'].removeprefix('res://')
        old_size=Image.open(old_source).size;new_size=Image.open(source).size
        factor=new_size[0]/old_size[0]
        expected=[v*factor for v in old['region']]
        drift=max(abs(a-b)/max(expected[2],1) for a,b in zip(fresh['region'],expected))
        assert drift<0.03,(row['id'],'Artwork moved outside preserved frame',drift)
        geometry=unary_union([Polygon(p) for p in fresh['pieces']]).buffer(-0.8,join_style=2)
        data=old.copy();data.update(source=fresh['source'],sha256=fresh['sha256'],region=expected)
        data['pieces']=[[[round(x,3),round(y,3)] for x,y in list(p.exterior.coords)[:-1]] for poly in polygons(geometry) for p in open_holes(poly)]
        data['method']='Read-only neutral vector registration of imagegen material polish; 0.8 source-pixel edge inset; prior proportional placement frame retained'
        data['source_geometry']={'canvas':list(new_size),'detected_region':fresh['region'],'relative_frame_drift':drift}
        data['owner_revision']='room-style-polish-v1'
        (candidate/name).write_text(json.dumps(data,separators=(',',':'))+'\n')
        if args.install: shutil.copy2(candidate/name,REG/name)
        record={'id':row['id'],'department':row['department'],'source':data['source'],'sha256':data['sha256'],'previous_source':old['source'],'registration':str((REG/name).relative_to(ROOT)).replace('\\','/'),'canvas':list(new_size),'frame_drift':drift,'status':'integrated; native review pending' if args.install else 'registered; native review pending'}
        records.append(record)
    (FOLDER/'manifest.json').write_text(json.dumps(records,indent=2)+'\n')
    print(f'{len(records)} polished sources registered'+(' and installed' if args.install else '')+f'; max normalized frame drift {max(r["frame_drift"] for r in records):.4f}')
if __name__=='__main__': main()
