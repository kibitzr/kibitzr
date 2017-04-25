import functools


def wrap_dummy(transform_func):
    def transform(value, conf):
        return transform_func
    return transform


def bake_parametrized(transform_func, **kwargs):
    def transform(value, conf):
        return functools.partial(
            transform_func,
            value,
            **kwargs
        )
    return transform
