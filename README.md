# UI Kit

A modern, Tailwind-based look for Blender 5.2, Krita 5.3, FreeCAD 1.1, and SolidCraft. Colors, spacing, and fonts are generated from one `tokens/tokens.json`, so every app shares the same Zinc palette (Tailwind zinc grays with a rose accent). Built with Python, PyQt5 (inside Krita), and the Blender extension system.

![Krita with the theme](docs/images/krita.png)

It doesn't fork or patch any app, and the default keymaps are untouched. Nothing is deleted, only hidden or restyled.

## What's in it

- Blender theme (`uikit_zinc`): recolors the interface, panels, widgets, and editor backgrounds
- Blender add-on (`uikit_declutter`): hides tabs, panels, and workspaces by feature group (aimed at game asset work), and sets the fonts
- Krita plugin (`uikit_theme`): palette, stylesheet, fonts, and a command palette
- FreeCAD preference pack (`Zinc Dark`): stylesheet, 3D view and editor colors, and about 290 Lucide-style icons for the core Std, Sketcher, and Part Design commands
- SolidCraft theme (`Zinc`): interface, viewport, sketch, and Start screen colors

Colors only come from the Tailwind palette. Surfaces, text, and the accent go through shared roles (`surface.panel`, `accent.base`, ...), so every app layers the same way. Sketch, preview, syntax, and workspace colors keep their own Tailwind families. `zinc-935` and `zinc-915` are interpolated between zinc-950 and zinc-900 for the darkest surfaces.

## Install

Blender (5.2 or newer), once for each zip:

1. Open Preferences > Get Extensions, then the dropdown at the top right > Install from Disk.
2. Pick `uikit_zinc-0.2.0.zip` (the theme) or `uikit_declutter-0.1.0.zip` (the add-on).
3. Enable the theme under Preferences > Themes, or the add-on under Preferences > Add-ons, if Blender hasn't already.

The add-on has one checkbox per feature group in its preferences:

- Sculpting, Texture painting, Materials and shader nodes: on by default
- Rigging and animation: off by default
- Everything else (rendering, physics, compositing, scripting): off by default
- Geist and JetBrains Mono fonts: on by default

Hidden workspaces are only removed from new files. Files you open are left alone, and turning the add-on off brings everything back.

Krita (5.3):

1. Open Tools > Scripts > Import Python Plugin from File and pick `uikit_theme-0.1.0.zip`.
2. Restart Krita.
3. Enable "UI Kit Theme" in Settings > Configure Krita > Python Plugin Manager, then restart again.

Tools > Scripts > UI Kit Theme turns the whole thing off and restores Krita's own look. `Ctrl+K` (`Cmd+K` on macOS) opens a command palette that searches every Krita action.

FreeCAD (1.1):

1. Open Tools > Addon Manager, then the settings (gear) button, and add a custom repository: `https://github.com/blai30/zinc-ui-kit` with branch `freecad`.
2. Find "Zinc Theme" in the Addon Manager, install it, and restart FreeCAD.
3. Open Edit > Preferences > General, pick Zinc Dark under Theme, and click OK.
4. Restart FreeCAD again so the stylesheet and icons load everywhere.

Applying the pack runs `post.FCMacro`, which saves the icons folder to `BaseApp/Preferences/Bitmaps/CustomPathZincDark`. FreeCAD checks that folder before its built-in icons. To switch back, pick another theme, then remove the icon override in the Python console and restart:

```python
App.ParamGet("User parameter:BaseApp/Preferences/Bitmaps").RemString("CustomPathZincDark")
```

The `freecad` branch only holds the `freecad/` folder. A GitHub Action splits it out of `main` on every push, because FreeCAD looks for a pack folder at the root of an addon. For local work, link `freecad/` into your `Mod` folder instead (run `App.getUserAppDataDir()` in the Python console to find it).

SolidCraft:

1. Open the theme settings and import `solidcraft/Zinc.json`.
2. Pick Zinc. To pick up a newer build, import it again.

## Build from source

1. Create a venv: `python3 -m venv .venv`.
2. Install the dev dependencies: `.venv/bin/pip install -r requirements-dev.txt`.
3. Run the tests: `.venv/bin/python -m pytest`.
4. Build a package: `.venv/bin/python -m build <target>`.

Targets:

- `blender-theme`, `blender-addon`: need Blender installed (set `BLENDER_BIN` if it isn't in the default location)
- `krita-plugin`: no Blender needed
- `freecad-pack`, `solidcraft-theme`: rewrite the colors in `freecad/Zinc Dark/` and `solidcraft/Zinc.json` in place. Both are committed so they install straight from the repo, and a test fails if they're out of date
- `fonts`: regenerates the baked fonts from `fonts/source/`

Other packages end up in `dist/`. Change a color in `tokens/tokens.json` and rebuild to restyle everything. Per-app choices live in the mapping files (`build/blender_mapping.py`, `build/freecad_mapping.py`, and so on).

## Fonts

Geist (UI) and JetBrains Mono (monospace), both under the SIL Open Font License 1.1. The license texts are in `blender/addon/fonts/`.

The bundled copies are modified. A few alternate glyphs are mapped in because neither app can switch OpenType features on:

- Geist: footed `1` and serifed capital `I`
- JetBrains Mono: slashed `0`

They're renamed "Geist UI Kit" and "JetBrains Mono UI Kit" so they never clash with copies you have installed. Your installed fonts aren't touched. The originals are in `fonts/source/`.

## Status

Tested on macOS with Blender 5.2.3 and Krita 5.3.4. Windows should work (there's no OS-specific code in the packages) but hasn't been tested. The Krita test harness in `krita/tools/` is macOS only. FreeCAD 1.1 was tested on Windows.

Known limits:

- Blender icons aren't replaced (they're compiled into the app)
- The Blender theme only covers the interface. Viewport selection colors, node colors, and animation colors are still Blender's defaults
- Blender context menus open under the cursor (not configurable)
- In Krita the docker title bars aren't restyled
- FreeCAD workbench selector icons stay stock (workbenches register them by absolute path), and less common commands fall back to FreeCAD's own icons
- The FreeCAD pack only sets the colors it lists. Leftovers from a previous theme, like Arch or CAM colors, stay as they were
- FreeCAD additive feature icons are emerald, matching their 3D preview, so they stay distinct from red subtractive ones

## License

Code is GPL-3.0-or-later, see `LICENSE`. Fonts keep the SIL Open Font License 1.1. The FreeCAD theme is MIT, and its Lucide-derived icons are ISC, see `freecad/LICENSE`.
