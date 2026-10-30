import sys
from pathlib import Path

version = sys.argv[1]
lines = Path("CHANGELOG.md").read_text().splitlines(keepends=True)

for i, line in enumerate(lines):
    if line.rstrip("\r\n") == f"## [{version}]":
        start = i + 1
        break
else:
    raise SystemExit(f"CHANGELOG.md: missing '## [{version}]' section")

end = start
for end in range(start, len(lines)):
    if lines[end].startswith("## ["):
        break

notes = "".join(lines[start:end]).strip()
Path("release-notes.md").write_text(notes + "\n")
