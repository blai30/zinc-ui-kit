from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from pathlib import Path

KRITA = "/Applications/krita.app/Contents/MacOS/krita"
REAL_RC = Path.home() / "Library" / "Preferences" / "kritarc"
WORK = Path("/tmp/uikit-krita")


def prepare(plugin_ids: list) -> None:
    # Krita reads kritarc and the plugin folder from the real profile whatever HOME is,
    # so a run rewrites the real kritarc. Keep one backup of the original.
    WORK.mkdir(parents=True, exist_ok=True)
    backup = WORK / "kritarc.backup"
    if REAL_RC.exists() and not backup.exists():
        shutil.copy2(REAL_RC, backup)
    text = "[python]\n" + "".join(f"enable_{plugin_id}=true\n" for plugin_id in plugin_ids)
    with open(REAL_RC, "w", encoding="utf-8", newline="\n") as file:
        file.write(text)


def restore() -> None:
    backup = WORK / "kritarc.backup"
    if backup.exists():
        shutil.copy2(backup, REAL_RC)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plugin_ids", nargs="*")
    parser.add_argument("--out", default=str(WORK / "out"))
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--restore", action="store_true", help="put the original kritarc back and exit")
    arguments = parser.parse_args()

    if arguments.restore:
        restore()
        return
    prepare(arguments.plugin_ids)
    out = Path(arguments.out)
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    environment = {**os.environ, "UIKIT_OUT": str(out)}
    with open(WORK / "stdout.txt", "w") as log:
        process = subprocess.Popen([KRITA, "--nosplash"], env=environment, stdout=log, stderr=subprocess.STDOUT)
        try:
            process.wait(timeout=arguments.timeout)
        except subprocess.TimeoutExpired:
            # Only ever stop the child this script started.
            process.terminate()
    print("exit", process.poll(), sorted(path.name for path in out.iterdir()))


if __name__ == "__main__":
    main()
