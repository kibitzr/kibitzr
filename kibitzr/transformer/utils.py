import functools


def wrap_dummy(transform_func):
    def transform_factory(value, conf):
        return transform_func
    return transform_factory


def bake_parametrized(transform_func, pass_conf=False, **kwargs):
    def transform_factory(value, conf):
        if pass_conf:
            return functools.partial(
                transform_func,
                value,
                conf=conf,
                **kwargs
            )
        else:
            return functools.partial(
                transform_func,
                value,
                **kwargs
            )
    return transform_factory
