"""Rebuild current locker assets and reviews from saved sources; no generation."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
steps = [("build_pickup_revision.py", "--actor", actor) for actor in ("bill", "veld", "branforth")]
steps += [(script,) for script in (
    "build_deposit_revision.py",
    "build_locker_sequences.py",
    "check_locker_sequences.py",
    "build_locker_review.py",
    "build_review.py",
)]
for script, *args in steps:
    subprocess.run([sys.executable, str(ROOT / script), *args], cwd=ROOT, check=True)
print("Locker pipeline rebuilt from saved sources. Native tests and visual review remain separate.")
