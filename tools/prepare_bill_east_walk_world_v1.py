"""Reuse the furnished-room source submission fixture for the complete walking bank."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
src=(R/'tools/review_bill_east_master_world_v5.gd').read_text(encoding='utf-8')
src=src.replace('bill-east-master-world-v5','bill-east-walk-world-v1').replace('interact','walk').replace('bill-east-reach-adjacent-motion-v2','bill-east-walk-master-full-v1')
start=src.index(' check(same(player.frames["walk-east"][0]')
end=src.index(' var camera_foot=actor.foot',start)
src=src[:start]+' check(player.frames["walk-east"].size()==48,"complete48 walking phases loaded")\n'+src[end:]
src=src.replace('or state=="walk":','or (state=="walk" and slot in [0,6,12,18,24,30,36,47]):')
src=src.replace('No natural chooser/activity dispatch, walking/gear, continuous cadence/fullsave/titleContinue or normal admission.','Complete48 walking sources explicitly bound; no natural locomotion/path dispatch, gear, continuous cadence/fullsave/titleContinue or normal admission.')
path=R/'tools/review_bill_east_walk_world_v1.gd';assert not path.exists();path.write_text(src,encoding='utf-8')
uid=(R/'tools/ensure_bill_east_master_world_v5_uids.gd').read_text(encoding='utf-8').replace('review_bill_east_master_world_v5','review_bill_east_walk_world_v1').replace('ensure_bill_east_master_world_v5_uids','ensure_bill_east_walk_world_v1_uids')
(R/'tools/ensure_bill_east_walk_world_v1_uids.gd').write_text(uid,encoding='utf-8')
run=(R/'tools/run_bill_east_master_world_v5.py').read_text(encoding='utf-8').replace('bill-east-master-world-v5','bill-east-walk-world-v1').replace('review_bill_east_master_world_v5','review_bill_east_walk_world_v1').replace('ensure_bill_east_master_world_v5_uids','ensure_bill_east_walk_world_v1_uids').replace('run_bill_east_master_world_v5','run_bill_east_walk_world_v1')
run=run.replace("OUT=ROOT/('output/bill-east-master-world-'+version)","OUT=ROOT/'output/bill-east-walk-world-v1'").replace("==36","==40")
run=run.replace("ROOT/'character/bill-east-reach-adjacent-motion-v2'","ROOT/'character/bill-east-reach-adjacent-motion-v2',ROOT/'character/bill-east-walk-master-full-v1'")
(R/'tools/run_bill_east_walk_world_v1.py').write_text(run,encoding='utf-8')
print('Prepared complete walking native fixture and isolated runner.')
