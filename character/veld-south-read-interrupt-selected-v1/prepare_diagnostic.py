"""Reuse the isolated runner without changing the live reader suite."""
from pathlib import Path
R=Path(__file__).resolve().parents[2]
s=(R/'tools/run_veld_south_read_interrupt_selected.py').read_text(encoding='utf-8')
s=s.replace('veld-south-read-interrupt-selected-v1','veld-south-sofa-fall-diagnostic-v1')
s=s.replace('test_veld_south_read_interrupt_selected.gd','test_veld_south_sofa_fall_diagnostic.gd')
s=s.replace("'scripts/run_save.gd',", "'scripts/run_save.gd','scripts/veld_death_motion.gd',")
s=s.replace("'0 failures; 56 interruptions'", "'0 failures; two prescribed actor mortality contexts'")
s=s.replace('VELD SOUTH READ INTERRUPT SELECTED','VELD SOUTH SOFA FALL DIAGNOSTIC')
s=s.replace("photo=OUT/'final.png'","photo=OUT/'helmet-1.4-room.png'")
s=s.replace('frozen_paths=sorted(set(frozen_paths))', '''for gear in ['bare','helmet']:
        manifest=ROOT/f'character/veld-death-ground-south-coherent-v1/{gear}-manifest.json'
        frozen_paths.append(manifest)
        for state in json.loads(manifest.read_text(encoding='utf-8'))['states']:
            frozen_paths.extend(manifest.parent/f for f in state['frameFiles'])
    frozen_paths=sorted(set(frozen_paths))''')
(R/'tools/run_veld_south_sofa_fall_diagnostic.py').write_text(s,encoding='utf-8')
print('Separate isolated mortality diagnostic runner ready')
