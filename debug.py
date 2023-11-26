import inspect


class Debug:
    allowed = ['default']

    @classmethod
    def print(cls, *args, label="default", **kw):
        if label in Debug.allowed:
            last_call = inspect.stack()[0]
            print(f"({label}, {last_call.function}() at {last_call.lineno}):",*args, **kw)