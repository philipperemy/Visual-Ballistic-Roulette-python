class CriticalException(Exception):
    def __str__(self):
        return 'CriticalException'


class PositiveValueExpectedException(Exception):
    def __str__(self):
        return 'PositiveValueExpectedException'


class SessionNotReadyException(Exception):
    def __str__(self):
        return 'SessionNotReadyException'
