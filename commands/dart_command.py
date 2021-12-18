from ..core.messages import COMMAND_UNAVAILABLE
from ..core.window_manager import get_window_manager, is_window_ignored

import sublime
import sublime_plugin


class DartCommand(sublime_plugin.WindowCommand):
    def is_enabled(self):
        return not is_window_ignored(self.window)


    def project(self):
        wm = get_window_manager(self.window)

        if project := wm.project:
            return project

        sublime.error_message(COMMAND_UNAVAILABLE)
        return None
