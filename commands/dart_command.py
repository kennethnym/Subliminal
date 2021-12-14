import sublime
import sublime_plugin

from ..core.messages import NOT_A_DART_FLUTTER_PROJECT_MESSAGE
from ..core.project import get_project_manager

class DartCommand(sublime_plugin.TextCommand):
    def get_current_project(self):
        project = get_project_manager().load_project(self.view.window())

        if not project:
            sublime.error_message(NOT_A_DART_FLUTTER_PROJECT_MESSAGE)

        return project
