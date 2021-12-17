from ... import asyncio

class Domain:
    _event_constructor_map = {}
    '''Maps names of events to their corresponding constructor.'''

    _response_constructor_map = {}

    __request_futures = {}

    __request_types = {}

    def __init__(self, daemon) -> None:
        self.__daemon = daemon
        daemon.listen(self.__daemon_listener)


    @classmethod
    def parse_event(cls, json):
        return cls._event_constructor_map[json["event"]](**json["params"])


    def make_request(self, request):
        self.__request_types[request.id] = request.method
        future = asyncio.get_event_loop().create_future()
        if request.has_response:
            self.__request_futures[request.id] = future

        self.__daemon.make_request(request)

        if not request.has_response:
            future.set_result(None)

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
            response = self.__parse_method_response(json["result"])
            self.__request_futures[req_id].set_result(response)
        except KeyError:
            pass
