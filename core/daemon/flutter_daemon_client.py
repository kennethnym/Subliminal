from typing import Any, Callable
from .flutter_daemon import DaemonData
from .api.device import DeviceDomain
from .api.daemon import DaemonDomain
from .api.utils import get_event_domain


class FlutterDaemonClient:
    __event_json_parser: dict[str, Callable[[DaemonData], Any]] = {
        DaemonDomain.nsp: DaemonDomain.parse_event,
        DeviceDomain.nsp: DeviceDomain.parse_event,
    }

    def __init__(self, daemon) -> None:
        self.__daemon_domain = DaemonDomain(daemon)
        self.__device_domain = DeviceDomain(daemon)
        self.__event_listeners = []

        daemon.listen(self.__daemon_listener)


    @property
    def daemon(self):
        return self.__daemon_domain


    @property
    def device(self):
        return self.__device_domain


    def add_event_listener(self, listener):
        self.__event_listeners.append(listener)


    def __daemon_listener(self, json):
        if "event" in json:
            domain = get_event_domain(json["event"])
            event = self.__event_json_parser[domain](json)
            for listener in self.__event_listeners:
                listener(event)
