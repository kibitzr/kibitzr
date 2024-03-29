from .factory import fetcher_factory  # noqa


def persistent_firefox():
    from .browser.fetcher import persistent_firefox as real_persistent_firefox  # pylint: disable=import-outside-toplevel
    real_persistent_firefox()


def cleanup_fetchers():
    from .browser.launcher import cleanup  # pylint: disable=import-outside-toplevel
    cleanup()
