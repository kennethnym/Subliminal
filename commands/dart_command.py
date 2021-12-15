from ..core.window_manager import get_window_manager
from ..core.messages import NOT_A_DART_FLUTTER_PROJECT_MESSAGE

import sublime
import sublime_plugin


class DartCommand(sublime_plugin.WindowCommand):
    def project(self):
        wm = get_window_manager(self.window)
        if wm:
            project = wm.project
            if project:
                return project

            sublime.error_message('This folder is not a Dart/Flutter project.')
            return None
        else:
            sublime.error_message('Command not available.')
            return None
