from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from build.blender_package import build_blender_addon, build_blender_theme
from build.fonts import build_fonts
from build.freecad_pack import build_freecad_pack
from build.krita_package import build_krita_plugin
from build.solidcraft_theme import build_solidcraft_theme
from build.tokens import load_tokens

ROOT = Path(__file__).parent.parent


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m build")
    parser.add_argument(
        "target",
        choices=["blender-theme", "blender-addon", "krita-plugin", "freecad-pack", "solidcraft-theme", "fonts"],
    )
    arguments = parser.parse_args()

    try:
        if arguments.target == "blender-theme":
            print(build_blender_theme(ROOT, load_tokens(ROOT / "tokens" / "tokens.json")))
        elif arguments.target == "blender-addon":
            print(build_blender_addon(ROOT))
        elif arguments.target == "freecad-pack":
            print(build_freecad_pack(ROOT, load_tokens(ROOT / "tokens" / "tokens.json")))
        elif arguments.target == "solidcraft-theme":
            print(build_solidcraft_theme(ROOT, load_tokens(ROOT / "tokens" / "tokens.json")))
        elif arguments.target == "fonts":
            for path in build_fonts(ROOT):
                print(path)
        else:
            print(build_krita_plugin(ROOT, load_tokens(ROOT / "tokens" / "tokens.json"), ROOT / "dist"))
    except FileNotFoundError as error:
        raise SystemExit(f"build failed: {error}")
    except subprocess.CalledProcessError as error:
        raise SystemExit(f"build failed: Blender exited with code {error.returncode}")


if __name__ == "__main__":
    main()
