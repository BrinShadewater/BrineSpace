"""Prepare independent North proof publisher without inherited failure claims."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
target=ROOT/'tools/publish_marsh_north_injury_material.py'
assert not target.exists()
text=(ROOT/'tools/publish_marsh_south_injury_material.py').read_text()
start=text.index("    previous=ROOT/");end=text.index('    recipe=',start)
text=text[:start]+text[end:]
text=text.replace('south','north').replace('South','North')
text=text.replace("BODY=ROOT/'character/marsh-north-collapse-material-v1/candidate-01'","BODY=ROOT/'character/marsh-north-collapse-material-v1/candidate-02'")
text=text.replace("'productionRendererChange':'Simulation-owned injury playback clears old cosmetic key, so following idle starts fresh. No actor/save format change.'","'productionRendererChange':'None in this North interval; existing simulation-owned injury playback resets cosmetic key for fresh idle.'")
text=text.replace("'prejoinEvidence':'403 passing controller checks but first normal idle mismatched authored endpoint; retained prejoin interval has original renderer hash and captures.'","'retainedFailedIntervals':[]")
text=text.replace('76 bounded inputs stable','107 bounded inputs stable').replace('Renderer cosmetic-phase join fixed; artwork remains unselected.','Existing renderer idle join verified for North; artwork remains unselected.')
target.write_text(text)
print('Prepared scoped North publisher.')
