from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent.parent
source=(ROOT/'tests/test_bill_seated_south_family_selected.gd').read_text()
source=source.replace('bill-seated-south-selected-sofa-v1','bill-seated-north-selected-reading-chair-v1').replace('bill-seated-south-family-v1','bill-seated-north-family-v1').replace('"south"','"north"').replace('"observation_room"','"crew_lounge"').replace('=="read"','=="sit"').replace('npc.goal="curiosity"','npc.goal="fatigue"')
old='check(npc.stage=="observation_sit" and npc.direction=="north","Actual reading sit chooser")'
new='''check(npc.stage=="life_sit" and npc.direction=="north","Actual lounge sitting chooser")
\t\t# Reading is explicitly scripted at the real lounge seat. This tests selected
\t\t# pose clocks/renderer/restores, not an autonomous lounge-reading chooser.
\t\tnpc.stage="observation_sit";npc.timer=.65'''
assert old in source
source=source.replace(old,new).replace('Actual observation reading station','Actual lounge seated station').replace('Actual south sofa geometry','Actual north chair geometry').replace('Actual route arrives and starts reading service','Actual route arrives and starts seated service').replace('BILL SOFA','BILL NORTH READING CONTRACT')
(ROOT/'tests/test_bill_seated_north_reading_selected.gd').write_text(source)
(ROOT/'tests/test_bill_seated_north_reading_selected.gd.uid').write_text('uid://s6b8w3m6p2r9v\n')
runner=(ROOT/'tools/run_bill_seated_south_family_selected_validation.py').read_text().replace('bill-seated-south-selected-sofa-v1','bill-seated-north-selected-reading-chair-v1').replace('test_bill_seated_south_family_selected','test_bill_seated_north_reading_selected').replace('BILL SOFA','BILL NORTH READING CONTRACT')
(ROOT/'tools/run_bill_seated_north_reading_selected_validation.py').write_text(runner)
print('Prepared normal-loader north reading stage contract at actual lounge chair; scripted reading explicit')
