class Error(Exception):
    """The base class for A2S exceptions.

    .. versionadded:: 0.6.0

    """


class PayloadError(ValueError, Error):
    """A malformed A2S packet was received.

    .. versionadded:: 0.6.0

    """
