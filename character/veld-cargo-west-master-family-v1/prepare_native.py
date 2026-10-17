from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'tests/test_veld_carry_west_master_proportions.gd').read_text(encoding='utf-8')
s=s.replace('const P := "res://character/veld-carry-west-master-proportions-v1/"','''const CANDIDATE_BARE := "res://character/veld-cargo-west-master-family-v1/bare-manifest.json"
const CANDIDATE_HELMET := "res://character/veld-cargo-west-master-family-v1/helmet-manifest.json"
const BASELINE_BARE := {"unload":"res://character/veld-unload-west-consistent-v1/bare-manifest.json","pickup":"res://character/veld-pickup-west-consistent-v1/bare-manifest.json"}
const BASELINE_HELMET := {"unload":"res://character/veld-unload-west-consistent-v1/helmet-manifest.json","pickup":"res://character/veld-pickup-west-consistent-v1/helmet-manifest.json"}''')
s=s.replace('output/veld-carry-west-master-proportions-v1/','output/veld-cargo-west-master-family-v1/')
s=s.replace('veld-carry-west-master-scratch','veld-cargo-west-master-scratch')
s=s.replace('for gear in ["bare","helmet"]:','for case in [{"gear":"bare","action":"unload"},{"gear":"bare","action":"pickup"},{"gear":"helmet","action":"unload"},{"gear":"helmet","action":"pickup"}]:\n\t\tvar gear: String=case.gear\n\t\tvar action: String=case.action')
s=s.replace('baseline.load_manifest("res://character/veld-carry-west-consistent-v1/bare-manifest.json")','baseline.load_manifest(BASELINE_BARE[action])')
s=s.replace('baseline.load_equipment_manifest("diving-helmet","res://character/veld-carry-west-consistent-v1/helmet-manifest.json")','baseline.load_equipment_manifest("diving-helmet",BASELINE_HELMET[action])')
s=s.replace('player.load_manifest("res://character/veld-carry-west-master-proportions-v1/bare-manifest.json")','player.load_manifest(CANDIDATE_BARE)')
s=s.replace('player.load_equipment_manifest("diving-helmet","res://character/veld-carry-west-master-proportions-v1/helmet-manifest.json")','player.load_equipment_manifest("diving-helmet",CANDIDATE_HELMET)')
s=s.replace('P+gear+"-manifest.json"','CANDIDATE_BARE if gear=="bare" else CANDIDATE_HELMET')
s=s.replace('var seen := {}','var state: Dictionary={}\n\t\tfor entry in pack.states:\n\t\t\tif entry.id==action+"-west":state=entry\n\t\tcheck(not state.is_empty() and not state.loop,"Finite action source")\n\t\tvar seen := {}')
s=s.replace('player.cycle_seconds("carry-west",equipment),.84','player.cycle_seconds(action+"-west",equipment),.52').replace('Exact840mscycle','Exact520msfinite action')
s=s.replace('range(52)','range(18)')
s=s.replace('var position := Vector2(-time*.07351351351351351/.84,0)','var position := Vector2.ZERO')
s=s.replace('frame("carry","west"','frame(action,"west"')
s=s.replace('var index: int=int(floor(fposmod(time,.84)/.14+0.000001))%6','''var index: int=5
			var remaining: float=time
			for slot in range(6):
				var duration: float=float(state.frameDurationsMs[slot])/1000.0
				if remaining<duration: index=slot;break
				remaining-=duration''')
s=s.replace('P+str(pack.states[0].frameFiles[index])','str(state.frameFiles[index])')
s=s.replace('Distance-driven source slot','Finite action source slot')
s=s.replace('texture.get_meta("crew_water_kind")=="carry" and not texture.get_meta("crew_water_pose")','texture.get_meta("crew_water_kind")==str(state.waterKinds[index]) and not texture.get_meta("crew_water_pose")')
s=s.replace('Dry carrying source','Original dry action source metadata')
s=s.replace('board.time=time','board.time=0.0')
s=s.replace('gear+"-%03d"%n','gear+"-"+action+"-%03d"%n')
s=s.replace('"gear":gear,"time":time','"gear":gear,"action":action,"time":time')
s=s.replace('All six phases and loop wraps observed','All six finite poses observed')
s=s.replace('VELD WEST MASTER MOTION','VELD WEST MASTER ACTIONS').replace('104native presentations','72native presentations')
assert 'P+' not in s and 'frame("carry"' not in s
(R/'tests/test_veld_cargo_west_master_family.gd').write_text(s,encoding='utf-8')
(R/'tests/test_veld_cargo_west_master_family.gd.uid').write_text('uid://d0evcwmfa1\n',encoding='utf-8')
w=(R/'tools/run_veld_carry_west_master_proportions.py').read_text(encoding='utf-8')
w=w.replace('output/veld-carry-west-master-proportions-v1','output/veld-cargo-west-master-family-v1').replace('test_veld_carry_west_master_proportions.gd','test_veld_cargo_west_master_family.gd').replace('veld-carry-west-master-scratch','veld-cargo-west-master-scratch')
w=w.replace("['veld-carry-west-master-proportions-v1','veld-carry-west-consistent-v1']","['veld-cargo-west-master-family-v1','veld-unload-west-consistent-v1','veld-pickup-west-consistent-v1']")
w=w.replace('paths.extend(p.parent/x for x in s[\'frameFiles\'])',"paths.extend(R/x[6:] if x.startswith('res://') else p.parent/x for x in s['frameFiles'])")
w=w.replace('helmet-051-native.png','helmet-pickup-017-native.png').replace(',0 failures;104native presentations',',0 failures;72native presentations')
w=w.replace('candidate standalone actual crew-player distance-clock/native rendering; no normal selection/controller/world/furniture/save acceptance','candidate standalone actual crew-player finite-clock/native rendering, unload/pickup/both gears; no normal selection/controller/world/prop ownership/save acceptance')
(R/'tools/run_veld_cargo_west_master_family.py').write_text(w,encoding='utf-8')
print('Paired UID finite-action fixture/isolated runner prepared;72native samples')
