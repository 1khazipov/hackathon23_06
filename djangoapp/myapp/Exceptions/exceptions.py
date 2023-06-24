

class ResourceUnavailableException(Exception):

    def __init__(self, message=None):
        self._message = message

    @property
    def message(self):
        return self._message