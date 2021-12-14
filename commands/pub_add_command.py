from ..core.project import get_project_manager
from .dart_command import DartCommand

import sublime_plugin


class PubAddCommand(DartCommand):
    def run(self, _, package_name):
        project = super(PubAddCommand, self).get_current_project()
        if project:
            project.pub_add(package_name)

    def input(self, _):
        return PackageNameInputHandler()


class PackageNameInputHandler(sublime_plugin.TextInputHandler):
    def name(self):
        return "package_name"

    def placeholder(self):
        return "Package name (package_name / package_name@x.y.z)"
