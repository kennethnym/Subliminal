from ..core.messages import COMMAND_UNAVAILABLE
from ..core.window_manager import get_window_manager, is_window_ignored

import sublime
import sublime_plugin


class DartCommand(sublime_plugin.WindowCommand):
    def is_enabled(self):
        return not is_window_ignored(self.window)


    @property
    def window_manager(self):
        return get_window_manager(self.window)


    def project(self):
        wm = self.window_manager

        if project := wm.project:
            return project

        sublime.error_message(COMMAND_UNAVAILABLE)
        return None
