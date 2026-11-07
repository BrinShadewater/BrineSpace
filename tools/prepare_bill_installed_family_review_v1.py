"""Reuse the existing physical-scale review layout with the verified installed inventory."""
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'character/bill-installed-coverage-2026-10-04'
s=(R/'character/bill-full-family-consistency-2026-10-03-v1/build_review.py').read_text();a=s.index('spec=');b=s.index('masters={')
s=s[:a]+"audit=json.loads((P/'source-audit.json').read_text())\n"+s[b:]
(D/'build_review.py').write_text(s,encoding='utf-8')
