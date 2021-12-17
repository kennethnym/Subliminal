import os.path
import yaml
from threading import Thread
from typing import Any
from yaml.error import YAMLError

from .daemon.api.device import DeviceAddedEvent, DeviceRemovedEvent
from .panel import create_output_panel, show_output_panel
from .messages import INDEXING_IN_PROGRESS_MESSAGE, NOT_A_DART_FLUTTER_PROJECT_MESSAGE, NOT_A_FLUTTER_PROJECT_MESSAGE
from .process import run_process
from .env import get_dart_path, get_flutter_path, load_env
from .constants import PUBSPEC_YAML_FILE_NAME

import sublime


class CurrentProject(object):
    def __init__(self, window, daemon_client):
        self.__window = window
        self.__path = window.folders()[0]
        self.__pubspec = {} # type: dict[str, Any]
        self.__availble_devices = {}
        self.__daemon_client = daemon_client
        self.__is_pubspec_invalid = True
        self.__is_flutter_project = False

        self.__load_pubspec()


    @property
    def window(self):
        return self.__window


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

    
    def has_dependency_on(self, dep):
        return self.__pubspec["dependencies"][dep] is not None


    def __daemon_event_listener(self, event):
        if isinstance(event, DeviceAddedEvent):
            self.__availble_devices[event.device.id] = event.device
        elif isinstance(event, DeviceRemovedEvent):
            self.__availble_devices.pop(event.device.id)


    def __load_pubspec(self):
        with open(os.path.join(self.__path, PUBSPEC_YAML_FILE_NAME)) as stream:
            try:
                self.__pubspec = yaml.safe_load(stream)
                self.__is_pubspec_invalid = False
                self.__is_flutter_project = self.has_dependency_on("flutter")
            except YAMLError:
                self.__is_pubspec_invalid = True
                pass

    
    def __start_process(self, command):
        panel = create_output_panel(self.__window)

        show_output_panel(self.__window)

        Thread(
            target=run_process,
            args=(
                [
                    get_flutter_path(self.__window)
                    if self.__is_flutter_project
                    else get_dart_path(self.__window)
                ]
                + command,
                self.__path,
                panel,
            ),
        ).start()
