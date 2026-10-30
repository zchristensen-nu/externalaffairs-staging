"""Make a claude.ai Artifact copy of docs/ for native commenting.

The artifact wraps its main page in its own skeleton, serves directory links only as explicit files, and blocks fonts from
other hosts, so: strip index.html's document wrapper, point `dir/` links at `dir/index.html`, and bundle FF Real Head.
    python3 build/artifact.py <out-dir> <fonts-dir>     # then publish <out-dir>/index.html with every other file
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
out, fonts = Path(sys.argv[1]), Path(sys.argv[2])
shutil.rmtree(out, ignore_errors=True)
shutil.copytree(ROOT / "docs", out, ignore=shutil.ignore_patterns("404.html", ".nojekyll"))
shutil.copytree(fonts, out / "assets/fonts")
css = out / "assets/nu-ds.css"
css.write_text(css.read_text().replace("https://www.northeastern.edu/wp-content/themes/nu-start-child/fonts/", "fonts/"))


def fix(m):
    u = m.group(1)
    if u.startswith(("http", "mailto:", "tel:", "#", "/")):
        return m.group(0)
    path, _, frag = u.partition("#")
    if path == "" or path.endswith("/"):
        path += "index.html"
    return f'href="{path}{"#" + frag if frag else ""}"'


for f in out.rglob("*.html"):
    s = re.sub(r'href="([^"]*)"', fix, f.read_text())
    if f == out / "index.html":
        head = re.sub(r'<meta charset[^>]*>|<meta name="viewport"[^>]*>', "", re.search(r"<head>(.*?)</head>", s, re.S).group(1))
        s = head.strip() + "\n" + re.search(r"<body[^>]*>(.*)</body>", s, re.S).group(1)
    f.write_text(s)

files = {str(p.relative_to(out)): str(p.relative_to(out)) for p in out.rglob("*") if p.is_file() and p.name != "index.html" or p.is_file() and p.parent != out}
files.pop("index.html", None)
(out.parent / f"{out.name}-files.json").write_text(json.dumps(files))
print(len(files), "files besides index.html")
