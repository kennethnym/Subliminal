from ..core.messages import COMMAND_UNAVAILABLE
from .dart_command import DartCommand

import sublime


class PubGetCommand(DartCommand):
    def run(self):
        project = super().project()
        if project:
            project.pub_get()
        else:
            sublime.error_message(COMMAND_UNAVAILABLE)
