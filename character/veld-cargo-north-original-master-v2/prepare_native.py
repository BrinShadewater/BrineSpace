from pathlib import Path
R=Path(__file__).resolve().parents[2];P=Path(__file__).resolve().parent
s=(R/'tests/test_veld_idle_north_original_master_v1.gd').read_text().replace('veld-idle-north-original-master-v1','veld-cargo-north-original-master-v2').replace('veld-north-idle-scratch','veld-north-cargo-original-scratch').replace('VELD ORIGINAL NORTH MASTER IDLE','VELD ORIGINAL NORTH CARGO')
s=s.replace('[["unload-north",.52,"idle-north",0.0],["pickup-north",0.0,"idle-north",0.0],["pickup-north",.52,"carry-start-north",0.0],["carry-start-north",.32,"carry-north",0.0],["carry-stop-north",.32,"pickup-north",.52]]','[["unload-north",.52,"idle-north",0.0],["pickup-north",0.0,"idle-north",0.0]]')
(R/'tests/test_veld_cargo_north_original_master_v2.gd').write_text(s)
(R/'tests/test_veld_cargo_north_original_master_v2.gd.uid').write_text('uid://cvldcargonorthorig2\n')
s=(R/'tools/run_veld_idle_north_original_master_v1.py').read_text().replace('veld-idle-north-original-master-v1','veld-cargo-north-original-master-v2').replace('test_veld_idle_north_original_master_v1.gd','test_veld_cargo_north_original_master_v2.gd').replace('veld-north-idle-scratch','veld-north-cargo-original-scratch')
start=s.index('paths.update([P/');end=s.index('\ndef inputs():',start)
s=s[:start]+"paths.update(P.glob('raw-*.png'));paths.update(P.glob('prompt-*.txt'));paths.add(P/'register_source.py')"+s[end:]
s=s.replace('six North states/both gears','three North states/both gears').replace('exact idle/cargo/action source joins','exact standing idle/cargo source joins; older gait/start/turn held endpoint differs and is not accepted')
(R/'tools/run_veld_cargo_north_original_master_v2.py').write_text(s)
