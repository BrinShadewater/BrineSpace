from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1');f=p/'prepare_local_material_stride.py';s=f.read_text();old=".replace('local-material-phase4-v90',f'local-material-phase{phase}-v{version}').replace('bare-004.png',f'bare-{phase:03d}.png').replace('phase4',f'phase{phase}')";new=".replace('phase4',f'phase{phase}').replace(f'local-material-phase{phase}-v90',f'local-material-phase{phase}-v{version}').replace('bare-004.png',f'bare-{phase:03d}.png')";assert old in s;f.write_text(s.replace(old,new))
for phase in range(40,45):
    folder=(p/f'local-material-phase{phase}{phase-40}-v{phase+114}').resolve();assert folder.parent==p.resolve()
    allowed={'edit-target.png','master-textile-reference.png','inputs.json','prompt.txt'};assert {q.name for q in folder.iterdir()}==allowed
    for q in folder.iterdir():q.unlink()
    folder.rmdir()
print('Corrected preparer substitution order and removed five unused preparation folders.')
