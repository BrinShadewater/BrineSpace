"""Read-only comparison of an installed skill with its maintained source."""
import argparse, hashlib, json
from pathlib import Path

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--installed", type=Path, required=True)
    args = parser.parse_args()
    for folder in [args.source, args.installed]:
        if not (folder / "SKILL.md").is_file():
            parser.error(f"Not a skill directory: {folder}")
    differences = []
    checked = 0
    for original in sorted(args.source.rglob("*")):
        if not original.is_file() or any(p in {".git", "__pycache__"} for p in original.parts):
            continue
        relative = original.relative_to(args.source)
        installed = args.installed / relative
        checked += 1
        if not installed.is_file():
            differences.append({"path": str(relative), "status": "missing"})
        elif digest(original) != digest(installed):
            differences.append({"path": str(relative), "status": "different"})
    print(json.dumps({"checked": checked, "differences": differences}, indent=2))
    return 1 if differences else 0

if __name__ == "__main__":
    raise SystemExit(main())
