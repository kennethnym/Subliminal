import os
import signal
import subprocess
from threading import Thread
from typing import List

from .daemon.flutter_daemon_client import FlutterRpcClient
from .daemon.api.device import DeviceAddedEvent, DeviceRemovedEvent, Device
from .daemon.api.app import AppStartEvent, AppStartedEvent
from .panel import create_output_panel, destroy_output_panel, show_output_panel
from .messages import APP_NOT_RUNNING, NO_DEVICE_SELECTED, NOT_A_FLUTTER_PROJECT_MESSAGE
from .env import Env
from .process import run_process
from .panel import append_to_output_panel

import sublime


class CurrentProject:
    def __init__(self, window: sublime.Window, env: Env, daemon_client: FlutterRpcClient):
        self.target_device = None # type: str | None

        self.__window = window
        self.__path = window.folders()[0]
        self.__pubspec = {}
        self.__availble_devices = {} # type: dict[str, Device]
        self.__daemon_client = daemon_client
        self.__is_running = False
        self.__running_app_id = None # type: str | None
        self.__is_pubspec_invalid = True
        self.__is_flutter_project = False
        self.__env = env
        self.__command_process = None # type: subprocess.Popen | None
        # Client for interacting with 'flutter run --machine'
        self.__run_daemon_client = None # type: FlutterRpcClient | None


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
        self.__load_pubspec()
        devices = await self.__daemon_client.device.get_devices()
        for device in devices:
            self.__availble_devices[device.id] = device
        self.__daemon_client.add_event_listener(self.__daemon_event_listener)


    def pub_get(self):
        self.__start_process_thread(["pub", "get"])


    def clean(self):
        if self.__is_flutter_project:
            self.__start_process_thread(["clean"])
        else:
            sublime.error_message(NOT_A_FLUTTER_PROJECT_MESSAGE)


    async def stop_app(self):
        if not self.__is_flutter_project:
            sublime.error_message(NOT_A_FLUTTER_PROJECT_MESSAGE)
        elif self.__is_running and (app_id := self.__running_app_id):
            await self.__daemon_client.app.stop_app(app_id)
        elif p := self.__command_process:
            os.killpg(os.getpgid(p.pid), signal.SIGTERM)
            destroy_output_panel(self.__window)
        else:
            sublime.error_message(APP_NOT_RUNNING)


    async def hot_reload(self, is_manual: bool):
        if not self.__is_flutter_project:
            sublime.error_message(NOT_A_FLUTTER_PROJECT_MESSAGE)
        elif self.__is_running and (app_id := self.__running_app_id):
            await self.__daemon_client.app.restart(
                app_id,
                is_manual=is_manual,
                full_restart=False,
            )
        else:
            sublime.error_message(APP_NOT_RUNNING)


    async def restart(self):
        if not self.__is_flutter_project:
            sublime.error_message(NOT_A_FLUTTER_PROJECT_MESSAGE)
        elif self.__is_running and (app_id := self.__running_app_id):
            await self.__daemon_client.app.restart(
                app_id,
                is_manual=True,
                full_restart=True,
            )
        else:
            sublime.error_message(APP_NOT_RUNNING)


    def pub_add(self, package_name):
        self.__start_process_thread(["pub", "add", package_name])


    def run(self, args: List[str]):
        if self.target_device and self.__is_flutter_project:
            self.__start_process_thread(["run", "-d", self.target_device] + args)
        else:
            sublime.error_message(NO_DEVICE_SELECTED)


    def has_dependency_on(self, dep):
        return self.__pubspec["dependencies"][dep] is not None


    def __load_pubspec(self):
        with open(os.path.join(self.__path, 'pubspec.yaml'), 'r') as pubspec:
            for line in pubspec:
                if line.rstrip().startswith("flutter:"):
                    self.__is_flutter_project = True
                    break


    def __daemon_event_listener(self, event):
        if isinstance(event, DeviceAddedEvent):
            self.__availble_devices[event.device.id] = event.device
        elif isinstance(event, DeviceRemovedEvent):
            self.__availble_devices.pop(event.device.id)
        elif isinstance(event, AppStartEvent):
            self.__running_app_id = event.app_id
        elif isinstance(event, AppStartedEvent):
            self.__is_running = True


    def __start_process_thread(self, command: List[str]):
        panel = create_output_panel(self.__window)

        show_output_panel(self.__window)

        Thread(
            target=self.__run_process,
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


    def __run_process(self, command: List[str], cwd: str, output_panel: sublime.View):
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=cwd,
            bufsize=1,
            start_new_session=True,
        )

        self.__command_process = process

        out = process.stdout
        if out:
            for line in iter(out.readline, b""):
                append_to_output_panel(output_panel, line)
