from pathlib import Path
import importlib.util
P=Path(__file__).resolve().parent
s=(P/'run_bill_pickup_east_candidate_validation.py').read_text(encoding='utf-8').replace('bill-pickup-east-candidate-native-v1','bill-pickup-live-boundary-v1').replace('test_bill_pickup_east_candidates.gd','test_bill_pickup_live_boundary.gd').replace('BILL PICKUP','BILL LIVE')
s=s.replace("photo=OUT/'loaded-water-carry.png'","photo=OUT/'timeline.json'")
exec(compile(s,__file__,'exec'))
