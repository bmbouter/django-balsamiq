class NotImplementedException(Exception):
    pass

class AbstractUserObject:

    def _json_encode(self):
        raise NotImplementedException
