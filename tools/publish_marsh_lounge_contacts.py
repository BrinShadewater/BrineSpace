"""Remove rejected corner-armchair movies from the current Marsh review."""
from pathlib import Path
import json, re
ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'output/marsh-rest-2026-10-14/corner-native'
OUT = ROOT / 'character/marsh-rest-review-2026-10-14/review'
def main():
    report = json.loads((EVIDENCE / 'report.json').read_text())
    assert report['failures'] == 0
    path = OUT / 'index.html'
    html = path.read_text(encoding='utf-8')
    html = re.sub(r'<article><h3>crew_lounge-q[0-3].*?</article>', '', html, flags=re.S)
    html = html.replace('Current lounge and bunk · retained', 'Current bunk · corner armchairs omitted')
    html = html.replace('Actual north-facing lounge lifecycle in four rotations and east-facing station-prop bunk entry, rest and exit. These retain their current artwork and choreography.', 'Marsh no longer sits on the angled corner lounge armchairs. Their rejected clips are removed from this review. The reading seats and east-facing bunk remain available. Other crew retain their existing chair use.')
    path.write_text(html, encoding='utf-8')
    (OUT / 'lounge-contact-publication.json').write_text(json.dumps({'cornerArmchairsExcludedFor': 'marsh', 'nativeFailures': report['failures'], 'evidence': str(EVIDENCE.relative_to(ROOT))}, indent=2) + '\n')
    print('Removed four rejected corner-chair videos from the current gallery')
if __name__ == '__main__': main()
