import json

class Request:
    def __init__(self, method, **kwargs) -> None:
        self.__method = method
        self.__args = kwargs

    def serialize(self):
        j = {"method": self.__method}
        j.update(self.__args)
        return json.dumps([j])
