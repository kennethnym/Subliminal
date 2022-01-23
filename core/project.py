import asyncio
import os
import signal
import subprocess
from threading import Thread
from typing import List, Union

from .rpc import FlutterRpcClient, FlutterRpcProcess
from .rpc.api.device import DeviceAddedEvent, DeviceRemovedEvent, Device
from .rpc.api.app import AppStartEvent, AppStartedEvent
from .panel import (
    PROJECT_RUN_OUTPUT_PANEL_NAME,
    create_output_panel,
    destroy_output_panel,
    show_output_panel,
)
from .messages import (
    PROJECT_NOT_RUNNING,
    NO_DEVICE_SELECTED,
    NOT_A_FLUTTER_PROJECT_MESSAGE,
)
from .env import Env
from .process import run_process
from .panel import append_to_output_panel

import sublime


class CurrentProject:
    def __init__(
        self,
        window: sublime.Window,
        env: Env,
        rpc_client: FlutterRpcClient,
        loop: asyncio.AbstractEventLoop,
    ):
        self.__target_device = None  # type: str | None

        self.__window = window
        self.__path = window.folders()[0]
        self.__pubspec = {}
        self.__availble_devices = {}  # type: dict[str, Device]
        self.__daemon_rpc_client = rpc_client
        self.__is_running = False
        self.__running_app_id = None  # type: str | None
        self.__loop = loop
        self.__is_pubspec_invalid = True
        self.__is_flutter_project = False
        self.__env = env
        self.__command_process = None  # type: subprocess.Popen | None
        # Client for interacting with 'flutter run --machine'
        self.__flutter_run_rpc_process = None  # type: FlutterRpcProcess | None
        self.__flutter_run_rpc_client = None  # type: FlutterRpcClient | None

    @property
    def path(self):
        return self.__path

    @property
    def window(self):
        return self.__window

    @property
    def available_devices(self):
        return self.__availble_devices.values()

    @property
    def has_connected_devices(self):
        return bool(self.__availble_devices)

    @property
    def is_running(self):
        return bool(self.__running_app_id)

    @property
    def target_device(self):
        return self.__target_device

    @property
    def is_flutter_project(self):
        return self.__is_flutter_project

    @target_device.setter
    def target_device(self, value: Union[str, None]):
        self.__target_device = value
        if view := self.__window.active_view():
            if value:
                device = self.__availble_devices[value]
                view.set_status("a_selected_device", f"Selected device: {device.name}")
            else:
                view.erase_status("a_selected_device")

    async def initialize(self):
        self.__load_pubspec()
        devices = await self.__daemon_rpc_client.device.get_devices()
        for device in devices:
            self.__availble_devices[device.id] = device
        self.__daemon_rpc_client.add_event_listener(self.__daemon_event_listener)

    def pub_get(self):
        self.__start_process_thread(["pub", "get"])

    def clean(self):
        if self.__is_flutter_project:
            self.__start_process_thread(["clean"])
        else:
            sublime.error_message(NOT_A_FLUTTER_PROJECT_MESSAGE)

    def run_tests(self, name: str = ""):
        self.__start_process_thread(
            [
                "test",
                "-r",
                "expanded",
            ]
            + (["-N", name] if name else [])
        )

    async def stop_running(self):
        if p := self.__command_process:
            os.killpg(os.getpgid(p.pid), signal.SIGTERM)
            destroy_output_panel(self.__window)
        elif self.__is_flutter_project and (app_id := self.__running_app_id):
            if self.__is_running and (rpc := self.__flutter_run_rpc_client):
                # the app is running on the device
                await rpc.app.stop_app(app_id)
            elif rpc_process := self.__flutter_run_rpc_process:
                # flutter run is triggered, build is running, but app is not running on the device
                rpc_process.terminate()
                self.__flutter_run_rpc_process = None
            destroy_output_panel(self.__window, name=PROJECT_RUN_OUTPUT_PANEL_NAME)
        else:
            sublime.error_message(PROJECT_NOT_RUNNING)

    async def hot_reload(self, is_manual: bool):
        if not self.__is_flutter_project:
            sublime.error_message(NOT_A_FLUTTER_PROJECT_MESSAGE)
        elif (
            self.__is_running
            and (app_id := self.__running_app_id)
            and (rpc := self.__flutter_run_rpc_client)
        ):
            active_view = self.__window.active_view()
            if active_view:
                active_view.set_status("z_hot_reload_status", "Hot reloading...")
            await rpc.app.restart(
                app_id,
                is_manual=is_manual,
                full_restart=False,
            )
            if active_view:
                active_view.erase_status("z_hot_reload_status")
        else:
            sublime.error_message(PROJECT_NOT_RUNNING)

    async def hot_restart(self):
        if not self.__is_flutter_project:
            sublime.error_message(NOT_A_FLUTTER_PROJECT_MESSAGE)
        elif (
            self.__is_running
            and (app_id := self.__running_app_id)
            and (rpc := self.__flutter_run_rpc_client)
        ):
            active_view = self.__window.active_view()
            if active_view:
                active_view.set_status("z_hot_restart_status", "Hot restarting...")
            await rpc.app.restart(
                app_id,
                is_manual=True,
                full_restart=True,
            )
            if active_view:
                active_view.erase_status("z_hot_restart_status")
        else:
            sublime.error_message(PROJECT_NOT_RUNNING)

    def pub_add(self, package_name):
        self.__start_process_thread(["pub", "add", package_name])

    def run(self, args: List[str]):
        if self.__is_flutter_project:
            if device := self.target_device:
                self.__start_rpc_process(
                    [self.__env.flutter_path, "run", "--machine", "-d", device] + args
                )
            else:
                sublime.error_message(NO_DEVICE_SELECTED)
        else:
            self.__start_process_thread(["run"])

    def has_dependency_on(self, dep):
        return self.__pubspec["dependencies"][dep] is not None

    def __load_pubspec(self):
        with open(os.path.join(self.__path, "pubspec.yaml"), "r") as pubspec:
            for line in pubspec:
                if line.rstrip().startswith("flutter:"):
                    self.__is_flutter_project = True
                    break

    def __daemon_event_listener(self, event):
        if isinstance(event, DeviceAddedEvent):
            self.__availble_devices[event.device.id] = event.device
        elif isinstance(event, DeviceRemovedEvent):
            self.__availble_devices.pop(event.device.id)

    def __flutter_run_rpc_event_listener(self, event):
        if isinstance(event, AppStartEvent):
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

    def __start_rpc_process(self, command: List[str]):
        panel = create_output_panel(self.__window, name=PROJECT_RUN_OUTPUT_PANEL_NAME)
        process = FlutterRpcProcess(command, self.__loop, cwd=self.__path)
        process.on_output(lambda message: append_to_output_panel(panel, message))
        rpc_client = FlutterRpcClient(process)
        rpc_client.add_event_listener(self.__flutter_run_rpc_event_listener)
        self.__flutter_run_rpc_process = process
        self.__flutter_run_rpc_client = rpc_client

        show_output_panel(self.__window, name=PROJECT_RUN_OUTPUT_PANEL_NAME)
        process.start()

    def __run_process(self, command: List[str], cwd: str, panel: sublime.View):
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=cwd,
            bufsize=1,
            start_new_session=True,
        )

        self.__command_process = process

        if out := process.stdout:
            for line in iter(out.readline, b""):
                append_to_output_panel(panel, str(line, encoding="utf8"))
