# -*- coding: utf-8 -*-


class FailedLoginException(Exception):
    """User is not logged in"""

    def __init__(self):
        msg = 'User not logged in'
        super().__init__(msg)


class UnsupportedBrowserException(Exception):
    """Browser not supported or not compatible"""

    def __init__(self):
        msg = 'Browser not supported'
        super().__init__(msg)


class ElementNotFoundException(Exception):
    """The element not found"""

    def __init__(self):
        msg = 'Timed out and element was not found'
        super().__init__(msg)


class InvalidFileException(Exception):
    """The path to the file is invalid"""

    def __init__(self):
        msg = 'Path does not contain file'
        super().__init__(msg)
