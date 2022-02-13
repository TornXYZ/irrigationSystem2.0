class Error(Exception):
    """Base class for custom exceptions"""
    pass

class PotDoubletteError(Error):
    """Raised when a pot is added to an already occupied slot."""


class PotNotExistingError(Error):
    """Raised when a pot is addressed which is not existing in th pot collection."""