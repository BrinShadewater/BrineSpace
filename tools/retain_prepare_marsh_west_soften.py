"""Retain complete corrected source and independent occupied-neutral builder."""
from pathlib import Path
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-west-collapse-material-v1/sources'
original=Path('C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96/exec-a3037173-b441-459b-9573-68599dd0b735.png')
target=BASE/'soften-02.raw.png';shutil.copy2(original,target)
request_path=BASE/'soften-02.request.json';request=json.loads(request_path.read_text())
request.update(status='generated whole West mild-dip source; unselected, packaging/review pending',generationId='exec-a3037173-b441-459b-9573-68599dd0b735',originalGeneratedPath=str(original),rawSha256=hashlib.sha256(target.read_bytes()).hexdigest())
request_path.write_text(json.dumps(request,indent=2)+'\n')
builder=ROOT/'tools/build_marsh_west_collapse_soften.py';assert not builder.exists()
text=(ROOT/'tools/build_marsh_north_collapse_soften.py').read_text().replace('north','west').replace('North','West')
text=text.replace('146/','147/').replace('neutral146occupied','neutral147occupied').replace("'neutralOccupiedTargetHeight':146","'neutralOccupiedTargetHeight':147")
text=text.replace('complete milder early dip','complete intermediate first dip')
text=text.replace('Source01 first dip125height superseded by measured new whole articulation; desired135 not forced. Exposed dark soles retained.','Source01 first dip145height superseded by measured134row whole articulation; desired140 not forced. Warm ivory boot uppers and charcoal soles retained.')
builder.write_text(text)
print('Retained corrected West raw/request execution/SHA; prepared independent soften builder.')
