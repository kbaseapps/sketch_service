

class InvalidRequestParams(Exception):
    """The JSON data passed in a request body is invalid."""
    pass


class UnrecognizedWSType(Exception):
    """An attempt to use the service on a type that we cannot handle."""

    def __init__(self, typ, valid_types):
            self.typ = typ
            self.valid_types = valid_types

    def __str__(self):
        return ("Unable to handle type: " + self.typ +
                ". Valid types are: " + str(self.valid_types.values()))
