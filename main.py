import os
from .core.project import get_project_manager
from .core.view_manager import get_view_manager
from .commands import *

import sublime
import sublime_plugin


class SublimeEventListener(sublime_plugin.EventListener):
    def __init__(self) -> None:
        super().__init__()
        self.__view_manager = get_view_manager()
        self.__project_manager = get_project_manager()

    def on_load_async(self, view):
        window = view.window()
        self.__view_manager.register_view(view)
        if not self.__view_manager.window_has_views(view.window()):
            self.__project_manager.load_project(window)

    def on_close(self, view):
        window = view.window()
        self.__view_manager.unregister_view(view)
        if not self.__view_manager.window_has_views(window):
            get_project_manager().unload_project(window)
