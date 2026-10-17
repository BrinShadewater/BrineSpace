from pathlib import Path
import json,hashlib,re
H=Path(__file__).resolve().parent;R=H.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
v=json.loads((H/'validation-checks.json').read_text());n=json.loads((H/'native-candidate-v1-checks.json').read_text());log=(H/'native-candidate-v1.log').read_text(encoding='utf-8');assert n['exit_code']==0 and n['engine_errors']==[] and n['real_profile_changed_files']==[] and '1491 checks, 0 failures' in log
for f,h in v['frameHashes'].items():assert sha(H/f)==h
for g,h in v['manifestHashes'].items():assert sha(H/f'{g}-manifest.json')==h
proof=dict(installed=False,checks=1491,states=24,references=192,scope='Actual candidate player direction change/all phases/pause/finite completion/exact cargo0 joins,8native pages; not world/controller or owner visual acceptance',hashes={p.relative_to(R).as_posix():sha(p) for p in [R/'tools/review_veld_swim_carry_turn_matrix_coherent_v1.gd',H/'bare-manifest.json',H/'helmet-manifest.json',H/'validation-checks.json',H/'provenance.json',H/'native-candidate-v1.log',H/'native-candidate-v1-checks.json']},frameHashes=v['frameHashes'])
(H/'native-evidence.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
O=R/'output/veld-cargo-controller-matrix-v1'
if (O/'validation.json').exists():
 c=json.loads((O/'validation.json').read_text());t=json.loads((O/'timeline.json').read_text());assert c['passed'] and c['realProfileChanges']==[] and len(t)==96
 nominal=[x for x in t if ' nominal ' in x['name']];assert len(nominal)==48 and all(x['turnSlots']==list(range(12)) for x in nominal)
 distinct={}
 for d in ['east','west','north','south']:
  for g in ['bare','helmet']:
   rows=[x for x in nominal if x['name'].startswith(d+' '+g+' nominal')];hs={x['exits'][0]['previousPixelHash'] for x in rows};assert len(hs)==6;assert all(x['exits'][1]['previousPixelHash']==x['exits'][1]['nextPixelHash'] for x in rows);distinct[d+' '+g]=6
 cl=(O/'native.log').read_text(encoding='utf-8');assert not re.search(r'^(SCRIPT ERROR|ERROR):',cl,re.M);count=int(re.search(r'VELD PHASE BOUNDARIES: (\d+) checks,0 failures',cl).group(1))
 paths=[R/'tools/review_veld_cargo_controller_matrix_v1.gd',R/'scripts/crew_expedition.gd',R/'scripts/crew_sprite_player.gd',R/'character/veld-salvage-pickup-family-coherent-v1/bare-manifest.json',R/'character/veld-salvage-pickup-family-coherent-v1/helmet-manifest.json',R/'character/veld-swim-carry-matrix-coherent-v1/bare-manifest.json',R/'character/veld-swim-carry-matrix-coherent-v1/helmet-manifest.json',H/'bare-manifest.json',H/'helmet-manifest.json',H/'validation-checks.json',O/'validation.json',O/'native.log',O/'timeline.json']
 (H/'controller-evidence.json').write_text(json.dumps(dict(installed=False,checks=count,routes=96,nominalCargoReturnCases=48,all12HalfPhasesPerNominalCase=True,distinctNominalWorkExits=distinct,exactNominalPickupCargoBoundaries=True,validation=c,hashes={p.relative_to(R).as_posix():sha(p) for p in paths},scope='Actual Veld controller/grid work-pickup-return with candidate actions/cargo/turns and inherited ordinary recall turns. Not full furnished/exterior/traffic journey or owner visual acceptance.'),indent=2)+'\n',encoding='utf-8');print(f'{count} actual controller checks,96cases,48cargo returns each exercising12half phases.')
print('1491 native player checks bound to24states/192frames and source package.')
