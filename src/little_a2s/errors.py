class Error(Exception):
    """The base class for A2S exceptions."""


class PayloadError(ValueError, Error):
    """The received A2S packet was malformed."""
