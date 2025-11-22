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


class ChallengeError(Error):
    """The server repeatedly challenged our client in spite of us attempting
    to comply with their challenges.

    This is a rare exception that suggests the server's A2S implementation is broken.

    .. versionadded:: 0.6.0

    """
