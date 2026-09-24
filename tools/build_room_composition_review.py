"""Build a same-scale selected-card board from the native inventory audit.

No raster is changed. Refuse missing ledger entries, invalid or changed cards.
"""
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]


def build(inventory_path, output, include_incomplete=False):
    raw = inventory_path.read_text(encoding='utf-8-sig')
    inventory = json.loads(raw[raw.index('{'):])
    if inventory['errors'] and not include_incomplete:
        raise ValueError(inventory['errors'])
    ledger = {r['id']: r for r in json.loads((ROOT / 'docs/ORGANIC_ROOM_ROLLOUT.json').read_text())['rooms']}
    cards = []
    review_counts = {'current': 0, 'stale': 0, 'missing': 0}
    for row in inventory['rooms']:
        if not row['card_sha256'] or not row['ledger_present']:
            if not include_incomplete:
                raise ValueError(f"Incomplete inventory row: {row['id']}")
            cards.append(f'<article><p class="missing">Awaiting selected art or furnishing record</p>'
                         f'<h2>{html.escape(row["name"])}</h2><code>{html.escape(row["id"])}</code>'
                         '<p>Not visually reviewed. No substitute card is shown.</p></article>')
            continue
        source = ROOT / row['card'].removeprefix('res://')
        if hashlib.sha256(source.read_bytes()).hexdigest() != row['card_sha256']:
            raise ValueError(f"Selected card changed after inventory: {row['id']}")
        entry = ledger[row['id']]
        limitations = entry.get('limitations', 'Visual review pending')
        if isinstance(limitations, list):
            limitations_html = '<ul>' + ''.join('<li>' + html.escape(str(item)) + '</li>' for item in limitations) + '</ul>'
        else:
            limitations_html = '<p>' + html.escape(str(limitations)) + '</p>'
        revision = entry.get('composition_revision', '')
        revision_html = f'<p>{html.escape(revision)}</p>' if revision else ''
        review = entry.get('visual_review', {})
        review_state = 'missing' if not review else ('current' if review.get('card_sha256') == row['card_sha256'] else 'stale')
        review_counts[review_state] += 1
        if review_state != 'current' and revision:
            revision_html = '<p>Recorded composition note (not verified against selected card):</p>' + revision_html
        review_label = 'Visual findings recorded' if review.get('card_sha256') == row['card_sha256'] else ('Visual findings need refresh' if review else 'Visual findings not recorded')
        scope = review.get('scope', 'Scope not recorded; consult the linked evidence.') if review else 'No visual review recorded.'
        scope_html = f'<p class="review-scope">Recorded review scope: {html.escape(str(scope))}</p>'
        review_html = ''
        if review:
            if review.get('card_sha256') != row['card_sha256']:
                review_html = '<p class="missing">Recorded visual review predates the selected card. Review again.</p>'
            else:
                findings = ''.join(f'<li>{html.escape(item)}</li>' for item in review.get('findings', []))
                review_html = f'<p>{html.escape(review.get("decision", ""))}</p><ul>{findings}</ul>'
        href = quote(os.path.relpath(source, output.parent).replace('\\', '/'), safe='/')
        cards.append(f'<article><a href="{href}"><img src="{href}" alt="{html.escape(row["name"])}"></a>'
                     f'<h2>{html.escape(row["name"])}</h2><code>{html.escape(row["id"])}</code>'
                     f'<p class="review-state">{review_label}</p>'
                     f'{scope_html}'
                     f'<details><summary>Recorded evidence and limitations</summary>{revision_html}{review_html}{limitations_html}'
                     f'<p>{html.escape(row["card"])}</p><p>SHA-256: {row["card_sha256"]}</p></details></article>')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
                      '<title>BrineSpace room composition review</title><style>'
                      'body{background:#102127;color:#d6e3df;font:16px system-ui;margin:32px}h1{font-size:26px}'
                      'main{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px}'
                      'article{background:#1c3036;padding:16px;border:1px solid #39535a}img{display:block;width:100%;aspect-ratio:1;object-fit:contain;image-rendering:pixelated}'
                      'h2{font-size:19px;margin-bottom:6px}code{color:#91b2ad}details{margin-top:12px;overflow-wrap:anywhere}summary{cursor:pointer}'
                      '.missing{color:#ffbd99;border:1px solid #b87655;padding:24px}'
                      '.review-state{font-size:13px;color:#bdcec8}'
                      '</style><h1>Room composition review</h1>'
                      + ('<p class="missing">Incomplete inventory report: '+html.escape('; '.join(inventory['errors']))+'</p>' if inventory['errors'] else '') +
                      f'<p>{len(cards)} current database identities. Equal-size selected card previews; these are not fresh station renders or visual approval.</p>'
                      f'<p>Review records: {review_counts["current"]} match current card bytes; {review_counts["stale"]} refer to older cards; {review_counts["missing"]} have no visual review. Stale records do not imply missing art or a need to replace the room. Matching hashes do not establish owner acceptance.</p>'
                      '<p>Review supported objects, activity grouping, service connections, department character and clear circulation. Confirm findings in native station views.</p>'
                      '<main>' + ''.join(cards) + '</main></html>', encoding='utf-8')
    print(f'Built {len(cards)} room review entries: {output}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inventory', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--include-incomplete', action='store_true', help='Show explicit missing-art entries; does not waive inventory or export gates')
    args = parser.parse_args()
    build(args.inventory, args.output.resolve(), args.include_incomplete)
