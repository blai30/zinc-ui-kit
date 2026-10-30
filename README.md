# Zinc UI Kit

A Tailwind-based theme for Blender 5.2, Krita 5.3, FreeCAD 1.1, Aseprite 1.3, and SolidCraft. Every app is generated from one `tokens/tokens.json`, so they all share the same zinc grays and rose accent. Nothing is forked or patched, and the default keymaps are untouched.

| Blender | Krita |
| --- | --- |
| ![Blender](docs/images/blender.png) | ![Krita](docs/images/krita.png) |
| **FreeCAD** | **SolidCraft** |
| ![FreeCAD](docs/images/freecad.png) | ![SolidCraft](docs/images/solidcraft.png) |
| **Aseprite** | |
| ![Aseprite](docs/images/aseprite.png) | |

## What's in it

- Blender theme (`uikit_zinc`)
- Blender add-on (`uikit_declutter`): hides tabs, panels, and workspaces by feature group, and sets the fonts
- Krita plugin (`uikit_theme`): palette, stylesheet, fonts, and a `Ctrl+K` command palette
- FreeCAD preference pack (`Zinc Dark`): stylesheet, 3D view colors, and about 290 Lucide-style icons
- Aseprite theme (`Zinc`): drawn at 2x for 100% scaling, with Lucide icons and Geist
- SolidCraft theme (`Zinc`)

## Install

Blender:

1. Open Preferences > Get Extensions > Install from Disk (dropdown at the top right).
2. Pick `uikit_zinc-0.2.0.zip` or `uikit_declutter-0.1.0.zip`.
3. Enable it under Preferences > Themes or Preferences > Add-ons.

The add-on's preferences have a checkbox per feature group (sculpting, painting, materials, rigging, rendering, etc). Hidden workspaces only get removed from new files, and turning the add-on off brings everything back.

Krita:

1. Open Tools > Scripts > Import Python Plugin from File and pick `uikit_theme-0.1.0.zip`.
2. Enable "UI Kit Theme" in Settings > Configure Krita > Python Plugin Manager.
3. Restart Krita.

FreeCAD:

1. In the Addon Manager settings, add `https://github.com/blai30/zinc-ui-kit` with branch `freecad` as a custom repository.
2. Install "Zinc Theme" and restart FreeCAD.
3. Pick Zinc Dark under Edit > Preferences > General > Theme, then restart again.

To remove the icons after switching themes, run this in the Python console and restart:

```python
App.ParamGet("User parameter:BaseApp/Preferences/Bitmaps").RemString("CustomPathZincDark")
```

Aseprite: open `zinc-theme-0.1.0.aseprite-extension` (or add it under Edit > Preferences > Extensions), then pick Zinc under Preferences > Theme. Set Screen Scaling and UI Element Scaling to 100%. A custom font set under Preferences > Theme overrides the bundled Geist.

SolidCraft: import `solidcraft/Zinc.json` in the theme settings and pick Zinc.

## Build

1. Run `python3 -m venv .venv` and `.venv/bin/pip install -r requirements-dev.txt`.
2. Run the tests with `.venv/bin/python -m pytest`.
3. Build with `.venv/bin/python -m build <target>`.

Targets are `blender-theme`, `blender-addon`, `krita-plugin`, `freecad-pack`, `solidcraft-theme`, `aseprite-theme`, and `fonts`. The Blender targets need Blender installed (set `BLENDER_BIN` if it isn't in the default location). The FreeCAD and SolidCraft targets rewrite their files in place since they install straight from the repo, and the rest go to `dist/`. Per-app color choices live in `build/*_mapping.py`.

## Known limits

- Blender icons, viewport selection, node, and animation colors are still stock
- Krita docker title bars aren't restyled
- FreeCAD workbench icons and less common commands use FreeCAD's own icons
- Aseprite sizes that are hardcoded rather than themed (timeline layer column, palette swatches) start out small at 100% UI scaling, but can be resized
- Only tested on macOS (Blender, Krita) and Windows (FreeCAD, Aseprite)

## License

Code is GPL-3.0-or-later. Geist and JetBrains Mono are under the SIL Open Font License 1.1, bundled as "Geist UI Kit" and "JetBrains Mono UI Kit" with a few alternate glyphs baked in. The FreeCAD theme is MIT and its Lucide-derived icons are ISC (see `freecad/LICENSE`). The Aseprite theme builds on Aseprite's default theme, which is CC-BY-4.0, and uses Lucide icons under ISC (see `aseprite/`).
