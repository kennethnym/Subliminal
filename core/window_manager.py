import asyncio
import os

from .project import CurrentProject
from .daemon import FlutterDaemon, FlutterDaemonClient

import sublime


class WindowManager(object):
    def __init__(self, window) -> None:
        super().__init__()
    
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
            self.__daemon_client = FlutterDaemonClient(self.__daemon)
            self.__project = CurrentProject(window, self.__daemon_client)

            asyncio.create_task(self.__initialize())
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

        self.__daemon.start()
        self.__is_daemon_started = True


    def unload(self):
        self.__daemon.terminate()
        _unregister_window_manager(self.__window)


    async def __initialize(self):
        while not self.__daemon.is_started:
            continue

        await self.__project.initialize()
        await self.__daemon_client.device.enable()


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
