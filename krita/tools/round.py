from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PLUGINS = Path.home() / "Library" / "Application Support" / "krita" / "pykrita"
WORK = Path("/tmp/uikit-krita")
UNPACKED = WORK / "plugin"
VENV_PYTHON = ROOT / ".venv" / "bin" / "python"


def running() -> bool:
    return subprocess.run(["pgrep", "-lx", "krita"], capture_output=True).returncode == 0


def main() -> None:
    # One polish round: build the zip, unpack it, link it plus the capture plugin into
    # Krita's plugin folder, run Krita, and always remove the links afterwards.
    if running():
        raise SystemExit("Krita is running. Close it first.")
    zip_path = Path(subprocess.run([str(VENV_PYTHON), "-m", "build", "krita-plugin"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip().splitlines()[-1])
    if UNPACKED.exists():
        subprocess.run(["rm", "-rf", str(UNPACKED)], check=True)
    UNPACKED.mkdir(parents=True)
    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(UNPACKED)

    links = {
        PLUGINS / "uikit_theme.desktop": UNPACKED / "uikit_theme.desktop",
        PLUGINS / "uikit_theme": UNPACKED / "uikit_theme",
        PLUGINS / "capture.desktop": ROOT / "krita" / "tools" / "capture" / "capture.desktop",
        PLUGINS / "capture": ROOT / "krita" / "tools" / "capture" / "capture",
    }
    created = []
    try:
        for link, target in links.items():
            link.symlink_to(target)
            created.append(link)
        subprocess.run([str(VENV_PYTHON), str(ROOT / "krita" / "tools" / "run_krita.py"), "uikit_theme", "capture", *sys.argv[1:]], check=True)
    finally:
        for link in created:
            link.unlink()
        leftovers = [path.name for path in PLUGINS.iterdir() if path.name.startswith(("uikit", "capture", "spike"))]
        print("links left:", leftovers)


if __name__ == "__main__":
    main()
