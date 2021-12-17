from ..core.messages import COMMAND_UNAVAILABLE
from .dart_command import DartCommand

import sublime


class FlutterCleanCommand(DartCommand):
    def run(self):
        project = super().project()
        if project:
            project.clean()
        else:
            sublime.error_message(COMMAND_UNAVAILABLE)
