from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
base=(R/'character/james-ward-lifecycle-v1/validate.gd').read_text(encoding='utf-8')
specs={'east':((22,20),(21,20),1),'south':((20,22),(20,21),0),'west':((18,20),(19,20),1)}
old='game._place_room("storage_bay",Vector2i(20,19),true);game._place_room("storage_bay",Vector2i(19,19),true)'
for face,(cell,room,rotation) in specs.items():
    s=base.replace('res://character/james-ward-lifecycle-v1/','res://character/james-ward-cardinal-v1/'+face+'/')
    s=s.replace('Vector2i(19,18)','Vector2i'+str(cell)).replace('Vector2i(19,19)','Vector2i'+str(room)).replace('Vector2(19.5,19.5)','Vector2'+str((room[0]+.5,room[1]+.5)))
    # Replace the transformed setup line; no physical actor/path/facing override.
    line='game._place_room("storage_bay",Vector2i(20,19),true);game._place_room("storage_bay",Vector2i'+str(room)+',true)'
    assert line in s
    setup='var ward:Dictionary=game.wrecks[Vector2i(19,18)].duplicate(true)\n\tgame.wrecks.erase(Vector2i(19,18));game.drone_fleet.sites.erase(Vector2i(19,18))\n\tgame.wrecks[Vector2i'+str(cell)+']=ward;ward.rotation='+str(rotation)+'\n\tgame._place_room("storage_bay",Vector2i'+str(room)+',true)'
    s=s.replace(line,setup).replace('north',face).replace('North',face.capitalize())
    s=s.replace('OUT+"validate.gd.uid"','"res://character/james-ward-cardinal-v1/'+face+'.gd.uid"')
    s=s.replace('JAMES WARD LIFECYCLE:','JAMES WARD '+face.upper()+':')
    s=s.replace('Not other facings, pause-work return/resume, power/door blockage, gear or all hazard proof.','Not pause-work return/resume, power/door blockage, gear or other ward kinds. Dedicated relocated cryo ward and actual single storage approach; no physical actor pose, facing, collision or route overrides.')
    (P/(face+'.gd')).write_text(s,encoding='utf-8');(P/face).mkdir(exist_ok=True)
files=['scripts/branforth_npc.gd','scripts/ward_repair.gd','scripts/james_hull_resume.gd','scripts/james_hull_return.gd','scripts/station_effects.gd','scripts/grid_canvas.gd','character/james-torch-material-residue-v2/bare-manifest.json']
(P/'runtime-input-before.json').write_text(json.dumps({f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in files},indent=2),encoding='utf-8')
print('Three directional fixtures and seven frozen input hashes saved')
