from .request import Request
from .domain import Domain
from .utils import dot


class AppStartEvent:
    def __init__(self, appId: str, directory: str, deviceId: str) -> None:
        self.app_id = appId
        self.directory = directory
        self.device_id = deviceId


class AppStartedEvent:
    def __init__(self, appId: str) -> None:
        self.app_id = appId


class AppDomain(Domain):
    nsp = "app"

    # app domain events
    start = dot(nsp, "start")
    debug_port = dot(nsp, "debugPort")
    started = dot(nsp, "started")
    log = dot(nsp, "log")
    progress = dot(nsp, "progress")
    stop = dot(nsp, "dot")
    web_launch_url = dot(nsp, "web_launch_url")

    # app domain commands
    __restart = dot(nsp, "restart")

    _event_constructor_map = {
        start: AppStartEvent,
        started: AppStartedEvent
    }


    def restart(self, app_id: str, is_manual: bool, full_restart: bool = False):
        super().make_request(Request(
            method=self.__restart,
            has_response=True,
            appId=app_id,
            fullRestart=full_restart,
            reason="manual" if is_manual else "save",
        ))
