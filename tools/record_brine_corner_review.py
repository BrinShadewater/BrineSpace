"""Record the inspected corner asset and verify transparent notch/body probes."""
import json
import sys
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
folder=sys.argv[1] if len(sys.argv)>1 else 'assets/brine-corner-service-v1'
evidence=sys.argv[2] if len(sys.argv)>2 else 'output/brine-corner-service-2026-09-08'
path=ROOT/folder/'material-scale-review.json'
data=json.loads(path.read_text())
with Image.open(ROOT/data['export_path']) as image:
    alpha=image.getchannel('A')
    probes={'outside':((0,0),0),'inner_notch':((800,800),0),'ceramic_body':((200,600),255)}
    if 'analysis' in folder: probes={'outside':((0,0),0),'inner_notch':((500,800),0),'ceramic_body':((1000,700),255)}
    for name,(point,value) in probes.items(): assert alpha.getpixel(point)==value,(name,alpha.getpixel(point))
data.update(department='BRINE / Core',condition='Maintained; quiet matte ceramic and subdued glass',attachment_class='northwest corner fitted furniture',functional_bays=['Aquamarine circulation channel','Sealed filter cassettes','Recessed water-quality display','Cartridge storage and inspection surface'],runtime_behavior='Decorative service furniture; no new simulation behavior',camera_and_facing='Axial overhead NW corner; north arm faces south, west arm faces east',proposed_ground_footprint_world=[128,118.08029878618115],placement_exclusions=['North and west doors','Central chamber','Existing peripheral furniture'])
data['review']['materials']={'verdict':'pass','findings':['Native pearl ceramic and aquamarine match the BRINE chamber; modest peripheral detail.']}
data['review']['native_scale']={'verdict':'pass','evidence':'output/brine-corner-service-2026-09-08/room.png','findings':['128-unit wide L remains peripheral to the central chamber.']}
data['review']['alpha']={'verdict':'pass','findings':['Native registered export reviewed; exterior and inner notch transparent, ceramic body retained.'],'probes':{name:{'point':point,'alpha':value} for name,(point,value) in probes.items()}}
data['review']['integration']={'stage':'studio_library','evidence':'output/brine-corner-service-2026-09-08/review-final.log','findings':['BRINE Room Default tray entry and static NW prop/door clearance pass.','Preview only; existing personal layouts untouched. Conservative rectangular collision bound; no occupied route acceptance.']}
data['owner_acceptance']=None
registration=json.loads((ROOT/folder/'registration.json').read_text())
data['proposed_ground_footprint_world']=[128,128*registration['region'][3]/registration['region'][2]]
data['review']['native_scale']['evidence']=evidence+'/room.png'
data['review']['integration']['evidence']=evidence+'/review-final.log'
if folder.endswith('v2'):
    data['functional_bays']=['Circulation channel','Filter cassettes','North monitoring bank','West diagnostic consoles','Pump cartridges and fluid lines']
    data['review']['materials']['findings']=['Denser equipment and cyan monitors follow the owner reference; matte pearl ceramic remains consistent with BRINE.']
if 'analysis' in folder:
    data['attachment_class']='northeast corner fitted furniture'
    data['camera_and_facing']='Axial overhead NE corner; inward south and west controls'
    data['functional_bays']=['Sample cartridges','Sealed centrifuge','Diagnostic monitors','Membrane oxygenators','Coolant heat exchanger']
    data['review']['integration']['evidence']=evidence+'/review.log'
    data['review']['integration']['findings']=['Available in BRINE default tray. NE fixture replaces the existing dual workstation for clearance; authored room and personal layouts are unchanged.']
    data['review']['materials']['findings']=['Native pearl ceramic and aquamarine match BRINE and the NW companion; distinct equipment remains readable at 128 units.']
path.write_text(json.dumps(data,indent=2)+'\n')
print('BRINE corner: native review recorded; exterior/notch/body alpha verified')
