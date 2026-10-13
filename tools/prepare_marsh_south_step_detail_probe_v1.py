"""Prepare actual normal-catalogue seven-pose playback and bounded inputs."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/review_marsh_cargo_normal_player_v1.gd').read_text()
for old,new in [('cargo-matched-v1','south-step-detail-v1'),('cargo-normal-player-v1-2026-10-03','south-step-detail-player-v1-2026-10-03'),('states==48 and slots==272 and restores==272','states==1 and slots==7 and restores==7'),('all48cargo states/272exact sources','complete South short-step state/7exact sources'),('272player restore','7player restore'),('MARSH NORMAL CARGO PLAYER','MARSH SOUTH STEP DETAIL PLAYER'),('if i in [0,int(entry.frameFiles.size()/2),entry.frameFiles.size()-1]:','if true:'),('First/middle/last native source/station comparison captures.','All seven native source/station comparison captures.')]:
    assert old in s;s=s.replace(old,new)
(ROOT/'tools/review_marsh_south_step_detail_v1.gd').write_text(s)
(ROOT/'tools/review_marsh_south_step_detail_v1.gd.uid').write_text('uid://ds3stepdetail8v2\n')
s=(ROOT/'tools/fingerprint_marsh_cargo_normal_v1.py').read_text().replace('cargo-matched-v1','south-step-detail-v1')
s=s.replace('for name in [',"for name in ['install_marsh_south_step_detail_v1.py','review_marsh_south_step_detail_v1.gd','review_marsh_south_step_detail_v1.gd.uid','fingerprint_marsh_south_step_detail_v1.py',")
s=s.replace("for m in receipt['manifests']:paths.add(ROOT/m['sourceManifest'])","paths.add(ROOT/receipt['oldManifest']);paths.add(ROOT/receipt['wholeSource'])")
s=s.replace("for f in receipt['wholeFrameCopies']:paths.add(ROOT/f['source'])","for f in receipt['originalSources']:paths.add(ROOT/f['path'])")
(ROOT/'tools/fingerprint_marsh_south_step_detail_v1.py').write_text(s)
print('Normal seven-pose player proof and scratch interval fingerprint prepared')
