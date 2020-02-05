class InvalidJSON(Exception):

    def __init__(self, msg):
        self.message = msg


class InvalidParams(Exception):
    """The JSON data passed in a request body is invalid."""

    def __init__(self, req_id, msg):
        self.req_id = req_id
        self.message = msg


class UnknownMethod(Exception):

    def __init__(self, req_id, msg):
        self.req_id = req_id
        self.message = msg


class UnrecognizedWSType(Exception):
    """An attempt to use the service on a type that we cannot handle."""

    def __init__(self, typ, valid_types):
        self.typ = typ
        self.valid_types = valid_types

    def __str__(self):
        return ("Unable to handle type: " + self.typ +
                ". Valid types are: " + str(self.valid_types.values()))
