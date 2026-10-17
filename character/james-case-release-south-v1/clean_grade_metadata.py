from pathlib import Path
P=Path(__file__).resolve().parent
path=P/'build.py'
old=path.read_text()
new=old.replace("'neutralGain':ng,'goldGain':gg.tolist(),'skinGain':sg.tolist(),",'')
assert new!=old
path.write_text(new)
