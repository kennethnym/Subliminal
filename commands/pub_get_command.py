from .dart_command import DartCommand

import sublime
import sublime_plugin

class PubGetCommand(DartCommand):
    def run(self):
        project = super(PubGetCommand, self).project()
        if project:
            project.pub_get()
