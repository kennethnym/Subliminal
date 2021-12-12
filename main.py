import os
from .core.project import load_project
from .commands import *

import sublime as sublime
import sublime_plugin as sublime_plugin


__all__ = ["ExampleCommand", "PubGetCommand", "FlutterCleanCommand"]


class SublimeEventListener(sublime_plugin.EventListener):
    def on_load_async(self, view):
        window = view.window()
        load_project(window)
