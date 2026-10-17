"""Same scratch/profile guard as the shared runner; budget for eight fresh scenes."""
from pathlib import Path
R=Path(__file__).resolve().parents[2]
source=(R/'character/james-death-family-v1/run_validation.py').read_text(encoding='utf-8')
assert source.count('proc.wait(timeout=240)')==1
source=source.replace('proc.wait(timeout=240)','proc.wait(timeout=600)')
exec(compile(source,'shared-native-runner-with-eight-scene-budget','exec'))
