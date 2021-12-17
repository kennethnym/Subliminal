from threading import Thread
from typing import Any

from .daemon.flutter_daemon_client import FlutterDaemonClient
from .daemon.api.device import DeviceAddedEvent, DeviceRemovedEvent, Device
from .panel import create_output_panel, show_output_panel
from .messages import INDEXING_IN_PROGRESS_MESSAGE, NO_DEVICE_SELECTED, NOT_A_DART_FLUTTER_PROJECT_MESSAGE, NOT_A_FLUTTER_PROJECT_MESSAGE
from .env import Env
from .process import run_process

import sublime


class CurrentProject(object):
    def __init__(self, window: sublime.Window, env: Env, daemon_client: FlutterDaemonClient):
        self.target_device = None # type: str | None

        self.__window = window
        self.__path = window.folders()[0]
        self.__pubspec = {} # type: dict[str, Any]
        self.__availble_devices = {} # type: dict[str, Device]
        self.__daemon_client = daemon_client
        self.__is_pubspec_invalid = True
        self.__is_flutter_project = False
        self.__env = env

        # self.__load_pubspec()


    @property
    def window(self):
        return self.__window


    @property
    def available_devices(self):
        return self.__availble_devices.values()


    @property
    def has_connected_devices(self):
        return bool(self.__availble_devices)


    async def initialize(self):
        devices = await self.__daemon_client.device.get_devices()
        for device in devices:
            self.__availble_devices[device.id] = device
        self.__daemon_client.add_event_listener(self.__daemon_event_listener)


    def pub_get(self):
        self.__start_process(["pub", "get"])


    def clean(self):
        if self.__is_flutter_project:
            self.__start_process(["clean"])
        else:
            sublime.error_message(NOT_A_FLUTTER_PROJECT_MESSAGE)

    
    def pub_add(self, package_name):
        self.__start_process(["pub", "add", package_name])


    def run(self):
        if self.target_device and self.__is_flutter_project:
            self.__start_process(["run", "-d", self.target_device])
        else:
            sublime.error_message(NO_DEVICE_SELECTED)


    def has_dependency_on(self, dep):
        return self.__pubspec["dependencies"][dep] is not None


    def __daemon_event_listener(self, event):
        if isinstance(event, DeviceAddedEvent):
            self.__availble_devices[event.device.id] = event.device
        elif isinstance(event, DeviceRemovedEvent):
            self.__availble_devices.pop(event.device.id)

    
    def __start_process(self, command):
        panel = create_output_panel(self.__window)

        show_output_panel(self.__window)

        Thread(
            target=run_process,
            args=(
                [
                    self.__env.flutter_path
                    if self.__is_flutter_project
                    else self.__env.dart_path
                ]
                + command,
                self.__path,
                panel,
            ),
        ).start()
