import os
from .core.window_manager import WindowManager, get_window_manager
from .core.constants import PUBSPEC_YAML_FILE_NAME
from .commands import *

import sublime
import sublime_plugin


class SublimeEventListener(sublime_plugin.EventListener):
    def __init__(self) -> None:
        super().__init__()
        self.__is_applicable = False
        self.__window_manager = None # type: WindowManager | None


    def on_new_window_async(self, window: sublime.Window):    
        project_path = window.folders()[0]
        self.__is_applicable = os.path.isfile(
            os.path.join(project_path, PUBSPEC_YAML_FILE_NAME)
        )
        if self.__is_applicable and not self.__window_manager:
            wm = get_window_manager(window)
            self.__window_manager = wm
            if wm.project:
                wm.start_daemon()


    def on_pre_close_window(self, _):
        wm = self.__window_manager
        if wm:
            wm.unload()
