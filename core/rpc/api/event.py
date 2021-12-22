class DaemonEvent(object):
    def __init__(self, name, params) -> None:
        super().__init__()
        self.name = name
        self.params = params

    @classmethod
    def from_json(cls, json):
        return DaemonEvent(json["event"], json["params"])
