import os

from .project import get_project_manager
from .daemon import FlutterDaemon

import sublime


class WindowManager(object):
    def __init__(self, window) -> None:
        super().__init__()
        self.__project = get_project_manager().load_project(window)

        if self.__project:
            env = sublime.load_settings("LSP-Dart.sublime-settings").get("env", dict(os.environ))

            if "FLUTTER_ROOT" in env:
                self.__flutter_path = os.path.join(env["FLUTTER_ROOT"], "bin", "flutter")
                try:
                    self.__dart_path = os.path.join(env["DART_SDK"], "bin", "dart")
                except KeyError:
                    self.__dart_path = os.path.join(env["FLUTTER_ROOT"], "bin", "dart")

                self.__window = window
                self.__is_daemon_started = False
                self.__daemon = FlutterDaemon(self.__flutter_path)
            else:
                sublime.error_message('Unable to determine the path to the Flutter SDK. Please define "FLUTTER_ROOT" under the "env" key in LSP-Dart settings.')


    @property
    def flutter_path(self):
        return self.__flutter_path


    @property
    def dart_path(self):
        return self.__dart_path


    @property
    def project(self):
        return self.__project


    def start_daemon(self):
        if self.__is_daemon_started:
            return

        self.__is_daemon_started = True
        self.__daemon.start()


    def on_view_closed(self):
        if not self.__window.is_valid():
            get_project_manager().unload_project(self.__window)
            _unregister_window_manager(self.__window)


    def __on_daemon_event(self, event):
        pass


__window_managers = {}


def _unregister_window_manager(window):
    try:
        __window_managers.pop(window.id())
    except KeyError:
        pass


def get_window_manager(window):
    win_id = window.id()
    try:
        return __window_managers[win_id]
    except KeyError:
        wm = WindowManager(window)
        __window_managers[window.id()] = wm
        return wm
