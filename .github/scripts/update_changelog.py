import sys
from pathlib import Path

old, new = sys.argv[1:3]
lines = Path("CHANGELOG.md").read_text().splitlines(keepends=True)

for i, line in enumerate(lines):
    if line.rstrip("\r\n") == "## [Unreleased]":
        unreleased = i
        break
else:
    raise SystemExit("CHANGELOG.md: missing '## [Unreleased]' section")

for end in range(unreleased + 1, len(lines)):
    if lines[end].startswith("## ["):
        break
else:
    raise SystemExit("CHANGELOG.md: no section follows [Unreleased]")

if not any(entry.strip() for entry in lines[unreleased + 1 : end]):
    raise SystemExit("CHANGELOG.md: [Unreleased] is empty; nothing to release")

lines[unreleased] = f"## [{new}]\n"
lines[unreleased:unreleased] = ["## [Unreleased]\n", "\n"]

for i, line in enumerate(lines):
    if line.startswith("[Unreleased]:"):
        link = i
        break
else:
    raise SystemExit("CHANGELOG.md: missing '[Unreleased]:' link reference")

unreleased_link = lines[link]
if f"compare/{old}...HEAD" not in unreleased_link:
    raise SystemExit(
        f"CHANGELOG.md: [Unreleased] link does not end with 'compare/{old}...HEAD'"
    )
base = unreleased_link.split("]: ", 1)[1].strip().rsplit("/compare/", 1)[0]
lines[link] = f"[Unreleased]: {base}/compare/{new}...HEAD\n"
lines[link + 1 : link + 1] = [f"[{new}]: {base}/compare/{old}...{new}\n"]

Path("CHANGELOG.md").write_text("".join(lines))
