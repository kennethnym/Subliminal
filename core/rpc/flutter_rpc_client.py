from typing import Any, Callable, Dict

from .flutter_rpc import DaemonData, FlutterRpcProcess
from .api.app import AppDomain
from .api.device import DeviceDomain
from .api.daemon import DaemonDomain
from .api.utils import get_event_domain


DaemonEventListener = Callable[[Any], None]

class FlutterRpcClient:
    __event_json_parser: Dict[str, Callable[[DaemonData], Any]] = {
        DaemonDomain.nsp: DaemonDomain.parse_event,
        DeviceDomain.nsp: DeviceDomain.parse_event,
        AppDomain.nsp: AppDomain.parse_event,
    }

    def __init__(self, process: FlutterRpcProcess) -> None:
        self.__daemon_domain = DaemonDomain(process)
        self.__device_domain = DeviceDomain(process)
        self.__app_domain = AppDomain(process)
        self.__event_listeners = [] # type: list[DaemonEventListener]

        process.listen(self.__daemon_listener)


    @property
    def daemon(self):
        return self.__daemon_domain


    @property
    def device(self):
        return self.__device_domain


    @property
    def app(self):
        return self.__app_domain


    def add_event_listener(self, listener: DaemonEventListener):
        self.__event_listeners.append(listener)


    def __daemon_listener(self, json):
        if "event" in json:
            domain = get_event_domain(json["event"])
            event = self.__event_json_parser[domain](json)
            if event:
                for listener in self.__event_listeners:
                    listener(event)
