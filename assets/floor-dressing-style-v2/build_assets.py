"""Extract reviewed floor decorations with true alpha; retain every source."""
from pathlib import Path
import importlib.util,json,hashlib
from PIL import Image
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('cleanup',ROOT/'tools/room_art_pipeline.py')
cleanup=importlib.util.module_from_spec(spec); spec.loader.exec_module(cleanup)
ITEMS=[
 ('engineering_access_plate',(78,80,285,289),32,'engineering','beside machinery service access'),
 ('linear_drain',(345,132,620,238),46,'wet_service','beside wet equipment or along a service edge'),
 ('inspection_hatch',(671,76,887,291),34,'engineering','clear maintenance access'),
 ('tread_service_mat',(955,104,1194,266),46,'engineering','operator stance beside a machine'),
 ('medical_bedside_mat',(58,387,298,573),44,'medical','beside a bed or examination station'),
 ('lab_access_panel',(373,374,593,584),34,'science','beneath a sealed lab service connection'),
 ('boot_scrub_tray',(655,402,902,565),36,'medical','decontamination preparation area'),
 ('specimen_alignment_ring',(951,365,1185,597),56,'science','around a work area without covering the floor'),
 ('cargo_corner_markings',(62,681,299,879),66,'cargo','around a cargo staging position'),
 ('pallet_alignment_plate',(370,677,583,884),38,'cargo','beneath a supported pallet'),
 ('threshold_tread_strip',(639,743,899,829),54,'operations','flush threshold detail clear of door leaves'),
 ('briefing_zone_mat',(943,694,1208,875),60,'command','beneath a briefing group'),
 ('woven_bedside_rug',(53,990,299,1149),54,'habitation','bedside or reading nook'),
 ('oval_braided_rug',(344,977,597,1158),56,'habitation','beneath a small seating group'),
 ('plant_drip_tray',(635,990,886,1155),48,'cultivation','beneath plant containers'),
 ('irrigation_drain_tiles',(925,1014,1215,1130),58,'cultivation','along growing equipment service edge')]
# Reviewed revised atlas regions: row spacing changed during generation.
xs=[0,313,626,939,1254]; ys=[0,330,650,950,1254]
ITEMS=[(key,(xs[i%4],ys[i//4],xs[i%4+1],ys[i//4+1]),width,department,placement) for i,(key,region,width,department,placement) in enumerate(ITEMS)]
GAPS={'specimen_alignment_ring':[(1068,500),(1001,432),(1136,430),(1136,565),(1000,565)]}
source_path=HERE/'source/atlas.png'; source=Image.open(source_path)
sprites={}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
for key,region,width,department,placement in ITEMS:
    seeds=[(x-region[0],y-region[1]) for x,y in GAPS.get(key,[])]
    donor=Image.open(HERE/'source/plant-drip-tray-v3.png') if key=='plant_drip_tray' else source.crop(region)
    clean=cleanup.clear_exterior(donor,seeds)
    bounds=clean.getchannel('A').getbbox(); assert bounds
    image=clean.crop(bounds); assert image.getchannel('A').getextrema()==(0,255)
    path=HERE/'sprites'/f'{key}.png'; image.save(path)
    sprites[key]={'path':path.relative_to(ROOT).as_posix(),'size':image.size,'pivot':[image.width/2,image.height/2],
      'units_per_pixel':width/image.width,'department':department,'placement':placement,
      'source_region':region if key!='plant_drip_tray' else None,'source_override':'assets/floor-dressing-style-v2/source/plant-drip-tray-v3.png' if key=='plant_drip_tray' else None,'alpha_trim':bounds,'gap_seeds_source':GAPS.get(key,[]),
      'layer':'floor_under_actors','collision':False,'sha256':sha(path)}
tray_path=HERE/'source/plant-drip-tray-v3.png'
tray=Image.open(tray_path)
manifest={'version':1,'source':{'path':source_path.relative_to(ROOT).as_posix(),'size':source.size,'mode':source.mode,'sha256':sha(source_path)},'correction_source':{'path':tray_path.relative_to(ROOT).as_posix(),'size':tray.size,'mode':tray.mode,'sha256':sha(tray_path)},'sprites':sprites}
(HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(f'Built {len(sprites)} RGBA floor decorations.')

