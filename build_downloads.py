"""Package unchanged dongle binaries for a direct GitHub Pages download."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument("source", type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parent
out = root / "dist" / "downloads"
work = root / "work"
work.mkdir(exist_ok=True)
names = ["app_window.exe", "jl_firmware_upgrade_x64.dll", "jl_firmware_upgrade_x86.dll", "T4N_dog_V16_update.ufw"]
expected = {
    "app_window.exe": "704842f6e19dc25a5dc6f3e1d6a789b00e0bd6325691355bf84687ad49a38549",
    "jl_firmware_upgrade_x64.dll": "5e8270ba8cf3aeb38e83c72125e8dfc07bf984f259db60deb4bb274218985190",
    "jl_firmware_upgrade_x86.dll": "c2ee97a4975182146b9093492e68a3336cdd529d97696ea4d013066ec9c4dda6",
    "T4N_dog_V16_update.ufw": "6fdf627ec7f55aeae97cc17312d9c11107bafdbf989fd5f28dbd23d9a34a0a33",
}
files = {name: (args.source / name).read_bytes() for name in names}
for name, data in files.items():
    if hashlib.sha256(data).hexdigest() != expected[name]:
        raise SystemExit(f"Unexpected SHA256 for {name}")
files["LEEME.txt"] = (out / "LEEME.txt").read_text(encoding="utf-8").replace("\r\n", "\n").encode("utf-8")
files["Tutorial_EN.png"] = (root / "dist" / "assets" / "updater-official-buttons.png").read_bytes()
sums = "\n".join(f"{hashlib.sha256(data).hexdigest()}  {name}" for name, data in files.items()) + "\n"
files["SHA256SUMS.txt"] = sums.encode()
(out / "SHA256SUMS.txt").write_text(sums, encoding="utf-8")
archive = out / "GameSir_Nova_Lite_SOLO_DONGLE_V16.zip"
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for name, data in files.items():
        z.writestr(name, data)
data = archive.read_bytes()
manifest = {"filename": archive.name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
(out / "kit-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print(json.dumps({**manifest, "contents": list(files)}, indent=2))
