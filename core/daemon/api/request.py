import json
import random

class Request:
    def __init__(self, method: str, has_response: bool, **kwargs) -> None:
        self.__method = method
        self.__args = kwargs
        self.__id = random.getrandbits(32)
        self.__has_response = has_response


    @property
    def has_response(self):
        return self.__has_response


    @property
    def id(self):
        return self.__id


    @property
    def method(self):
        return self.__method


    def serialize(self):
        j = {"method": self.__method, "id": self.__id}
        if self.__args:
            j.update(self.__args)
        return json.dumps([j])
