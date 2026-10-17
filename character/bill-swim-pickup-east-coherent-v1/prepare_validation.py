from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
s=(ROOT/'tests/test_bill_salvage_east_candidates.gd').read_text(encoding='utf-8')
s=s.replace('bill-salvage-east-coherent-v1/manifest.json','bill-swim-pickup-east-coherent-v1/manifest.json').replace('bill-salvage-helmet-east-coherent-v1/manifest.json','bill-swim-pickup-helmet-east-coherent-v1/manifest.json').replace('bill-salvage-east-candidate-native-v1','bill-pickup-east-candidate-native-v1')
start=s.index('\tfor gear in ["","diving-helmet"]:');end=s.index('\tvar actor=',start)
s=s[:start]+'''\tfor gear in ["","diving-helmet"]:
\t\tvar row: Array=player.frames["swim-pickup-east"] if gear.is_empty() else player.equipment_frames[gear]["swim-pickup-east"]
\t\tcheck(player.frame_at_elapsed("swim-pickup-east",0.0,gear)==row[0],"Pickup entry "+gear)
\t\tcheck(player.frame_at_elapsed("swim-pickup-east",.519,gear)==row[5],"Last pose before cargo award "+gear)
\t\tcheck(player.frame_at_elapsed("swim-pickup-east",.52,gear)==row[5],"Finite completion "+gear)
\t\tcheck(player.frame_at_elapsed("swim-pickup-east",1.0,gear)==row[5],"Finite terminal hold "+gear)
''' +s[end:]
s=s.replace('var key: String="salvage-east"','var key: String="swim-pickup-east"').replace('BILL SALVAGE CANDIDATE','BILL PICKUP CANDIDATE')
(ROOT/'tests/test_bill_pickup_east_candidates.gd').write_text(s,encoding='utf-8')
(ROOT/'tests/test_bill_pickup_east_candidates.gd.uid').write_text('uid://f8w3m6r2s9h4b\n',encoding='utf-8')
s=(ROOT/'tools/run_bill_salvage_east_candidate_validation.py').read_text(encoding='utf-8').replace('bill-salvage-east-candidate-native-v1','bill-pickup-east-candidate-native-v1').replace('test_bill_salvage_east_candidates.gd','test_bill_pickup_east_candidates.gd').replace('BILL SALVAGE','BILL PICKUP')
(ROOT/'tools/run_bill_pickup_east_candidate_validation.py').write_text(s,encoding='utf-8')
