import asyncio
import os
from threading import Thread

from .daemon.api.daemon import DaemonConnectedEvent
from .project import CurrentProject
from .daemon import FlutterDaemon, FlutterDaemonClient
from .env import Env

import sublime


class WindowManager:
    def __init__(self, window: sublime.Window) -> None:
        super().__init__()
    
        env_dict = sublime.load_settings("LSP-Dart.sublime-settings").get("env", dict(os.environ))

        if "FLUTTER_ROOT" in env_dict:
            env = Env.from_dict(env_dict)

            self.__window = window
            self.__is_daemon_started = False
            self.__daemon = FlutterDaemon(env.flutter_path)
            self.__daemon_client = FlutterDaemonClient(self.__daemon)
            self.__project = CurrentProject(window, env, self.__daemon_client)
        else:
            sublime.error_message('Unable to determine the path to the Flutter SDK. Please define "FLUTTER_ROOT" under the "env" key in LSP-Dart settings.')


    @property
    def project(self):
        return self.__project


    def start_daemon(self):
        if self.__is_daemon_started:
            return

        self.__daemon_client.add_event_listener(self.__daemon_event_listener)
        self.__daemon.start()
        self.__is_daemon_started = True


    def unload(self):
        self.__daemon.terminate()
        _unregister_window_manager(self.__window)


    def __daemon_event_listener(self, event):
        if isinstance(event, DaemonConnectedEvent):
            Thread(target=lambda: asyncio.run(self.__initialize())).start()


    async def __initialize(self):
        await self.__project.initialize()
        await self.__daemon_client.device.enable()


__window_managers = {}


def _unregister_window_manager(window):
    try:
        __window_managers.pop(window.id())
    except KeyError:
        pass


def get_window_manager(window) -> WindowManager:
    win_id = window.id()
    try:
        return __window_managers[win_id]
    except KeyError:
        wm = WindowManager(window)
        __window_managers[window.id()] = wm
        return wm
