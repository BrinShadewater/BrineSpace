"""Resolve a historical source through the selected material grading layer.

Original provenance hashes still test the original sources. Pixel/installation
expectations follow the current selection, while full-polish tests independently
verify that grading cannot change alpha, geometry or protected pixels.
"""
from pathlib import Path
import hashlib,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'character/marsh-full-polish-v1/colour-lock.json'
RECORDS=json.loads(PATH.read_text()) if PATH.exists() else {}
BY_HASH={r['before']:ROOT/r['source'] for r in RECORDS.values()}
def selected_source(path):
    p=Path(path)
    return BY_HASH.get(hashlib.sha256(p.read_bytes()).hexdigest(),p)
def open_selected(path):return Image.open(selected_source(path))
