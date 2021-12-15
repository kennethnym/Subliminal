from .utils import dot
from .request import Request


class Daemon(object):
    __nsp = "daemon"

    # daemon events
    connected = dot(__nsp, "connected")
    log_message = dot(__nsp, "logMessage")
    show_message = dot(__nsp, "showMessage")

    # daemon commands
    @classmethod
    def shutdown(cls):
        return Request(
            method=dot(cls.__nsp, "shutdown")
        )
