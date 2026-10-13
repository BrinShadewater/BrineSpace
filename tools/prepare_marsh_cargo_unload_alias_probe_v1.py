"""Derive a bounded alias review from the maintained normal-player probe."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/review_marsh_cargo_normal_player_v1.gd').read_text()
for old,new in [('cargo-matched-v1','cargo-unload-matched-v1'),('cargo-normal-player-v1-2026-10-03','cargo-unload-alias-player-v1-2026-10-03'),('states==48 and slots==272 and restores==272','states==4 and slots==16 and restores==16'),('all48cargo states/272exact sources','all4retained cargo-unload aliases/16exact sources'),('272player restore','16player restore'),('MARSH NORMAL CARGO PLAYER','MARSH CARGO UNLOAD ALIAS PLAYER')]:
    assert old in s;s=s.replace(old,new)
(ROOT/'tools/review_marsh_cargo_unload_alias_v1.gd').write_text(s)
(ROOT/'tools/review_marsh_cargo_unload_alias_v1.gd.uid').write_text('uid://dm4cargoalias7p2\n')
s=(ROOT/'tools/fingerprint_marsh_cargo_normal_v1.py').read_text()
s=s.replace('cargo-matched-v1','cargo-unload-matched-v1')
s=s.replace('for name in [',"for name in ['install_marsh_cargo_unload_alias_v1.py','review_marsh_cargo_unload_alias_v1.gd','review_marsh_cargo_unload_alias_v1.gd.uid','fingerprint_marsh_cargo_unload_alias_v1.py',")
s=s.replace("for m in receipt['manifests']:paths.add(ROOT/m['sourceManifest'])","for a in receipt['aliases']:paths.add(ROOT/a['oldManifest']);paths.add(ROOT/a['newManifest'])")
s=s.replace("for f in receipt['wholeFrameCopies']:paths.add(ROOT/f['source'])","for a in receipt['aliases']:\n for f in a['selectedSources']:paths.add(ROOT/f['path'].removeprefix('res://'))")
(ROOT/'tools/fingerprint_marsh_cargo_unload_alias_v1.py').write_text(s)
print('4state/16slot native alias probe and bounded fingerprint prepared')
