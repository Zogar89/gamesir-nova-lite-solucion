"""Check links and archive integrity without running the firmware updater."""
import hashlib
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import zipfile

root = Path(__file__).resolve().parent / "dist"

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            assert values["id"] not in self.ids, f"Duplicate ID: {values['id']}"
            self.ids.add(values["id"])
        for field in ["href", "src"]:
            if field in values:
                self.links.append(values[field])

page = Page()
html = (root / "index.html").read_text(encoding="utf-8")
page.feed(html)
for link in page.links:
    if link.startswith("#"):
        assert link[1:] in page.ids, f"Broken anchor {link}"
    elif not link.startswith(("http:", "https:", "data:")):
        assert (root / link).is_file(), f"Missing asset {link}"
manifest = json.loads((root / "downloads" / "kit-manifest.json").read_text())
data = (root / "downloads" / manifest["filename"]).read_bytes()
assert len(data) == manifest["bytes"]
assert hashlib.sha256(data).hexdigest() == manifest["sha256"]
with zipfile.ZipFile(io.BytesIO(data)) as archive:
    assert archive.testzip() is None
    names = archive.namelist()
    assert len(names) == 7
    assert [name for name in names if name.endswith(".ufw")] == ["T4N_dog_V16_update.ufw"]
    assert all("/" not in name and "\\" not in name for name in names)
    for line in archive.read("SHA256SUMS.txt").decode().splitlines():
        expected, name = line.split("  ", 1)
        assert hashlib.sha256(archive.read(name)).hexdigest() == expected, name
assert hashlib.sha256((root / "downloads" / "T4N_dog_V16_update.ufw").read_bytes()).hexdigest() == "6fdf627ec7f55aeae97cc17312d9c11107bafdbf989fd5f28dbd23d9a34a0a33"
assert all(path.stat().st_size < 100 * 1024 * 1024 for path in root.rglob("*") if path.is_file())
print(json.dumps({"local_links": len(page.links), "kit_bytes": len(data), "archive_files": names, "sha256": manifest["sha256"], "status": "passed"}, indent=2))
