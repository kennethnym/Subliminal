import os
from threading import Thread
from typing import List
from .core.window_manager import WindowManager, get_window_manager, ignore_window, unignore_window, unload_window_manager, unload_window_managers
from .core.constants import PUBSPEC_YAML_FILE_NAME
from .core.hot_reload import FileChangeListener
from .commands import *

import sublime
import sublime_plugin


def _load_window_manager(window: sublime.Window):
    project_path = window.folders()[0]
    applicable = os.path.isfile(
        os.path.join(project_path, PUBSPEC_YAML_FILE_NAME)
    )
    if applicable:
        wm = get_window_manager(window)
        if wm.project:
            wm.start_daemon()
    else:
        ignore_window(window)


def plugin_loaded():
    for window in sublime.windows():
        Thread(target=_load_window_manager, args=(window,)).start()


def plugin_unloaded():
    unload_window_managers()


class SublimeEventListener(sublime_plugin.EventListener):
    def __init__(self) -> None:
        super().__init__()
        self.__is_applicable = False
        self.__window_manager = None # type: WindowManager | None


    def on_new_window_async(self, window: sublime.Window):
        _load_window_manager(window)


    def on_pre_close_window(self, window: sublime.Window):
        unignore_window(window)
        unload_window_manager(window)
