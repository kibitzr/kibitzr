from six.moves import input as compat_input


def prompt_return():
    compat_input(
        "Press Enter to save Firefox profile; "
        "or close Firefox to cancel: "
    )
