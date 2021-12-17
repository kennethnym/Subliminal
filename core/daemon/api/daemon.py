from .utils import dot
from .request import Request
from .domain import Domain


class DaemonConnectedEvent(object):
    def __init__(self, version, pid) -> None:
        super().__init__()
        self.version = version
        self.pid = pid


class DaemonLogEvent(object):
    def __init__(self, log=None, error=False) -> None:
        super().__init__()
        self.log = log
        self.error = error


class DaemonShowMessageEvent(object):
    def __init__(self, level, title, message) -> None:
        super().__init__()
        self.level = level
        self.title = title
        self.message = message


class DaemonDomain(Domain):
    nsp = "daemon"

    # daemon events
    connected = dot(nsp, "connected")
    log = dot(nsp, "log")
    show_message = dot(nsp, "showMessage")

    # daemon methods
    __shutdown = dot(nsp, "shutdown")

    event_constructor_map = {
        connected: DaemonConnectedEvent,
        log: DaemonLogEvent,
        show_message: DaemonShowMessageEvent
    }


    # daemon commands
    def shutdown(self):
        super().make_request(Request(
            method=self.__shutdown,
            has_response=False,
        ))
