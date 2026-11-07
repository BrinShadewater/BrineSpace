"""Keep actual East carry fixture; replace only complete far-contact source."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for original,target in [('review_marsh_east_carry02_actor.gd','review_marsh_east_carry03_actor.gd'),('publish_marsh_east_carry02_actor.py','publish_marsh_east_carry03_actor.py'),('fingerprint_marsh_east_carry02_actor.py','fingerprint_marsh_east_carry03_actor.py')]:
    s=(ROOT/'tools'/original).read_text().replace('carry02','carry03').replace('carry-actor-02','carry-actor-03').replace('candidate-02','candidate-03')
    if target.startswith('fingerprint'):
        s=s.replace("'near-06-unselected']","'near-06-unselected','contact-07-unselected']")
        s=s.replace("names+=['tools/'+n", "names+=['tools/prepare_marsh_east_carry03_native.py','tools/prepare_marsh_east_carry_contact07.py','tools/build_marsh_east_carry_contact07.py','tools/assemble_marsh_east_carry03.py','tools/assemble_marsh_east_carry02.py','tools/prepare_marsh_east_carry02_native.py']\nnames+=['tools/'+n")
        # The older prefix producer remains a real dependency, with its existing name.
        s=s.replace("'prepare_marsh_east_carry03_native.py','review", "'prepare_marsh_east_carry02_native.py','review")
    p=ROOT/'tools'/target;assert not p.exists();p.write_text(s)
    if target.endswith('.gd'):p.with_suffix('.gd.uid').write_text('uid://dc0ehcarry3v96\n')
print('Prepared unchanged East cargo movement fixture for complete corrected contact03 cycle.')
