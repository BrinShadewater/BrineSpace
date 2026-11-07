"""Fail if tracked game media or binary payloads enter the code-only repository."""

from pathlib import Path
import subprocess


MEDIA_EXTENSIONS = {
    ".png", ".apng", ".jpg", ".jpeg", ".gif", ".webp", ".svg",
    ".ogv", ".mp4", ".mov", ".avi", ".wav", ".ogg", ".flac", ".aiff",
    ".ttf", ".otf", ".woff", ".woff2", ".res", ".translation",
    ".pck", ".zip", ".gz", ".dmg", ".exe", ".bin", ".log",
}
LFS_POINTER = b"version https://git-lfs.github.com/spec/v1\n"


def main():
    root = Path(__file__).resolve().parents[1]
    names = subprocess.check_output(["git", "-C", str(root), "ls-files", "-z"]).split(b"\0")
    problems = []
    count = 0
    for raw in names:
        if not raw:
            continue
        relative = raw.decode("utf-8")
        path = root / relative
        count += 1
        if path.suffix.lower() in MEDIA_EXTENSIONS:
            problems.append(f"media/log extension: {relative}")
            continue
        if not path.is_file():
            problems.append(f"missing tracked file: {relative}")
            continue
        data = path.read_bytes()
        if data.startswith(LFS_POINTER):
            problems.append(f"LFS pointer: {relative}")
        elif b"\0" in data:
            problems.append(f"binary content: {relative}")
    for problem in problems[:25]:
        print(problem)
    if len(problems) > 25:
        print(f"... and {len(problems) - 25} more")
    print(f"Checked {count:,} tracked paths; {len(problems)} source-only violations")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
