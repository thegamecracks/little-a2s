class Error(Exception):
    """The base class for A2S exceptions.

    .. versionadded:: 0.6.0

    """


class PayloadError(ValueError, Error):
    """A malformed A2S packet was received.

    This is raised by :class:`A2SClientProtocol` and propagated up to
    the :class:`A2S` and :class:`AsyncA2S` clients.

    .. versionadded:: 0.6.0

    """
