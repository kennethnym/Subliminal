import asyncio

from .request import Request
from ..flutter_daemon import FlutterDaemon

class Domain:
    _event_constructor_map = {}
    '''Maps names of events to their corresponding constructor.'''

    _response_constructor_map = {}

    def __init__(self, daemon: FlutterDaemon) -> None:
        self.__daemon = daemon
        self.__request_futures = {} # type: dict[int, asyncio.Future]
        self.__request_types = {}   # type: dict[int, str]
        daemon.listen(self.__daemon_listener)


    @classmethod
    def parse_event(cls, json):
        try:
            return cls._event_constructor_map[json["event"]](**json["params"])
        except KeyError:
            return None


    def make_request(self, request: Request):
        self.__request_types[request.id] = request.method
        future = asyncio.get_event_loop().create_future()
        self.__request_futures[request.id] = future
        self.__daemon.make_request(request)

        return future


    def __parse_method_response(self, response):
        req_id = response["id"]
        result = response["result"]
        method = self.__request_types[req_id]
        constructor = self._response_constructor_map[method]

        if isinstance(result, list):
            return [constructor(**item) for item in result]

        return constructor(**result)


    def __daemon_listener(self, json):
        try:
            req_id = json["id"]
            future = self.__request_futures[req_id]

            response = None
            if "result" in json:
                response = self.__parse_method_response(json)

            future.get_loop().call_soon_threadsafe(future.set_result, response)
        except KeyError as e:
            print(e)
            pass
