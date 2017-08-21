try:
    import sh  # noqa
except ImportError:
    # Windows alternative:
    import pbs as sh  # noqa

try:
    from smtplib import SMTPNotSupportedError  # noqa
except ImportError:
    # SMTPNotSupportedError is new in 3.5
    from smtplib import SMTPException as SMTPNotSupportedError  # noqa
