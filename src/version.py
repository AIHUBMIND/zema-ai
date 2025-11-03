"""Version information for Zema AI."""
__version__ = "0.1.8"
__version_info__ = (0, 1, 8)


def get_version() -> str:
    """Get current version"""
    return __version__


def get_version_info() -> tuple:
    """Get version as tuple"""
    return __version_info__

