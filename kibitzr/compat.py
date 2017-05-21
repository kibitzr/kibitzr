try:
    import sh  # noqa
except ImportError:
    # Windows alternative:
    import pbs as sh  # noqa
