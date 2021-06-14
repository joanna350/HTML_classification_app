def singleton(cls):
    return cls()


def singleton_with_args(*args, **kwargs):
    def wrapper(cls):
        return cls(*args, **kwargs)
    return wrapper
