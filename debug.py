import inspect


class Debug:
    allowed = ['default']
    last_context = None

    @classmethod
    def print(cls, *args, label="default", **kw):
        if label in Debug.allowed:
            last_call = inspect.stack()[1]
            file_name = last_call.filename.split("\\")[-1]

            if cls.last_context != last_call.function:
                print()
                cls.last_context = last_call.function
            print(f'({label}, {last_call.function}() at {file_name}, line {last_call.lineno}):', *args, **kw)