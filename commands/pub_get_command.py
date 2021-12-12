from .dart_command import DartCommand

import sublime
import sublime_plugin

class PubGetCommand(DartCommand):
    def run(self, _):
        project = super(PubGetCommand, self).get_current_project()
        if project:
            project.pub_get()
