import re
from pathlib import Path

import pytest

from build.colors import to_hex, to_rgb
from build.freecad_mapping import ICONS, PREFERENCES
from build.freecad_pack import PACK, render_icon, render_parameters, render_preferences, stale_freecad_files
from build.tokens import load_tokens

ROOT = Path(__file__).parent.parent
TOKENS = load_tokens(ROOT / "tokens" / "tokens.json")
PREFERENCES_XML = """\
<FCParameters>
  <FCParamGroup Name="Root">
    <FCParamGroup Name="BaseApp">
      <FCParamGroup Name="Preferences">
        <FCParamGroup Name="Editor">
          <!-- blue-500 -->
          <FCUInt Name="Text" Value="{text}"/>
        </FCParamGroup>
      </FCParamGroup>
    </FCParamGroup>
  </FCParamGroup>
</FCParameters>
"""


def test_committed_pack_matches_the_tokens():
    # Run `python -m build freecad-pack` if this fails.
    assert stale_freecad_files(ROOT, TOKENS) == []


def test_every_cfg_color_is_mapped():
    text = (ROOT / PACK / "Zinc Dark.cfg").read_text(encoding="utf-8")
    names = set(re.findall(r'<FCUInt Name="([^"]+)"', text))
    assert names == {key.rsplit("/", 1)[1] for key in PREFERENCES}


def test_every_stylesheet_parameter_is_defined():
    stylesheet = (ROOT / PACK / "Zinc Dark.qss").read_text(encoding="utf-8")
    parameters = (ROOT / PACK / "parameters" / "Zinc Dark.yaml").read_text(encoding="utf-8")
    defined = set(re.findall(r"^([\w ]+):", parameters, re.MULTILINE))
    assert set(re.findall(r"@(\w+)", stylesheet)) <= defined


def test_preferences_keep_alpha_and_rename_the_comment(monkeypatch):
    monkeypatch.setattr("build.freecad_pack.PREFERENCES", {"Editor/Text": "accent.base"})
    # The editor packs colors with a zero alpha byte.
    rendered = render_preferences(PREFERENCES_XML.format(text=0x3B82F600), TOKENS)
    red, green, blue = to_rgb(TOKENS.color("accent.base"))
    assert f'Value="{red << 24 | green << 16 | blue << 8}"' in rendered
    assert f"<!-- {TOKENS.roles['accent.base']} -->" in rendered


def test_missing_preference_raises(monkeypatch):
    mapping = {"Editor/Text": "accent.base", "Editor/Missing": "accent.base"}
    monkeypatch.setattr("build.freecad_pack.PREFERENCES", mapping)
    with pytest.raises(KeyError, match="is missing: Editor/Missing'"):
        render_preferences(PREFERENCES_XML.format(text=0), TOKENS)


def test_parameters_reference_a_generated_palette():
    text = (ROOT / PACK / "parameters" / "Zinc Dark.yaml").read_text(encoding="utf-8")
    rendered = render_parameters(text, TOKENS)
    shade = TOKENS.roles["surface.background"]
    name = shade.split("-")[0].capitalize() + shade.split("-")[1]
    assert 'Background: "@{}"'.format(name) in rendered
    assert '{}: "{}"'.format(name, TOKENS.hex("surface.background")) in rendered


def test_icon_classes_set_their_attribute():
    icon = '<svg stroke="#000000" class="stroke-base"><path fill="#000000" stroke="none" class="fill-accent"/></svg>'
    rendered = render_icon(icon, TOKENS)
    assert f'stroke="{to_hex(TOKENS.resolve(ICONS["base"]))}"' in rendered
    assert f'fill="{to_hex(TOKENS.resolve(ICONS["accent"]))}"' in rendered
    assert 'stroke="none"' in rendered


def test_unknown_icon_class_raises():
    with pytest.raises(KeyError, match="stroke-missing"):
        render_icon('<path stroke="#000000" class="stroke-missing"/>', TOKENS)


def test_additive_icons_stay_distinct_from_subtractive_ones():
    assert TOKENS.resolve(ICONS["additive"]) != TOKENS.resolve(ICONS["subtractive"])
    assert ICONS["accent"] not in (ICONS["additive"], ICONS["subtractive"])
