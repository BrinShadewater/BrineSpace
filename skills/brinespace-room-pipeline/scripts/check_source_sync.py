"""Read-only comparison of an installed skill with its maintained source.

--ignore-eol   treat CRLF/LF-only differences as equal (Windows checkouts and
               installed copies often differ only in line endings).
--expected F   JSON list of {"path": ..., "reason": ...} entries that are
               deliberately divergent; they are reported but do not fail.
"""
import argparse, hashlib, json
from pathlib import Path

def digest(path, ignore_eol=False):
    data = path.read_bytes()
    if ignore_eol:
        data = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--installed", type=Path, required=True)
    parser.add_argument("--ignore-eol", action="store_true")
    parser.add_argument("--expected", type=Path, help="JSON allowlist of deliberate divergences")
    args = parser.parse_args()
    for folder in [args.source, args.installed]:
        if not (folder / "SKILL.md").is_file():
            parser.error(f"Not a skill directory: {folder}")
    expected = {}
    if args.expected:
        for entry in json.loads(args.expected.read_text(encoding="utf-8")):
            expected[entry["path"].replace("\\", "/")] = entry.get("reason", "")
    differences = []
    allowed = []
    checked = 0
    for original in sorted(args.source.rglob("*")):
        if not original.is_file() or any(p in {".git", "__pycache__"} for p in original.parts):
            continue
        relative = original.relative_to(args.source)
        key = relative.as_posix()
        installed = args.installed / relative
        checked += 1
        status = None
        if not installed.is_file():
            status = "missing"
        elif digest(original, args.ignore_eol) != digest(installed, args.ignore_eol):
            status = "different"
        if status is None:
            continue
        if key in expected:
            allowed.append({"path": key, "status": status, "reason": expected[key]})
        else:
            differences.append({"path": key, "status": status})
    print(json.dumps({"checked": checked, "differences": differences, "expected_divergences": allowed}, indent=2))
    return 1 if differences else 0

if __name__ == "__main__":
    raise SystemExit(main())
