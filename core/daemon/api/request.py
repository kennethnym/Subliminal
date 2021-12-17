import json
from uuid import uuid4

class Request:
    def __init__(self, method, has_response, **kwargs) -> None:
        self.__method = method
        self.__args = kwargs
        self.__id = uuid4()
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
        j = {"method": self.__method, "id": self.__id.int}
        if self.__args:
            j.update(self.__args)
        return json.dumps([j])
