"""Build a local environment catalogue from explicit, hash-verified selections."""
import argparse
import html
import json
from pathlib import Path
from urllib.parse import quote
from audit_environment_pack import inspect_pack


def build(ledger_path):
    report = inspect_pack(ledger_path)
    pack = ledger_path.resolve().parent
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    title = html.escape(ledger.get("title", pack.name.replace("-", " ").title()))
    cards = []
    for source in report["sources"]:
        if not source["selected"]:
            continue
        name = html.escape(source["id"].replace("-", " ").title())
        path = quote(source["file"])
        size = " × ".join(map(str, source["native_size"]))
        cards.append(f'<article><a href="{path}"><img src="{path}" alt="{name}"></a>'
                     f'<h2>{name}</h2><p>{size} · original pixels · {source["mode"]}</p></article>')
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BRINE — TITLE</title><style>body{background:#081d26;color:#bdd0c8;font:16px/1.6 system-ui;margin:0}main{max-width:1440px;margin:auto;padding:36px 24px}h1{font-size:38px}p{max-width:940px;color:#93ada8}a{color:#acd4c1}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}article{padding:16px;background:#13313a}article img{width:100%;aspect-ratio:1;object-fit:contain}h2{font-size:20px}nav{margin:24px 0}figure{margin:24px 0}figure img{width:100%}@media(max-width:900px){.grid{grid-template-columns:repeat(2,1fr)}}@media(max-width:500px){.grid{grid-template-columns:1fr}}</style>
<main><small>BRINE / UNDERWATER ASSET LIBRARY</small><h1>TITLE</h1>'''.replace("TITLE", title)
    page += f'<p>{report["identity_count"]} selected identities from {report["source_count"]} preserved sources. Original colors below; station previews show runtime tint. The source audit checks provenance and alpha, not visual acceptance.</p>'
    page += '<nav><a href="README.md">Integration and review</a> · <a href="manifest.json">Source ledger</a> · <a href="generation-record.json">Original prompts</a></nav><section class="grid">'
    page += "\n".join(cards) + '</section>'
    for preview in ledger.get("native_previews", []):
        path, label = html.escape(preview["path"], quote=True), html.escape(preview["label"])
        page += f'<figure><a href="{path}"><img loading="lazy" src="{path}" alt="{label}"></a><figcaption>{label}</figcaption></figure>'
    page += '</main></html>'
    (pack / "index.html").write_text(page, encoding="utf-8")
    print(f'Catalogue written: {pack / "index.html"}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    build(parser.parse_args().ledger)
