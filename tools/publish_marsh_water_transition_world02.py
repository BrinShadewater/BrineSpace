"""Publish source parity and actual q2 footage using ordered original manifests."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/publish_marsh_water_transition_world01.py').read_text()
s=s.replace("exec(compile(s,str(__file__),'exec'))", "s=s.replace('water-transition-world-01','water-transition-world-02').replace('transition-world-01-review','transition-world-02-review').replace('combined01-cross-review','combined02-cross-review').replace('q0 journey','q2 journey').replace('water-transition-world-02-2026-10-03','water-transition-world-02-2026-10-03-retry1')\nexec(compile(s,str(__file__),'exec'))")
exec(compile(s,str(__file__),'exec'))
