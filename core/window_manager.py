import asyncio
import os
import subprocess
from threading import Thread
from typing import Dict, Set

from .plugin_settings import PluginSettings
from .rpc.api.daemon import DaemonConnectedEvent
from .project import CurrentProject
from .rpc import FlutterRpcProcess, FlutterRpcClient
from .env import Env

import sublime


class WindowManager:
    def __init__(self, window: sublime.Window) -> None:
        super().__init__()
    
        env_dict = sublime.load_settings("LSP-Dart.sublime-settings").get("env", dict(os.environ))
        settings = sublime.load_settings("Subliminal.sublime-settings").to_dict()

        self.__plugin_settings = PluginSettings(**settings)

        if "FLUTTER_ROOT" in env_dict:
            env = Env.from_dict(env_dict)
            loop = asyncio.new_event_loop()

            self.__env = env
            self.__window = window
            self.__is_daemon_started = False
            self.__event_loop = loop
            self.__daemon = FlutterRpcProcess([env.flutter_path, "daemon"], loop)
            self.__daemon_client = FlutterRpcClient(self.__daemon)
            self.__project = CurrentProject(window, env, self.__daemon_client, loop)
        else:
            sublime.error_message('Unable to determine the path to the Flutter SDK. Please define "FLUTTER_ROOT" under the "env" key in LSP-Dart settings.')


    @property
    def env(self):
        return self.__env


    @property
    def project(self):
        return self.__project


    @property
    def event_loop(self):
        return self.__event_loop


    @property
    def plugin_settings(self):
        return self.__plugin_settings


    def start_daemon(self):
        if self.__is_daemon_started:
            return

        Thread(target=self.__event_loop.run_forever).start()
        self.__daemon_client.add_event_listener(self.__daemon_event_listener)
        self.__daemon.start()
        self.__is_daemon_started = True


    def unload(self):
        self.__daemon.terminate()
        _unregister_window_manager(self.__window)


    def __daemon_event_listener(self, event):
        if isinstance(event, DaemonConnectedEvent):
            asyncio.run_coroutine_threadsafe(self.__initialize(), self.__event_loop)


    async def __initialize(self):
        await self.__project.initialize()
        await self.__daemon_client.device.enable()


_window_managers: Dict[int, WindowManager] = {}

_ignored_window: Set[int] = set()


def _unregister_window_manager(window: sublime.Window):
    try:
        _window_managers.pop(window.id())
    except KeyError:
        pass


def ignore_window(window: sublime.Window):
    _ignored_window.add(window.id())


def unignore_window(window: sublime.Window):
    _ignored_window.remove(window.id())


def is_window_ignored(window: sublime.Window):
    return window.id() in _ignored_window


def get_window_manager(window) -> WindowManager:
    win_id = window.id()
    try:
        return _window_managers[win_id]
    except KeyError:
        wm = WindowManager(window)
        _window_managers[window.id()] = wm
        return wm


def unload_window_manager(window: sublime.Window):
    try:
        _window_managers[window.id()].unload()
    except KeyError:
        pass


def unload_window_managers():
    for _, wm in _window_managers.items():
        wm.unload()
