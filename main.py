import os
from .core.window_manager import get_window_manager
from .commands import *

import sublime
import sublime_plugin


class SublimeEventListener(sublime_plugin.ViewEventListener):
    def __init__(self, view) -> None:
        super().__init__(view)
        self.__window = view.window()
        self.__window_manager = None


    def on_activated(self):
        if not self.__window_manager:
            self.__window_manager = get_window_manager(self.__window)
            if self.__window_manager.project:
                self.__window_manager.start_daemon()


    def on_close(self):
        wm = self.__window_manager
        if wm:
            wm.on_view_closed()
