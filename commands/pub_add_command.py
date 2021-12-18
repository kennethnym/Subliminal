from .dart_command import DartCommand

import sublime_plugin


class PubAddCommand(DartCommand):
    def run(self, package_name):
        if project := super().project():
            project.pub_add(package_name)


    def input(self, _):
        return PackageNameInputHandler()


class PackageNameInputHandler(sublime_plugin.TextInputHandler):
    def name(self):
        return "package_name"


    def validate(self, arg: str) -> bool:
        return bool(arg)


    def placeholder(self):
        return "package_name[:@x.y.z]"
