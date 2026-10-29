from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from build.blender_package import build_blender_theme
from build.tokens import load_tokens

ROOT = Path(__file__).parent.parent


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m build")
    parser.add_argument("target", choices=["blender-theme"])
    arguments = parser.parse_args()

    tokens = load_tokens(ROOT / "tokens" / "tokens.json")
    if arguments.target == "blender-theme":
        try:
            print(build_blender_theme(ROOT, tokens))
        except FileNotFoundError as error:
            raise SystemExit(f"build failed: {error}")
        except subprocess.CalledProcessError as error:
            raise SystemExit(f"build failed: Blender exited with code {error.returncode}")


if __name__ == "__main__":
    main()
