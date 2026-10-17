from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_material_v49.py').read_text()
s=s.replace("out=p/'master-material-v49'","out=p/'master-material-phase12-v51'").replace('bare-000.png','bare-012.png')
s=s.replace("r/'character/james-west-master-carry-v1/local-v3-carry-pose.png'","p/'master-material-v49/bare-head-protected.png'")
s=s.replace('carrying-case design/finish only','repaired material finish only').replace('walking-entry pose','distinct walking stride pose').replace('No body reproportioning','Do not copy Image3 walking-entry legs. No body reproportioning')
exec(compile(s,str(__file__),'exec'))
