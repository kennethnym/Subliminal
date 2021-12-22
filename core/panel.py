from typing import Union
import sublime


_PLUGIN_OUTPUT_PANEL_NAME = "dart"

PROJECT_RUN_OUTPUT_PANEL_NAME = "dart.run_project"

# borrowed from Sublime-LSP's panel settings
# https://github.com/sublimelsp/LSP/blob/main/plugin/core/panels.py
_OUTPUT_PANEL_SETTINGS = {
    "auto_indent": False,
    "draw_indent_guides": False,
    "draw_unicode_white_space": "none",
    "draw_white_space": "none",
    "fold_buttons": True,
    "gutter": True,
    "is_widget": True,
    "line_numbers": False,
    "margin": 3,
    "match_brackets": False,
    "rulers": [],
    "scroll_past_end": False,
    "show_definitions": False,
    "tab_size": 4,
    "translate_tabs_to_spaces": False,
    "word_wrap": False
}


def create_output_panel(window: sublime.Window, name: str = _PLUGIN_OUTPUT_PANEL_NAME):
    panel = window.create_output_panel(name)
    settings = panel.settings()

    for k, v in _OUTPUT_PANEL_SETTINGS.items():
        settings.set(k, v)

    return panel


def show_output_panel(window: sublime.Window, name: str = _PLUGIN_OUTPUT_PANEL_NAME):
    window.run_command(
        "show_panel", {"panel": f"output.{name}"}
    )


def destroy_output_panel(window: sublime.Window, name: str = _PLUGIN_OUTPUT_PANEL_NAME):
    window.destroy_output_panel(name)


def append_to_output_panel(panel: sublime.View, line: str):
    panel.set_read_only(False)
    panel.run_command("append", {
        "characters": line
    })
    panel.set_read_only(True)
